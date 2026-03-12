from enum import Enum
import os
from collections import defaultdict
from typing import Dict, List

import torch
from sentence_transformers import SentenceTransformer, util
from torch import Tensor

from config.logger import logger
from task5.version_protocol import Searcher

# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# "sentence-transformers/all-mpnet-base-v2"  - точнее, но медленнее
# "cointegrated/rubert-tiny2" - для русского языка

FILE_TO_SAVE_DOC_VECS = "task5/doc_vecs.pt"


class SelectType(Enum):
    MAX = "max",
    AVG = "avg"

SEQ_LENGTH = 500
OVERLAP = 200

class TransformerSearcher(Searcher):
    """
    Поисковик, который работает следующим образом:
    строку запроса переводим в вектор с помощью transformer,
    далее для каждого докомента считаем его вектор (тоже с transformer sentences),
    ранжируем документы по косинусной близости вектора запроса и вектора документа.
    """

    def __init__(self, doc_texts: Dict[int, str], use_from_cache_if_exists: bool, select_type: SelectType):
        self.doc_texts = doc_texts
        self.model = SentenceTransformer("cointegrated/rubert-tiny2")
        self.model.max_seq_length = SEQ_LENGTH

        self.chunk_vecs = []
        self.chunk_to_doc_id = []
        self._prepare_index(use_from_cache_if_exists)
        self.select_type = select_type

    def _prepare_index(self, use_from_cache_if_exists: bool):
        if use_from_cache_if_exists and os.path.exists(FILE_TO_SAVE_DOC_VECS):
            cache = torch.load(FILE_TO_SAVE_DOC_VECS)
            self.chunk_vecs = cache["vecs"]
            self.chunk_to_doc_id = cache["ids"]
        else:
            all_chunks = []
            # Настройка параметров под модель
            max_length = SEQ_LENGTH  # Максимальный контекст rubert-tiny-v2
            overlap = OVERLAP      # Нахлест, чтобы не терять смысл на стыках
            
            # Получаем токенизатор из модели SentenceTransformer
            tokenizer = self.model.tokenizer 
            
            step = max_length - overlap 
    
            for doc_id, text in self.doc_texts.items():
                tokens = tokenizer.encode(text, add_special_tokens=False)
                n_tokens = len(tokens)
    
                if n_tokens <= max_length:
                    chunks_ids = [tokens]
                else:
                    chunks_ids = []
                    for i in range(0, n_tokens, step):
                        # Если текущее окно выходит за пределы текста
                        if i + max_length >= n_tokens:
                            # Берем последние 2048 токенов документа (fixed size)
                            last_chunk = tokens[-max_length:]
                            chunks_ids.append(last_chunk)
                            break # Завершаем обработку документа
                        
                        # Обычный полный чанк
                        chunk = tokens[i : i + max_length]
                        chunks_ids.append(chunk)
    
                # Декодируем токены обратно в текст для метода encode
                for chunk_id in chunks_ids:
                    chunk_text = tokenizer.decode(chunk_id, skip_special_tokens=True)
                    all_chunks.append(chunk_text)
                    self.chunk_to_doc_id.append(doc_id)
    
            # Эмбеддинги считаем один раз для всех чанков
            self.chunk_vecs = self.model.encode(
                all_chunks, 
                convert_to_tensor=True, 
                show_progress_bar=True,
                batch_size=16 # 2048 — это тяжелый контекст, батч лучше держать небольшим
            )
            self.flush_doc_vecs_to_file()

    def flush_doc_vecs_to_file(self):
        cache = {"vecs": self.chunk_vecs, "ids": self.chunk_to_doc_id}
        torch.save(cache, FILE_TO_SAVE_DOC_VECS)

    def _get_query_vec(self, query: str) -> Tensor:
        vec = self.model.encode(query, convert_to_tensor=True)

        return vec

    def get_docs(self, query: str) -> List[int]:
        query_vec = self._get_query_vec(query)

        # 1. Получаем сходство для ВСЕХ чанков (например, их 100)
        similarities = util.cos_sim(query_vec, self.chunk_vecs)[0]

        doc_scores = defaultdict(list)
        for score, doc_id in zip(similarities, self.chunk_to_doc_id):
            doc_scores[doc_id].append(score.item())

        if self.select_type == SelectType.AVG:
            doc_scores = {d_id: sum(s) / len(s) for d_id, s in doc_scores.items()}
        elif self.select_type == SelectType.MAX:
            doc_scores = {d_id: max(s) for d_id, s in doc_scores.items()}
        else:
            raise Exception()

        # 3. Сортируем документы по их максимальному скору
        # Сортируем список кортежей (doc_id, score) по убыванию score
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        pretty_docs = "\n".join(
            [f"  ID: {idx: <5} | Score: {score:.4f}" for idx, score in sorted_docs]
        )

        logger.info(f"sorted_docs: {pretty_docs}")

        # 4. Берем топ-K уникальных ID
        # top_k = 10
        result_ids = [doc_id for doc_id, score in sorted_docs]

        return result_ids

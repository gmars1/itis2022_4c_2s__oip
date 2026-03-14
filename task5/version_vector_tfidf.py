from collections import defaultdict
from typing import Dict, List

import numpy as np
from nltk.tokenize import word_tokenize

from config.logger import logger
from task2.main import (
    detect_language,
    language_specific_lemmatizer,
    language_specific_word_info_getter,
)
from task5.version_protocol import Searcher


class VectorTFIdfSearcher(Searcher):
    """
    Поисковик, который работает следующим образом:
    для каждого слова в поисковом запросе пытаемся получить его лемму,
    далее считаем считаем tfidf леммы (как среднее tfidf по всем документам),
    заполняем вектор запроса этими tfidf (остальные ячейки - нули),
    далее для каждого документа считаем его вектор (такой же вектор всех лемм, со значениями tfidf лемм из документа),
    ранжируем документы по косинусной близости вектора запроса и вектора документа.
    """

    def __init__(
        self,
        all_lemmas: List[str],
        tfidf_lemmas: Dict[int, Dict[str, List[float]]],
    ):
        self.all_lemmas = all_lemmas
        self.lemma_indexes = {
            lemma: idx for idx, lemma in enumerate(all_lemmas)
        }  # todo
        self.tfidf_lemmas = tfidf_lemmas

    def _get_query_vec(self, query: str) -> np.ndarray:
        """
        Convert query to TF-IDF vector. Convert each word to lemma, and calculate tfidf for it.
        """
        # Initialize zero vector
        vec = np.zeros(len(self.all_lemmas))

        # Tokenization
        tokens = word_tokenize(query.lower())
        logger.debug(f"word_tokenize query: {tokens}")
        if not tokens:
            logger.warning(f"tokenizer could not tokenize user query")
            return vec

        # Count term frequencies in query
        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1

        for token, freq in term_freq.items():
            # Try to get lemma for the token
            lemma = token
            lang = detect_language(token)
            if lang:
                word_info = language_specific_word_info_getter(token, lang)
                if word_info:
                    lemma = language_specific_lemmatizer(word_info, lang)

            # so, now we have lemma of query word
            if lemma in self.all_lemmas:
                idx = self.lemma_indexes[lemma]
                # get avg idf for lemma in all docs
                scores = [
                    floats[1]
                    for doc_index, doc_data in self.tfidf_lemmas.items()
                    for lemma, floats in doc_data.items()
                ]
                # logger.info(f"scores: {scores}")

                tfidf_avg = np.mean(scores) if scores else 0.0
                vec[idx] = tfidf_avg
        
        return vec

    def _get_doc_vec(self, doc_id: int) -> np.ndarray:
        """Get document vector"""
        vec = np.zeros(len(self.all_lemmas))

        if doc_id not in self.tfidf_lemmas.keys():
            logger.warning(f"was given not existing doc_id: {doc_id}")
            return vec

        doc_data = self.tfidf_lemmas[doc_id]
        for lemma, (idf, tfidf) in doc_data.items():
            if lemma in self.lemma_indexes.keys():
                idx = self.lemma_indexes[lemma]
                vec[idx] = tfidf

        return vec

    def get_docs(self, query: str) -> list[tuple[int, float]]:
        """Get document IDs sorted by relevance to query using cosine similarity"""
        query_vec = self._get_query_vec(query)

        # If query vector is all zeros, return empty list
        if np.linalg.norm(query_vec) == 0:
            return []

        # Compute cosine similarity for each document
        scores = []
        for doc_id in self.tfidf_lemmas.keys():
            doc_vec = self._get_doc_vec(doc_id)
            norm_d = np.linalg.norm(doc_vec)
            if norm_d > 0:
                similarity = np.dot(query_vec, doc_vec) / (
                    np.linalg.norm(query_vec) * norm_d
                )
            else:
                similarity = 0.0
                
            if similarity != 0.0:
                scores.append((doc_id, similarity))

        # Sort by similarity descending
        scores.sort(key=lambda x: x[1], reverse=True)
        logger.debug(
            "scores:\n{}",
            "\n".join(f"doc_id: {doc_id:<6} score: {score.item():.3f}" for doc_id, score in scores),
        )

        # Return document IDs in order of relevance
        return [(doc_id, score.item()) for doc_id, score in scores]

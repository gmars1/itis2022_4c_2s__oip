# from typing import Dict, List

# from torch import Tensor


# from task5.version_protocol import Searcher
# from sentence_transformers import SentenceTransformer, util

# # model_name = "sentence-transformers/all-MiniLM-L6-v2" 
# # "sentence-transformers/all-mpnet-base-v2"  - точнее, но медленнее
# # "cointegrated/rubert-tiny2" - для русского языка

# class TransformerSearcher(Searcher):
#     """
#     Поисковик, который работает следующим образом:
#     строку запроса переводим в вектор с помощью transformer,
#     далее для каждого докомента считаем его вектор (тоже с transformer sentences),
#     ранжируем документы по косинусной близости вектора запроса и вектора документа.
#     """
    
#     def __init__(
#         self,
#         doc_texts: Dict[int, str]
#     ):
#         self.doc_texts = doc_texts
#         self.model = SentenceTransformer('cointegrated/rubert-tiny2')
#         self.docs_vecs = self.model.encode(
#                     list(self.doc_texts.values()),
#                     convert_to_tensor=True,
#                     show_progress_bar=True
#                 )

#     def _get_query_vec(self, query: str) -> Tensor:
        
#         vec = self.model.encode(query, convert_to_tensor=True)
        
#         return vec


#     def get_docs(self, query: str) -> List[int]:
#         query_vec = self._get_query_vec(query)

        
#         similarities = util.cos_sim(query_vec, self.docs_vecs)[0]
                
#         top_k = 10
#         top_indices = similarities.topk(min(top_k, len(similarities))).indices.cpu().numpy()
        
#         doc_ids = list(self.doc_texts.keys())
#         result_ids = [doc_ids[idx] for idx in top_indices]
        
#         return result_ids
        
        

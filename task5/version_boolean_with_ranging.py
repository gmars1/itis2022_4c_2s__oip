import math
from typing import Dict, List, Set

import numpy as np

from config.logger import logger
from task2.main import (
    detect_language,
    language_specific_lemmatizer,
    language_specific_word_info_getter,
)
from task3.search import (
    PRIORITY,
    check_user_query,
    convert_to_postfix,
    eveluate_query,
    split_user_query,
)
from task5.version_protocol import Searcher


class BooleanWithRangingSearcher(Searcher):
    """
    Поисковик, который работает следующим образом:
    фильрует документы по булевым операторам в запросе,
    далее для каждого документа считаем его score
      (считаем score на основе булева запроса:
          если 'and' - то min tfidf операндов,
          если 'or' - max,
          если 'not' - пропускаем),
    ранжируем документы по score.
    """

    def __init__(
        self,
        doc_texts: Dict[int, str],
        invert_index: Dict[str, Set[int]],
        lemmas_invert_index: Dict[str, Set[int]],
        token_to_lemma: Dict[str, str],
        lemma_tokens: Dict[str, Set[str]],
        tfidf_tokens: Dict[int, Dict[str, list[float]]],
        tfidf_lemmas: Dict[int, Dict[str, list[float]]],
    ):
        self.doc_texts = doc_texts
        self.invert_index = invert_index
        self.lemmas_invert_index = lemmas_invert_index
        self.token_to_lemma = token_to_lemma
        self.lemma_tokens = lemma_tokens
        self.tfidf_tokens = tfidf_tokens
        self.tfidf_lemmas = tfidf_lemmas

    def _query_to_postfix_notation(self, user_query: str) -> list[str]:
        # transform query
        user_query = user_query.lower()

        # split into parts
        splitted = split_user_query(user_query)

        # check query
        if not check_user_query(splitted):
            return []

        return convert_to_postfix(splitted)

    def _filter_docs(self, postfix_query: list[str]) -> Set[int]:
        return eveluate_query(
            postfix_query, self.invert_index, self.lemmas_invert_index
        )

    def get_tfidf_of_query_word_in_doc(
        self,
        word: str,
        doc_id: int,
        tfidf_tokens: Dict[int, Dict[str, list[float]]],
        tfidf_lemmas: Dict[int, Dict[str, list[float]]],
    ) -> float:
        """получаем tfidf слова в запросе:
        если слово в "", то получаем tfidf точного слова,
        если без "", то получаем tdfidf леммы в документе
        """
        r = 0
        # ищем по точному совпадению
        if word.startswith('"') and word.endswith('"'):
            doc = tfidf_tokens[doc_id]
            word = word[1:-1]
            if word in doc:
                r = doc[word][1]
        else:
            # ищем по точному совпадению
            # + пробуем получить лемму и ищем по другим формам
            doc = tfidf_tokens[doc_id]
            if word in doc:
                r = doc[word][1]

            lang = detect_language(word)
            if not lang:
                logger.warning(f"getting tfidf of query word: cant detect lang of: {word}")
                # print(f"CANT DETECT LANG: {token}")
                return r
            lemma = language_specific_lemmatizer(
                language_specific_word_info_getter(word, lang), lang
            )
            doc_lemmas = tfidf_lemmas[doc_id]
            if lemma and lemma in doc_lemmas.keys():
                r = doc_lemmas[lemma][1]
        return r

    def _range_docs(
        self,
        filtered: Set[int],
        query_postfix_notation: list[str],
        tfidf_tokens: Dict[int, Dict[str, list[float]]],
        tfidf_lemmas: Dict[int, Dict[str, list[float]]],
    ) -> list[int]:
        logger.debug(f"query_postfix_notation: {query_postfix_notation}")

        doc_scores = dict()

        for doc_id in filtered:
            stack = []
            for token in query_postfix_notation:
                if token == "(" or token == ")":
                   continue 
                # если просто слово: добавляем в stack
                elif token not in PRIORITY.keys():
                    tfidf = self.get_tfidf_of_query_word_in_doc(
                        token, doc_id, tfidf_tokens, tfidf_lemmas
                    )
                    logger.debug(f"tfidf of {token} in doc {doc_id} : {tfidf}")
                    stack.append(tfidf)

                elif PRIORITY[token] == 3:
                    # получаем операнд, который надо отсечь
                    stack.pop()

                else:
                    # операции and, or - бинарные: берем 2 операнда
                    right = stack.pop()
                    left = stack.pop()

                    if PRIORITY[token] == 2:
                        stack.append(min(left, right))
                    else:
                        stack.append(np.mean([left, right]))

            doc_scores[doc_id] = stack[0] if stack else 0

        # Сортируем элементы словаря по значению (score) в обратном порядке (от большего к меньшему)
        sorted_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)

        sorted_docs_pretty = "\n" + "\n".join(
            [f"doc_id: {doc_id} score: {score}" for doc_id, score in sorted_docs]
        )
        logger.debug(f"sorted_docs: {sorted_docs_pretty}")

        # Возвращаем только список doc_id
        return [doc_id for doc_id, score in sorted_docs]

    def get_docs(self, query: str) -> List[int]:
        query_postfix_notation = self._query_to_postfix_notation(query)

        filtered = self._filter_docs(query_postfix_notation)

        ranged = self._range_docs(
            filtered, query_postfix_notation, self.tfidf_tokens, self.tfidf_lemmas
        )
        # ranged = list(filtered)

        return ranged

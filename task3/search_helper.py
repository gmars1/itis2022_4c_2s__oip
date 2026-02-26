from typing import Dict, Set

from task2.main import (
    detect_language,
    language_specific_lemmatizer,
    language_specific_word_info_getter,
)


def get_indexes_of_query_word(
    token: str,
    invert_index: Dict[str, Set[int]],
    token_to_lemma: Dict[str, str],
    lemma_tokens: Dict[str, Set[str]],
) -> Set[int]:
    """
    Функция для получения индексов файлов по запросу.
    Если слово в "", то ищется точное совпадение,
    иначе - включая другие формы слова.
    """
    r = set()
    # ищем по точному совпадению
    if token.startswith('"') and token.endswith('"'):
        r = r.union(invert_index.get(token[1:-1], set()))
    else:
        # ищем по точному совпадению
        # + пробуем получить лемму и ищем по другим формам
        r = r.union(invert_index.get(token, set()))
        lang = detect_language(token)
        if not lang:
            # print(f"CANT DETECT LANG: {token}")
            return r
        lemma = language_specific_lemmatizer(
            language_specific_word_info_getter(token, lang), lang
        )
        if lemma in lemma_tokens.keys():
            other = lemma_tokens[str(lemma)]
            indexes = set().union(*(invert_index.get(token, set()) for token in other))
            r = r.union(indexes)
    return r

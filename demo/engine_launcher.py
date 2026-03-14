from typing import Dict, Set

from files_management.files_accessor import FilesAccessor
from task5.version_boolean_with_ranging import BooleanWithRangingSearcher
from task5.version_protocol import Searcher
from task5.version_transformer import SelectType, TransformerSearcher
from task5.version_vector_tfidf import VectorTFIdfSearcher


def launch():
    invert_index: Dict[str, Set[int]] = dict()
    lemmas_invert_index: Dict[str, Set[int]] = dict()
    all_lemmas: Set[str] = set()

    token_to_lemma: Dict[str, str] = dict()  # token -> lemma
    lemma_tokens: Dict[str, Set[str]] = dict()  # lemma -> tokens

    tfidf_lemmas: Dict[int, Dict[str, list[float]]] = dict()
    tfidf_tokens: Dict[int, Dict[str, list[float]]] = dict()

    doc_texts: Dict[int, str] = dict()

    files = FilesAccessor()

    # loading from file
    print("Loading invert index file...")
    files.load_invert_index_file(invert_index)
    
    print("Loading lemmas invert index file...")
    files.load_lemmas_invert_index_file(lemmas_invert_index)

    print("Loading lemmas file...")
    files.load_lemmas_file_to_set(all_lemmas)
    all_lemmas_list = sorted(all_lemmas)

    print("Loading lemmas file...")
    files.load_lemmas_file_bidirectional(token_to_lemma, lemma_tokens)

    print("Loading tfidf folders...")
    files.load_tfidf_folders(tfidf_tokens, tfidf_lemmas)

    print("Load doc texts")
    files.get_text_from_docs(doc_texts)

    tfidf_searcher: Searcher = VectorTFIdfSearcher(all_lemmas_list, tfidf_lemmas)
    boolean_with_ranger_searcher: Searcher = BooleanWithRangingSearcher(
        doc_texts,
        invert_index,
        lemmas_invert_index,
        token_to_lemma,
        lemma_tokens,
        tfidf_tokens,
        tfidf_lemmas,
    )
    transformer_searcher_avg: Searcher = TransformerSearcher(doc_texts, True, SelectType.AVG)
    # transformer_searcher_max: Searcher = TransformerSearcher(doc_texts, True, SelectType.MAX)

    searchers = {
        "tfidf": tfidf_searcher,
        "boolean": boolean_with_ranger_searcher,
        "transformer": transformer_searcher_avg,
    }
    return searchers

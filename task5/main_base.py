import os
from time import sleep
from typing import Dict, Set

from config.logger import logger
from files_management.files_accessor import (
    TASK4_TFIDF_LEMMAS,
    TASK4_TFIDF_TOKENS,
    FilesFacade,
)
from task5.version_boolean_with_ranging import BooleanWithRangingSearcher
from task5.version_protocol import Searcher
from task5.version_transformer import TransformerSearcher, SelectType
from task5.version_vector_tfidf import VectorTFIdfSearcher


def interactive_search(
    user_query: str,
    choosen_searcher: Searcher,
) -> str:
    res = choosen_searcher.get_docs(user_query)

    if len(res) == 0:
        return "nothing has found"

    # convert to str
    result = ", ".join(list(map(str, res)))
    return result

def clean_user_inpp(inpp: str) -> str:
    clean_query = inpp.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")
    clean_query = " ".join(clean_query.split())
    return clean_query


def main() -> None:
    invert_index: Dict[str, Set[int]] = dict()
    lemmas_invert_index: Dict[str, Set[int]] = dict()
    all_lemmas: Set[str] = set()

    token_to_lemma: Dict[str, str] = dict()  # token -> lemma
    lemma_tokens: Dict[str, Set[str]] = dict()  # lemma -> tokens

    tfidf_lemmas: Dict[int, Dict[str, list[float]]] = dict()
    tfidf_tokens: Dict[int, Dict[str, list[float]]] = dict()

    doc_texts: Dict[int, str] = dict()

    files = FilesFacade()

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
    transformer_searcher_max: Searcher = TransformerSearcher(doc_texts, True, SelectType.AVG)
    # transformer_searcher_avg: Searcher = TransformerSearcher(doc_texts, True, SelectType.AVG)
    
    # add bm25 + transfromer 

    searchers = {
        "tfidf": tfidf_searcher,
        "boolean": boolean_with_ranger_searcher,
        "transformer": transformer_searcher_max,
    }
    choosen_searcher = tfidf_searcher

    #
    # REPL cicle todo
    closed = False
    engine_chosen = False
    while not engine_chosen:
        inpp: str = input(f"choose engine: {searchers.keys()}\n")
        inpp = clean_user_inpp(inpp)
        if inpp == "":
            inpp = "tfidf"
        if inpp not in searchers.keys():
            continue
        choosen_searcher = searchers[inpp]
        engine_chosen = True

    while not closed:
        print("==================")
        inp: str = input(
            "(enter 'quit' to leave):\n(enter 'switch' to change engine):\nENTER QUERY: "
        )
        inp = clean_user_inpp(inp)
        if inp == "quit":
            closed = True
            break
        elif inp == "switch":
            inputed = False
            while not inputed:
                npp: str = input(f"choose engine: {searchers.keys()}\n")
                npp = clean_user_inpp(npp)
                if npp not in searchers.keys():
                    continue
                choosen_searcher = searchers[npp]
                inputed = True
        else:
            # perform search
            result = interactive_search(inp, choosen_searcher)
            print(
                f"\nRESULT FOR '{inp}':\n{result}\n====================================\n"
            )
            sleep(1)


if __name__ == "__main__":
    main()

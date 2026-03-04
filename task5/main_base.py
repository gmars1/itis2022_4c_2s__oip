import os
from time import sleep
from typing import Dict, Set

from config.logger import logger
from task3.search import (
    load_invert_index_file,
    load_lemmas_file,
)
from task5.version_protocol import Searcher
from task5.version_vector_tfidf import VectorTFIdfSearcher


def get_text_from_docs(foldername: str, doc_texts: Dict[int, str]) -> None:
    for root, _, files in os.walk(foldername):
        for file in files:
            filepath = os.path.join(root, file)
            file_index = int(filepath.replace("task1/crawled/", "").replace(".txt", ""))
            with open(filepath, encoding="utf-8") as f:
                doc_texts.setdefault(file_index, f.read())


def load_all_lemmas_file(file: str, all_lemmas: Set[str]):
    with open(file, encoding="utf-8") as f:
        for line in f:
            all_lemmas.add(line.strip().split()[0])


def load_tfidf_folders(
    tfidf_tokens_folder: str,
    tfidf_lemmas_folder: str,
    tfidf_tokens: Dict[int, Dict[str, list[float]]],
    tfidf_lemmas: Dict[int, Dict[str, list[float]]],
):
    for root, _, files in os.walk(tfidf_tokens_folder):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, encoding="utf-8") as f:
                index = int(filepath[19:-4])
                data: Dict[str, list[float]] = dict()
                for line in f:
                    splitted = line.split()
                    data.setdefault(splitted[0], list(map(float, splitted[1:3])))
                tfidf_tokens.setdefault(index, data)

    for root, _, files in os.walk(tfidf_lemmas_folder):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, encoding="utf-8") as f:
                index = int(filepath[19:-4])
                data = dict()
                for line in f:
                    splitted = line.split()
                    data.setdefault(splitted[0], list(map(float, splitted[1:3])))
                tfidf_lemmas.setdefault(index, data)


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


def main() -> None:
    invert_index: Dict[str, Set[int]] = dict()
    all_lemmas: Set[str] = set()

    token_to_lemma: Dict[str, str] = dict()  # token -> lemma
    lemma_tokens: Dict[str, Set[str]] = dict()  # lemma -> tokens

    tfidf_lemmas: Dict[int, Dict[str, list[float]]] = dict()
    tfidf_tokens: Dict[int, Dict[str, list[float]]] = dict()

    doc_texts: Dict[int, str] = dict()

    # loading from file
    print("Loading invert index file...")
    load_invert_index_file("task3/invert_index.txt", invert_index)

    print("Loading lemmas file...")
    load_all_lemmas_file("task2/lemmas.txt", all_lemmas)
    all_lemmas_list = sorted(all_lemmas)

    print("Loading lemmas file...")
    load_lemmas_file("task2/lemmas.txt", token_to_lemma, lemma_tokens)

    print("Loading tfidf folders...")
    load_tfidf_folders(
        "task4/tfidf_tokens", "task4/tfidf_lemmas", tfidf_tokens, tfidf_lemmas
    )

    print("Load doc texts")
    get_text_from_docs("task1/crawled/", doc_texts)

    tfidf_searcher: Searcher = VectorTFIdfSearcher(all_lemmas_list, tfidf_lemmas)

    searchers = {"tfidf": tfidf_searcher}
    choosen_searcher = tfidf_searcher

    #
    # REPL cicle todo
    closed = False
    engine_chosen = False
    while not engine_chosen:
        inpp: str = input(f"choose engine: {searchers.keys()}\n")
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
        if inp == "quit":
            closed = True
            break
        if inp == "switch":
            inputed = False
            while not inputed:
                npp: str = input(f"choose engine: {searchers.keys()}\n")
                if npp not in searchers.keys():
                    continue
                choosen_searcher = searchers[npp]
                inputed = True
        # perform search
        result = interactive_search(inp, choosen_searcher)
        print(
            f"\nRESULT FOR '{inp}':\n{result}\n====================================\n"
        )
        sleep(1)


if __name__ == "__main__":
    main()

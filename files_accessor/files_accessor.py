import os
from typing import Dict, Set

TASK1_TARGET_LIST = "task1/target_list.txt"
TASK1_CRAWLED = "task1/crawled"
TASK1_INDEX = "task1/index.txt"

TASK2_TOKENS = "task2/tokens.txt"
TASK2_LEMMAS = "task2/lemmas.txt"

TASK2_TOKENS_FOLDER = "task2/tokens/"
TASK2_LEMMAS_FOLDER = "task2/lemmas/"

TASK3_INVERT_INDEX = "task3/invert_index.txt"
TASK3_LEMMAS_INVERT_INDEX = "task3/lemmas_invert_index.txt"

TASK4_TFIDF_TOKENS = "task4/tfidf_tokens"
TASK4_TFIDF_LEMMAS = "task4/tfidf_lemmas"


class FilesFacade:
    def get_links(self, filename: str = TASK1_TARGET_LIST) -> list[str]:
        """Load links from file"""
        with open(filename) as f:
            links = [line for line in f]
        return links

    def get_text_from_docs(
        self, doc_texts: Dict[int, str], foldername: str = TASK1_CRAWLED
    ) -> None:
        for root, _, files in os.walk(foldername):
            for file in files:
                filepath = os.path.join(root, file)
                file_index = int(
                    filepath.replace("task1/crawled/", "").replace(".txt", "")
                )
                with open(filepath, encoding="utf-8") as f:
                    doc_texts.setdefault(file_index, f.read())

    # def get_index(self):

    def load_allowed_words_file(
        self, allowed_words: Set[str], filename: str = TASK2_TOKENS
    ):
        with open(filename, encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                allowed_words.add(word)

    def load_lemmas_file(
        self, word_to_lemma: Dict[str, str], filename: str = TASK2_LEMMAS
    ):
        with open(filename, encoding="utf-8") as f:
            for line in f:
                splitted = line.split(" ")
                lemma = splitted[0]
                words = splitted[1:]
                for word in words:
                    word_to_lemma.setdefault(word, lemma)

    def load_invert_index_file(
        self, invert_index: Dict[str, Set[int]], filename: str = TASK3_INVERT_INDEX
    ):
        with open(filename, encoding="utf-8") as f:
            for line in f:
                splitted = line.strip().split(" ")
                word = splitted[0]
                indexes = set(map(int, splitted[1:]))
                invert_index.setdefault(word, indexes)

    def load_lemmas_invert_index_file(
        self,
        lemmas_invert_index: Dict[str, Set[int]],
        filename: str = TASK3_LEMMAS_INVERT_INDEX,
    ):
        self.load_invert_index_file(lemmas_invert_index, filename)

    def load_lemmas_file_bidirectional(
        self,
        token_to_lemma: Dict[str, str],
        lemma_tokens: Dict[str, Set[str]],
        filename: str = TASK2_LEMMAS,
    ):
        with open(filename, encoding="utf-8") as f:
            for line in f:
                splitted = line.split(" ")
                lemma = splitted[0]
                words = splitted[1:]
                lemma_tokens[lemma] = set(words)
                for word in words:
                    token_to_lemma.setdefault(word, lemma)

    def load_lemmas_file_to_set(self, all_lemmas: Set[str], file: str = TASK2_LEMMAS):
        with open(file, encoding="utf-8") as f:
            for line in f:
                all_lemmas.add(line.strip().split()[0])

    def load_tfidf_folders(
        self,
        tfidf_tokens: Dict[int, Dict[str, list[float]]],
        tfidf_lemmas: Dict[int, Dict[str, list[float]]],
        tfidf_tokens_folder: str = TASK4_TFIDF_TOKENS,
        tfidf_lemmas_folder: str = TASK4_TFIDF_LEMMAS,
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

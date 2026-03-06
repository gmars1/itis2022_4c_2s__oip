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


class FilesFacade:
    def get_links(self, filename: str = TASK1_TARGET_LIST) -> list[str]:
        """Load links from file"""
        with open(filename) as f:
            links = [line for line in f]
        return links

    # def get_crawled(self):

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

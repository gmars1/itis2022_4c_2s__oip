import os
from typing import Dict, Set

from nltk.tokenize import word_tokenize


def load_allowed_words_file(filename: str, allowed_words: Set[str]):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            allowed_words.add(word)


def load_lemmas_file(filename: str, word_to_lemma: Dict[str, str]):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            splitted = line.split(" ")
            lemma = splitted[0]
            words = splitted[1:]
            for word in words:
                word_to_lemma.setdefault(word, lemma)


def fill_folder_files_into_invert_index(
    foldername: str,
    allowed_words: Set[str],
    words_invert_index: dict[str, Set[int]],
    lemmas_invert_index: dict[str, Set[int]],
    word_to_lemma: Dict[str, str],
):
    for root, _, files in os.walk(foldername):
        for file in files:
            filepath = os.path.join(root, file)
            fill_file_into_invert_index(
                filepath,
                allowed_words,
                words_invert_index,
                lemmas_invert_index,
                word_to_lemma,
            )


def fill_file_into_invert_index(
    filename: str,
    allowed_words: Set[str],
    words_invert_index: dict[str, Set[int]],
    lemmas_invert_index: dict[str, Set[int]],
    word_to_lemma: Dict[str, str],
) -> None:
    """
    Process a single file, extracting tokens and lemmas.
    """
    file_index = int(filename.replace("task1/crawled/", "").replace(".txt", ""))
    with open(filename, encoding="utf-8") as f:
        for line in f:
            for word in word_tokenize(line.strip()):
                word = word.lower()
                if word in allowed_words:
                    words_invert_index.setdefault(word, set()).add(file_index)
                    if word in word_to_lemma.keys():
                        lemma = word_to_lemma[word]
                        lemmas_invert_index.setdefault(lemma, set()).add(file_index)


def main() -> None:
    words_invert_index: Dict[str, Set[int]] = dict()
    allowed_words: Set[str] = set()
    lemmas_invert_index: Dict[str, Set[int]] = dict()
    word_to_lemma: Dict[str, str] = dict()

    print("Loading tokens file...")
    load_allowed_words_file("task2/tokens.txt", allowed_words)

    print("Loading lemmas file...")
    load_lemmas_file("task2/lemmas.txt", word_to_lemma)

    print("Processing...")
    fill_folder_files_into_invert_index(
        "task1/crawled",
        allowed_words,
        words_invert_index,
        lemmas_invert_index,
        word_to_lemma,
    )

    # Write invert index
    with open("task3/invert_index.txt", "w", encoding="utf-8") as f:
        for token, file_indexes in sorted(words_invert_index.items()):
            f.write(f"{token} {' '.join(map(str, sorted(file_indexes)))}\n")
    print(f"invert index filled: {len(words_invert_index)} tokens")
    
    # Write invert index
    with open("task3/lemmas_invert_index.txt", "w", encoding="utf-8") as f:
        for lemma, file_indexes in sorted(lemmas_invert_index.items()):
            f.write(f"{lemma} {' '.join(map(str, sorted(file_indexes)))}\n")
    print(f"invert index filled: {len(lemmas_invert_index)} lemmas")


if __name__ == "__main__":
    main()

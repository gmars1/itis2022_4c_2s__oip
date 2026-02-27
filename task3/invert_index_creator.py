import os
from typing import Dict, Set

from nltk.tokenize import word_tokenize


def load_allowed_words_file(filename: str, allowed_words: Set[str]):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            allowed_words.add(word)


def fill_folder_files_into_invert_index(
    foldername: str, allowed_words: Set[str], words_invert_index: dict[str, Set[int]]
):
    for root, _, files in os.walk(foldername):
        for file in files:
            filepath = os.path.join(root, file)
            fill_file_into_invert_index(filepath, allowed_words, words_invert_index)


def fill_file_into_invert_index(
    filename: str,
    allowed_words: Set[str],
    words_invert_index: dict[str, Set[int]],
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


def main() -> None:
    words_invert_index: Dict[str, Set[int]] = dict()
    allowed_words: Set[str] = set()

    print("Loading tokens file...")
    load_allowed_words_file("task2/tokens.txt", allowed_words)

    print("Processing...")
    fill_folder_files_into_invert_index(
        "task1/crawled", allowed_words, words_invert_index
    )

    # Write invert index
    with open("task3/invert_index.txt", "w", encoding="utf-8") as f:
        for token, file_indexes in sorted(words_invert_index.items()):
            f.write(f"{token} {' '.join(map(str, sorted(file_indexes)))}\n")
    print(f"invert index filled: {len(words_invert_index)} tokens")


if __name__ == "__main__":
    main()

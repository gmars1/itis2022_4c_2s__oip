import os
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, Optional, Set

from nltk.tokenize import word_tokenize

from task2.version_fr import FrProcessor
from task2.version_rus import RusProcessor
from task2.verson_abstarct import LanguageProcessor


class Language(Enum):
    RUS = "rus"
    FR = "fr"


rusProcessor: LanguageProcessor = RusProcessor()
frProcessor: LanguageProcessor = FrProcessor()


@lru_cache(maxsize=10_000)
def detect_language(word: str) -> Optional[Language]:
    """
    Detect the language of a word based on character set.
    Returns Language.RUS if all characters are Cyrillic,
    Language.FR if all characters are Latin,
    otherwise prints "not found" and returns None.
    """

    # Check if all characters are Cyrillic
    if all(("а" <= char.lower() <= "я") or char.lower() == "ё" for char in word):
        return Language.RUS

    if any(ch in "éèêëàâîïôùûüçœæ" for ch in word):
        return Language.FR

    # Check if all characters are Latin
    if all(("a" <= char.lower() <= "z") for char in word):
        return Language.FR

    print(f"cant detirmine lang: {word}")
    return None


def fill_folder_files_into_storages(
    foldername: str, tokens: Set[str], lemmas: Dict[str, Set[str]]
) -> None:
    """
    Recursively process all files in a folder and its subfolders,
    extracting tokens and their lemmas.
    """
    for root, _, files in os.walk(foldername):
        for file in files:
            filepath = os.path.join(root, file)
            fill_file_into_storages(filepath, tokens, lemmas)


def fill_file_into_storages(
    filename: str, tokens: Set[str], lemmas: Dict[str, Set[str]]
) -> None:
    """
    Process a single file, extracting tokens and lemmas.
    """
    lang: Optional[Language]
    word_info: Any

    with open(filename, encoding="utf-8") as f:
        for line in f:
            for word in word_tokenize(line.strip()):
                # Apply common filters
                if not (word := common_filter(word)):
                    continue

                if not (lang := detect_language(word)):
                    continue

                if not (word_info := language_specific_word_info_getter(word, lang)):
                    continue

                # Apply language-specific filter
                if not (word_info := language_specific_filter(word_info, lang)):
                    continue

                # Add to tokens set
                tokens.add(word)

                # Get lemma and add to lemmas dictionary
                if lemma := language_specific_lemmatizer(word_info, lang):
                    lemmas.setdefault(lemma, set()).add(word)


def common_filter(word: str) -> Optional[str]:
    """
    Common preprocessing: keep only alphabetic words and convert to lowercase.
    """
    if not word.isalpha():
        return None
    return word.lower()


def language_specific_word_info_getter(word: str, lang: Language) -> Any:
    """
    Get word info.
    """
    if lang == Language.RUS:
        return rusProcessor.get_word_info(word)
    elif lang == Language.FR:
        return frProcessor.get_word_info(word)
    else:
        return None


def language_specific_filter(word_info: Any, lang: Language) -> Optional[Any]:
    """
    Apply language-specific filtering based on detected language.
    """
    if lang == Language.RUS:
        return rusProcessor.filter(word_info)
    elif lang == Language.FR:
        return frProcessor.filter(word_info)
    else:
        return None


def language_specific_lemmatizer(word_info: Any, lang: Language) -> Optional[Any]:
    """
    Get lemma for a word based on its language.
    """
    if lang == Language.RUS:
        return rusProcessor.get_lemma(word_info)
    elif lang == Language.FR:
        return frProcessor.get_lemma(word_info)
    else:
        return None


def main() -> None:
    tokens: Set[str] = set()
    lemmas: Dict[str, Set[str]] = dict()

    print("Processing...")
    fill_folder_files_into_storages("task1/crawled", tokens, lemmas)

    # print(detect_language.cache_info())
    # Write tokens
    with open("task2/tokens.txt", "w", encoding="utf-8") as f:
        for token in sorted(tokens):
            f.write(token + "\n")
    print(f"Tokens filled: {len(tokens)} tokens")

    # Write lemmas
    with open("task2/lemmas.txt", "w", encoding="utf-8") as f:
        for lemma, words in sorted(lemmas.items()):
            f.write(f"{lemma} {' '.join(sorted(words))}\n")
    print(f"Lemmas filled: {len(lemmas)} lemmas")


if __name__ == "__main__":
    main()

import os
from typing import Dict, Set

import numpy as np

from task3.invert_index_creator import load_allowed_words_file
from task3.search import load_invert_index_file, load_lemmas_file


def process_folder_files(
    foldername: str,
    tokens: Set[str],
    token_to_lemma: Dict[str, str],
    lemma_tokens: Dict[str, Set[str]],
    tfidf_tokens_folder: str,
    tfidf_lemmas_folder: str,
    invert_index: Dict[str, Set[int]],
    amount_of_files_total: int,
) -> None:
    file_index: int = 0
    token_to_idf: Dict[str, float] = dict()
    lemma_to_idf: Dict[str, float] = dict()

    for root, _, files in os.walk(foldername):
        for file in files:
            filepath = os.path.join(root, file)
            process_file(
                filepath,
                tokens,
                token_to_lemma,
                lemma_tokens,
                file_index,
                tfidf_tokens_folder,
                tfidf_lemmas_folder,
                invert_index,
                token_to_idf,
                lemma_to_idf,
                amount_of_files_total,
            )
            file_index += 1


def process_file(
    filename: str,
    tokens: Set[str],
    token_to_lemma: Dict[str, str],
    lemma_tokens: Dict[str, Set[str]],
    file_index: int,
    tfidf_tokens_folder: str,
    tfidf_lemmas_folder: str,
    invert_index: Dict[str, Set[int]],
    token_to_idf: Dict[str, float],
    lemma_to_idf: Dict[str, float],
    amount_of_files_total: int,
) -> None:
    tokens_count = 0
    token_to_count: Dict[str, int] = dict()
    lemma_to_count: Dict[str, int] = dict()

    with open(filename, encoding="utf-8") as f:
        for line in f:
            for word in line.strip().split():  # проходимся по каждому слову в файле
                if word in tokens:
                    tokens_count += 1
                    token_to_count.setdefault(word, 0)
                    token_to_count[word] += 1

                    if word in token_to_lemma:
                        lemma = token_to_lemma[word]  # todo может не быть
                        lemma_to_count.setdefault(lemma, 0)
                        lemma_to_count[lemma] += 1

    tfidf_tokens_file = f"{tfidf_tokens_folder}/{file_index}.txt"  # здесь - idf, tfidf для каждого токена в файле
    tfidf_lemmas_file = f"{tfidf_lemmas_folder}/{file_index}.txt"  # здесь - idf, tfidf для каждой леммы в файле

    os.makedirs(tfidf_tokens_folder, exist_ok=True)
    os.makedirs(tfidf_lemmas_folder, exist_ok=True)

    with open(tfidf_lemmas_file, "w", encoding="utf-8") as f_lemmas:
        for lemma, count in lemma_to_count.items():  # обрабатываем каждую лемму в файле
            lemma_tf = count / tokens_count

            if lemma not in lemma_to_idf:
                tokens = lemma_tokens[lemma]
                doc_indexes = set().union(
                    *(invert_index[token.strip()] for token in tokens)
                )  # объединение всех индексов файло, в которых есть эта лемма
                lemma_to_idf[lemma] = np.log(amount_of_files_total / len(doc_indexes))
            f_lemmas.write(
                f"{lemma} {lemma_to_idf[lemma]} {lemma_tf * lemma_to_idf[lemma]}\n"
            )

    with open(tfidf_tokens_file, "w", encoding="utf-8") as f_tokens:
        for token, count in token_to_count.items():  # обрабатываем каждый токен в файле
            token_tf = count / tokens_count
            if token not in token_to_idf:
                token_to_idf[token] = np.log(
                    amount_of_files_total / len(invert_index[token])
                )
            f_tokens.write(
                f"{token} {token_to_idf[token]} {token_tf * token_to_idf[token]}\n"
            )


def main() -> None:
    allowed_words: Set[str] = set()
    token_to_lemma: Dict[str, str] = dict()  # token -> lemma
    lemma_tokens: Dict[str, Set[str]] = dict()  # lemma -> tokens
    invert_index: Dict[str, Set[int]] = dict()

    print("Loading tokens file...")
    load_allowed_words_file("task2/tokens.txt", allowed_words)

    print("Loading lemmas file...")
    load_lemmas_file("task2/lemmas.txt", token_to_lemma, lemma_tokens)

    # loading from file
    print("Loading invert index file...")
    load_invert_index_file("task3/invert_index.txt", invert_index)

    process_folder_files(
        foldername="task1/crawled",
        tokens=allowed_words,
        token_to_lemma=token_to_lemma,
        lemma_tokens=lemma_tokens,
        tfidf_tokens_folder="task4/tfidf_tokens",
        tfidf_lemmas_folder="task4/tfidf_lemmas",
        invert_index=invert_index,
        amount_of_files_total=109,  # todo
    )


if __name__ == "__main__":
    main()

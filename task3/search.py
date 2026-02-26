from time import sleep
from typing import Dict, Set

from task3.search_helper import get_indexes_of_query_word


def load_invert_index_file(filename: str, invert_index: Dict[str, Set[int]]):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            splitted = line.strip().split(" ")
            word = splitted[0]
            indexes = set(map(int, splitted[1:]))
            invert_index.setdefault(word, indexes)


def load_lemmas_file(
    filename: str, token_to_lemma: Dict[str, str], lemma_tokens: Dict[str, Set[str]]
):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            splitted = line.split(" ")
            lemma = splitted[0]
            words = splitted[1:]
            lemma_tokens[lemma] = set(words)
            for word in words:
                token_to_lemma.setdefault(word, lemma)


def interactive_search(
    user_query: str,
    invert_index: Dict[str, Set[int]],
    token_to_lemma: Dict[str, str],
    lemma_tokens: Dict[str, Set[str]],
) -> str:
    # transform query
    user_query = user_query.lower()

    # split into parts
    splitted = split_user_query(user_query)

    # check query
    if not check_user_query(splitted):
        return "INCORRECT QUERY"

    result = search(splitted, invert_index, token_to_lemma, lemma_tokens)

    if len(result) == 0:
        return "nothing has found"

    # convert to str
    result = ", ".join(list(map(str, sorted(result))))
    return result


def split_user_query(query: str) -> list[str]:
    """Split query into parenthesis, operators and words"""
    query = query.replace("(", " ( ").replace(")", " ) ").replace("!", "! ")
    return query.split(" ")


def check_user_query(splitted: list[str]) -> bool:
    if splitted.count("(") != splitted.count(")"):
        return False
    # if regex: todo
    and_or = [x for x in splitted if x in PRIORITY.keys() and PRIORITY[x] != 3]
    words = [
        x for x in splitted if x not in PRIORITY.keys() and x not in ["(", ")", ""]
    ]
    # print(and_or)
    # print(words)
    if len(words) != len(and_or) + 1:
        return False
    return True


def search(
    splitted: list[str],
    invert_index: Dict[str, Set[int]],
    token_to_lemma: Dict[str, str],
    lemma_tokens: Dict[str, Set[str]],
):
    """Function to search in invert index"""
    # convert to postfix notation
    postfix_query = convert_to_postfix(splitted)
    # eval query
    return eveluate_query(postfix_query, invert_index, token_to_lemma, lemma_tokens)


# bigger - first
PRIORITY = {
    "!": 3,
    "not": 3,
    "не": 3,
    "&": 2,
    "and": 2,
    "и": 2,
    "|": 1,
    "or": 1,
    "или": 1,
}


def convert_to_postfix(splitted: list[str]) -> list[str]:
    res: list[str] = []
    stack: list[str] = []

    for t in splitted:
        # если слово, то добавляем просто в res
        if t not in PRIORITY:
            res.append(t)
        # если операнд, то смотрим на старшинство:
        # если в stack лежит, то что выполняется первее - добавляем в res
        # далее добавляем операнд в stack
        elif t in PRIORITY:
            while stack and stack[-1] in PRIORITY and PRIORITY[stack[-1]] > PRIORITY[t]:
                res.append(stack.pop())
            stack.append(t)
        # если открывающая, то просто добавляем в stack
        elif t == "(":
            stack.append(t)
        # собираем содердимое между скобок в res
        elif t == ")":
            while stack and stack[-1] != "(":
                res.append(stack.pop())
            stack.pop()

    # собираем оставшееся из stack
    while stack:
        res.append(stack.pop())

    return res


def eveluate_query(
    postfix_query: list[str],
    invert_index: Dict[str, Set[int]],
    token_to_lemma: Dict[str, str],
    lemma_tokens: Dict[str, Set[str]],
) -> Set[int]:
    stack = []
    print(f"postfix_query: {postfix_query}")

    # все индексы документов
    all_indexes = set().union(*invert_index.values()) if invert_index else set()

    for token in postfix_query:
        # если просто слово: добавляем в stack
        if token not in PRIORITY.keys():
            stack.append(
                get_indexes_of_query_word(
                    token, invert_index, token_to_lemma, lemma_tokens
                )
            )

        elif PRIORITY[token] == 3:
            # получаем операнд, который надо отсечь
            operand = stack.pop()
            # добавляем в stack, после отсечения
            stack.append(all_indexes - operand)

        else:
            # операции and, or - бинарные: берем 2 операнда
            right = stack.pop()
            left = stack.pop()

            if PRIORITY[token] == 2:
                stack.append(left & right)
            else:
                stack.append(left | right)

    return stack[0] if stack else set()


def main() -> None:
    invert_index: Dict[str, Set[int]] = dict()

    token_to_lemma: Dict[str, str] = dict()
    lemma_tokens: Dict[str, Set[str]] = dict()

    # loading from file
    print("Loading invert index file...")
    load_invert_index_file("task3/invert_index.txt", invert_index)

    print("Loading lemmas file...")
    load_lemmas_file("task2/lemmas.txt", token_to_lemma, lemma_tokens)

    # REPL cicle todo
    closed = False
    while not closed:
        print("==================")
        inp: str = input("(enter 'quit' to leave):\nENTER QUERY: ")
        if inp == "quit":
            closed = True
            break
        # perform search
        result = interactive_search(inp, invert_index, token_to_lemma, lemma_tokens)
        print(
            f"\nRESULT FOR '{inp}':\n{result}\n====================================\n"
        )
        sleep(1)


if __name__ == "__main__":
    main()

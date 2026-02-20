import inspect
from collections import namedtuple
from functools import lru_cache
from typing import Any, Optional

# compatibility fix for Python ≥3.11
if not hasattr(inspect, "getargspec"):
    ArgSpec = namedtuple("ArgSpec", "args varargs keywords defaults")

    def getargspec(func):
        spec = inspect.getfullargspec(func)
        return ArgSpec(spec.args, spec.varargs, spec.varkw, spec.defaults)

    inspect.getargspec = getargspec

import pymorphy2

from task2.verson_abstarct import LanguageProcessor


class RusProcessor(LanguageProcessor):
    # Initialize morphological analyzer
    morph = pymorphy2.MorphAnalyzer(lang="ru")

    # Parts of speech to filter out (like prepositions, conjunctions)
    BAD_POS = {
        "PREP",  # preposition
        "CONJ",  # conjunction
        # "PRCL",  # particle (commented out)
        # "INTJ",  # interjection (commented out)
    }

    NOT_GOOD = {"LATN", "PNCT", "NUMB", "intg", "real", "ROMN", "UNKN"}

    @lru_cache(maxsize=10_000)
    def get_word_info(self, word: str) -> Any:
        """
        Returns the pymorphy2 Parse object for a single word or None
        Uses caching to improve performance for repeated words.
        """
        p = self.morph.parse(word)[0]
        if p.tag.POS is None:
            print(f"rus analyzer could not analyze word: {word}")
            return None
        if p.tag.POS in self.NOT_GOOD:
            print(f"rus analyzer: not a rus word: {word}")
            return None
        return p

    def filter(self, word_info: Any) -> Optional[Any]:
        """
        Filters out unwanted Russian words based on part of speech.
        Returns None if the word's POS is in BAD_POS, otherwise returns the word_info (Parse object).
        """
        if word_info.tag.POS in self.BAD_POS:
            return None
        return word_info

    def get_lemma(self, word_info: Any) -> Optional[Any]:
        """
        Returns the normalized lemma (normal_form) of a Russian word.
        """
        return word_info.normal_form

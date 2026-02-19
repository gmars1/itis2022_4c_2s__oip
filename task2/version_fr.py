from functools import lru_cache

# from functools import lru_cache
from typing import Any, Optional

import spacy
import spacy.cli
from spacy.language import Language

from task2.verson_abstarct import LanguageProcessor


class FrProcessor(LanguageProcessor):
    # Parts of speech to filter out
    BAD_POS = {
        "ADP",  # preposition
        "CCONJ",  # coordinating conjunction
        "SCONJ",  # subordinating conjunction
    }

    # Lazy loading of the French model
    @lru_cache(maxsize=1)
    def get_nlp(self) -> Language:
        """
        Load and return the French spaCy model.
        Uses lru_cache to load only once.
        """
        # загружаем французскую модель
        return spacy.load("fr_core_news_sm")

    def get_word_info(self, word: str) -> Optional[Any]:
        """
        Returns a spaCy Token object for a single word.
        """
        nlp = self.get_nlp()
        doc = nlp(word)
        if len(doc) > 0:
            return doc[0]
        print(f"Failed to parse word: {word}")
        return None

    def filter(self, word_info: Any) -> Optional[Any]:
        """
        Filters out unwanted French words based on part of speech.
        Returns None if the word's POS is in BAD_POS, otherwise returns the word.
        """
        if word_info.pos_ in self.BAD_POS:
            return None
        return word_info

    def get_lemma(self, word_info: Any) -> Optional[Any]:
        """
        Returns the lemma of a French word.
        """
        if word_info:
            return word_info.lemma_
        return None

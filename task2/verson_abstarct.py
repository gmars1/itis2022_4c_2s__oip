# from abc import ABC, abstractmethod
from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class LanguageProcessor(Protocol):
    """Protocol defining the interface for language processors."""

    def get_word_info(self, word: str) -> Any:
        """
        Get word info.
        """
        ...

    def filter(self, word_info: Any) -> Optional[Any]:
        """Filter a word based on language-specific criteria."""
        ...

    def get_lemma(self, word_info: Any) -> Optional[Any]:
        """Return the lemma of a word."""
        ...

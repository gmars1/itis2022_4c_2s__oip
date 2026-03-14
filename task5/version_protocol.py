from typing import Protocol, runtime_checkable


@runtime_checkable
class Searcher(Protocol):
    """Protocol defining the interface for docs searcher."""

    def get_docs(self, query: str) -> list[tuple[int, float]]:
        """
        Get docs.
        """
        ...

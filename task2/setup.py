import ssl

import nltk
import spacy.cli


def setup_resources():
    """Скачивает все необходимые ресурсы для проекта"""
    print("Setting up NLP resources...")

    # Для NLTK
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    print("Downloading NLTK data...")
    nltk.download("punkt_tab")
    nltk.download("punkt")

    # Для spaCy
    print("Downloading spaCy French model...")
    spacy.cli.download("fr_core_news_sm")

    print("All resources downloaded!")


if __name__ == "__main__":
    setup_resources()

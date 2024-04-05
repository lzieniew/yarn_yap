import nltk

nltk.download("punkt")
from nltk.tokenize import sent_tokenize


def sanitize(text: str) -> list[str]:
    sentences = sent_tokenize(text)
    return sentences

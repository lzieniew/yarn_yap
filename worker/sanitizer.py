import nltk

nltk.download("punkt")
from nltk.tokenize import sent_tokenize
from langdetect import detect


def detect_whole_text_language(text: str):
    return detect(text)


def sanitize(text: str) -> list[str]:
    sentences = sent_tokenize(text)
    return sentences

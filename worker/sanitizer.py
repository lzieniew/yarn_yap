from beanie.odm.fields import PydanticObjectId
from langdetect.lang_detect_exception import LangDetectException
import nltk

from shared_components.models import Sentence
from shared_components.utils import run_async

nltk.download("punkt")
from nltk.tokenize import sent_tokenize
from langdetect import detect


def detect_whole_text_language(text: str):
    return detect(text)


def sanitize(text: str) -> list[PydanticObjectId]:
    sentences = []
    text_sentences = sent_tokenize(text)
    for text_sentence in text_sentences:
        try:
            language = detect(text_sentence)
        except LangDetectException:
            # if langdetect cant recognize language it means the sentence doesn't have any worth generating words, skipping
            continue
        sentence = Sentence(text=text_sentence, language=language, generated=False)
        run_async(sentence.create())
        sentences.append(sentence)
    sentences_ids = [sentence.id for sentence in sentences]
    return sentences_ids

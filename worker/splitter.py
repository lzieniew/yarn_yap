import textwrap
from beanie.odm.fields import PydanticObjectId
from langdetect.lang_detect_exception import LangDetectException
import nltk
from shared_components.config import get_max_sentence_length

from shared_components.models import Sentence
from shared_components.utils import run_async

nltk.download("punkt")
from nltk.tokenize import sent_tokenize
from langdetect import detect


def detect_whole_text_language(text: str):
    return detect(text)


def create_sentence(sentence_text: str, index: int):
    try:
        language = detect(sentence_text)
    except LangDetectException:
        # if langdetect cant recognize language it means the sentence doesn't have any worth generating words, skipping
        return
    sentence = Sentence(
        text=sentence_text,
        language=language,
        generated=False,
        sentence_number=index,
    )
    run_async(sentence.create())
    return sentence


def split_long_sentence(sentence: str) -> list[str]:
    max_length = get_max_sentence_length()
    return textwrap.wrap(sentence, width=max_length)


def split_into_sentences(text: str) -> list[Sentence]:
    max_length = get_max_sentence_length()
    sentences = []
    text_sentences = sent_tokenize(text)
    counter = 0
    for sentence_text in text_sentences:
        if len(sentence_text) > max_length:
            sub_sentences = split_long_sentence(sentence_text)
            for sub_sentence in sub_sentences:
                sentence = create_sentence(sub_sentence, counter)
                sentences.append(sentence)
                counter += 1
        else:
            sentence = create_sentence(sentence_text, counter)
            if sentence:
                sentences.append(sentence)
                counter += 1
    return sentences

import nltk
from langdetect import detect

from worker.tts_adapter import send_tts_request

nltk.download("punkt")

from nltk.tokenize import sent_tokenize


def generate(text: str, id: str):
    print(f"Generating voice for text: {text}")
    sentences = sent_tokenize(text)
    segments = []
    for sentence in sentences:
        language = detect(sentence)
        segments.append(send_tts_request(sentence, language=language))
    combined = sum(segments)
    output_filename = f"/app/{id}.wav"
    combined.export(output_filename, format="wav")
    return output_filename

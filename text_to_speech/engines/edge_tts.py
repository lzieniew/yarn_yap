import edge_tts


import os

import torch
from shared_components.utils import run_async


language_to_voice = {"en": "en-GB-SoniaNeural", "pl": "pl-PL-MarekNeural"}


def initialize():
    pass


def ready(tts) -> bool:
    return True


def generate(text: str, language: str, tts) -> str:
    file_path = "/app/text_to_speech/generated_files/output.wav"
    voice = language_to_voice[language]
    communicate = edge_tts.Communicate(text, voice)
    run_async(communicate.save(file_path))
    return file_path


def get_supported_languages() -> list[str]:
    return {"supported_languages": list(language_to_voice.keys())}

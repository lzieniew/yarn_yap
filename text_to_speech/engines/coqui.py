import os

import torch
from TTS.api import TTS


def initialize():
    os.environ["COQUI_TOS_AGREED"] = "1"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


def ready(tts: TTS):
    return tts is not None


def generate(text: str, language: str, tts: TTS):
    file_path = "/app/text_to_speech/generated_files/output.wav"
    tts.tts_to_file(
        text=text,
        speaker_wav="/app/text_to_speech/voices/bezi.wav",
        language=language,
        file_path=file_path,
    )
    return file_path


def get_supported_languages():
    return {
        "supported_languages": [
            "en",
            "es",
            "fr",
            "de",
            "it",
            "pt",
            "pl",
            "tr",
            "ru",
            "nl",
            "nl",
            "cs",
            "ar",
            "zh-cn",
            "ja",
            "hu",
            "ko",
            "hi",
        ]
    }

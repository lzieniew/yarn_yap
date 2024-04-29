import os

import torch
from TTS.api import TTS

from shared_components.enums import GenerationMethod


generation_method = None


def initialize():
    global generation_method
    os.environ["COQUI_TOS_AGREED"] = "1"
    cude_available = torch.cuda.is_available()
    generation_method = GenerationMethod.GPU if cude_available else GenerationMethod.CPU
    device = "cuda" if cude_available else "cpu"
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


def ready(tts: TTS):
    return tts is not None


def generate(text: str, language: str, tts: TTS, file_path: str):
    tts.tts_to_file(
        text=text,
        speaker_wav="/app/text_to_speech/voices/female.wav",
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


def get_generation_method():
    global generation_method
    return generation_method

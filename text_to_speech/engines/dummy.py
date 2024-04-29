import shutil
from TTS.api import TTS

from shared_components.enums import GenerationMethod


def initialize():
    pass


def ready(tts: TTS):
    return True


def generate(text: str, language: str, tts: TTS, file_path: str):
    source_path = "/app/text_to_speech/voices/bezi.wav"

    try:
        shutil.copy2(source_path, file_path)
    except Exception as ex:
        print(ex)
    return file_path


def get_supported_languages():
    return {
        "supported_languages": [
            "en",
            "pl",
        ]
    }


def get_generation_method():
    return GenerationMethod.EXTERNAL_SERVICE

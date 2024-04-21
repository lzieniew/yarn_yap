import asyncio
from tempfile import NamedTemporaryFile
import threading
import edge_tts
from pydub.audio_segment import AudioSegment


language_to_voice = {"en": "en-GB-SoniaNeural", "pl": "pl-PL-MarekNeural"}


def initialize():
    pass


def ready(tts) -> bool:
    return True


def generate(text: str, language: str, tts, file_path: str) -> str:
    voice = language_to_voice[language]
    communicate = edge_tts.Communicate(text, voice)

    # Using NamedTemporaryFile as a context manager to handle the temp mp3 file
    with NamedTemporaryFile(suffix=".mp3", delete=True) as temp_mp3_file:
        mp3_file_path = temp_mp3_file.name
        communicate.sync_save(mp3_file_path)

        try:
            # Reading the temporary mp3 file
            audio = AudioSegment.from_mp3(mp3_file_path)
            # Exporting to desired location and format
            audio.export(file_path, format="wav")
        except Exception as e:
            print(f"Error converting MP3 to WAV: {str(e)}")

    # The temp_mp3_file is automatically deleted upon exiting the with block
    return file_path


def get_supported_languages() -> list[str]:
    return {"supported_languages": list(language_to_voice.keys())}

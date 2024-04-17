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

    done_event = threading.Event()

    # Using NamedTemporaryFile as a context manager to handle the temp mp3 file
    with NamedTemporaryFile(suffix=".mp3", delete=True) as temp_mp3_file:
        mp3_file_path = temp_mp3_file.name

        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            async def async_task():
                # Save output to the temporary mp3 file
                await communicate.save(mp3_file_path)
                # Signal that the task is done
                done_event.set()

            loop.run_until_complete(async_task())
            loop.close()

        thread = threading.Thread(target=run_in_thread)
        thread.start()
        done_event.wait()
        thread.join()

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

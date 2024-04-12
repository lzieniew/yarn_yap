import asyncio
import threading
import edge_tts


language_to_voice = {"en": "en-GB-SoniaNeural", "pl": "pl-PL-MarekNeural"}


def initialize():
    pass


def ready(tts) -> bool:
    return True


def generate(text: str, language: str, tts) -> str:
    file_path = "/app/text_to_speech/generated_files/output.wav"
    voice = language_to_voice[language]
    communicate = edge_tts.Communicate(text, voice)

    done_event = threading.Event()

    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def async_task():
            # Your async operation
            await communicate.save(file_path)
            # Signal that the task is done
            done_event.set()

        loop.run_until_complete(async_task())
        loop.close()

    thread = threading.Thread(target=run_in_thread)
    thread.start()
    done_event.wait()
    thread.join()

    return file_path


def get_supported_languages() -> list[str]:
    return {"supported_languages": list(language_to_voice.keys())}

import requests
import io
from pydub import AudioSegment


BASE_TTS_URL = "http://text_to_speech:8000"


class LanguageNotSupportedException(Exception):
    pass


def check_server_ready() -> bool:
    try:
        return requests.get(f"{BASE_TTS_URL}/ready").json()["ready"]
    except requests.exceptions.ConnectionError:
        return False


def get_coqui_supported_languages() -> list[str]:
    response = requests.get(f"{BASE_TTS_URL}/languages")
    return response.json()["supported_languages"]


def send_coqui_tts_request(text: str, language: str, fallback_language: str):
    supported_languages = get_coqui_supported_languages()
    if language not in supported_languages:
        if fallback_language not in supported_languages:
            print(
                f"ERROR, neither {language} nor {fallback_language} are in languages supported by xtts2!"
            )
            print(f"The list of supported languages is {supported_languages}")
            raise LanguageNotSupportedException(
                f"Neither {language} nor {fallback_language} are supported"
            )
        else:
            # using fallback language
            print(f"WARNING, {language} not supported, using {fallback_language}")
            language = fallback_language
    payload = {"text": text, "language": language}
    headers = {"Content-Type": "application/json"}
    url = f"{BASE_TTS_URL}/tts"
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return AudioSegment.from_file(io.BytesIO(response.content), format="wav")
    else:
        print(f"ERROR, response {response.status_code}, {response.content}")


# interface - below 3 methods should be implemented for every other tts server


def send_tts_request(text, language, fallback_language):
    return send_coqui_tts_request(text, language, fallback_language)


def check_if_tts_active() -> bool:
    return check_server_ready()


def get_supported_languages() -> list[str]:
    return get_coqui_supported_languages()

import requests
import io
from pydub import AudioSegment


TTS_URL = "http://text_to_speech:8000/tts/"


def send_coqui_tts_request(text: str, language: str):
    payload = {"text": text, "language": language}
    headers = {"Content-Type": "application/json"}
    response = requests.post(TTS_URL, json=payload, headers=headers)
    return AudioSegment.from_file(io.BytesIO(response.content), format="wav")


def send_tts_request(text, language):
    return send_coqui_tts_request(text, language)

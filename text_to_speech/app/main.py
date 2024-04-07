from contextlib import asynccontextmanager
import os
from time import time
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse
import torch
from TTS.api import TTS
from text_to_speech.app.enums import Language


tts = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global tts
    start_time = time()
    os.environ["COQUI_TOS_AGREED"] = "1"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    print(f"Initialization done! It took {time() - start_time}")
    yield


app = FastAPI(lifespan=lifespan)


def run_generation(text: str, language: str) -> str:
    start_time = time()
    file_path = "/app/text_to_speech/generated_files/output.wav"
    tts.tts_to_file(
        text=text,
        speaker_wav="/app/text_to_speech/voices/dragan.wav",
        language=language,
        file_path=file_path,
    )
    print(f"Whole generation of text of length {len(text)} took {time() - start_time}")
    return file_path


@app.get("/ready")
async def readiness_check():
    return {"ready": tts is not None}


@app.get("/languages")
async def supported_languages():
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


@app.post("/tts/")
async def generate_audio(
    text: str = Body(..., example="Text to generate by model"),
    language: str = Body(..., example="en"),
):
    print(
        f"Starting generation for text with {len(text)} characters, language {language}, text: {text}"
    )
    try:
        path_to_audio_file = run_generation(text, language)
        return FileResponse(
            path=path_to_audio_file, media_type="audio/wav", filename="speech.wav"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

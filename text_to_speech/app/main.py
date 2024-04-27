from contextlib import asynccontextmanager
from time import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from shared_components.config import get_tts_engine
import importlib
from tempfile import NamedTemporaryFile

tts_module = importlib.import_module(f"text_to_speech.engines.{get_tts_engine()}")


tts = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global tts
    start_time = time()
    tts = tts_module.initialize()
    print(f"Initialization done! It took {time() - start_time}")
    yield


app = FastAPI(lifespan=lifespan)


def run_generation(text: str, language: str, file_path: str) -> str:
    start_time = time()
    tts_module.generate(text, language, tts, file_path)
    print(f"Whole generation of text of length {len(text)} took {time() - start_time}")


@app.get("/ready")
async def readiness_check():
    return {"ready": tts_module.ready(tts)}


@app.get("/languages")
async def supported_languages():
    return tts_module.get_supported_languages()


@app.get("/tts")
async def generate_audio(
    text: str = "Text to generate by model",
    language: str = "en",
):
    print(
        f"Starting generation for text with {len(text)} characters, language {language}, text: {text}"
    )
    try:
        with NamedTemporaryFile(delete=False) as temp_file:
            file_path = temp_file.name
            run_generation(text, language, file_path)
            with open(file_path, "rb") as f:
                audio_data = f.read()
            return Response(
                content=audio_data,
                media_type="audio/wav",
                headers={"Content-Disposition": "inline;filename=speech.wav"},
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from contextlib import asynccontextmanager
from time import time
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from shared_components.config import get_tts_engine
import importlib

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


def run_generation(text: str, language: str, background_tasks: BackgroundTasks) -> str:
    start_time = time()
    file_path = tts_module.generate(text, language, tts)
    print(f"Whole generation of text of length {len(text)} took {time() - start_time}")
    return file_path


@app.get("/ready")
async def readiness_check():
    return {"ready": tts_module.ready(tts)}


@app.get("/languages")
async def supported_languages():
    return tts_module.get_supported_languages()


@app.post("/tts/")
async def generate_audio(
    background_tasks: BackgroundTasks,
    text: str = Body(..., example="Text to generate by model"),
    language: str = Body(..., example="en"),
):
    print(
        f"Starting generation for text with {len(text)} characters, language {language}, text: {text}"
    )
    try:
        path_to_audio_file = run_generation(text, language, background_tasks)
        return FileResponse(
            path=path_to_audio_file, media_type="audio/wav", filename="speech.wav"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

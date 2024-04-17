from contextlib import asynccontextmanager
from time import time
from fastapi import Body, FastAPI, HTTPException
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


@app.post("/tts/")
async def generate_audio(
    text: str = Body(..., example="Text to generate by model"),
    language: str = Body(..., example="en"),
):
    print(
        f"Starting generation for text with {len(text)} characters, language {language}, text: {text}"
    )
    try:
        with NamedTemporaryFile(delete=True) as temp_file:
            file_path = temp_file.name
            run_generation(text, language, file_path)
            with open(file_path, "rb") as f:
                audio_data = f.read()
            # os.unlink(file_path)  # Ensure the temporary file is deleted.
            return Response(
                content=audio_data,
                media_type="audio/wav",
                headers={"Content-Disposition": "attachment;filename=speech.wav"},
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

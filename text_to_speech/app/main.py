from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse
import torch
from TTS.api import TTS
from text_to_speech.app.enums import Language


app = FastAPI()


def run_generation(text: str, language: str) -> str:
    file_path = "/app/text_to_speech/generated_files/output.wav"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    tts.tts_to_file(
        text=text,
        speaker_wav="/app/text_to_speech/voices/female.wav",
        language=language,
        file_path=file_path,
    )
    return file_path


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/tts/")
async def generate_audio():
    text: str = Body(..., example="Text to generate by model")
    language: Language = Body(..., example=Language.en)
    try:
        path_to_audio_file = run_generation(text, language)
        return FileResponse(
            path=path_to_audio_file, media_type="audio/mpeg", filename="speech.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

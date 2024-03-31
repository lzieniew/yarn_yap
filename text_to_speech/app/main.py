from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/tts/")
async def generate_audio(text: str):
    try:
        # Assuming text_to_speech returns the path of the generated audio file
        path_to_audio_file = "/app/generated_files/test.wav"
        return FileResponse(
            path=path_to_audio_file, media_type="audio/mpeg", filename="speech.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


from scipy.io.wavfile import write
import text_to_speech.StyleTTS2.ljinference
import test_to_speech.StyleTTS2.torch


app = FastAPI()


def run_generation():
    text = "Recent advances in large language models have brought immense value to the world, with their superior capabilities stemming from the massive number of parameters they utilize."

    # text = """ StyleTTS 2 is a text-to-speech model that leverages style diffusion and adversarial training with large speech language models to achieve human-level text-to-speech synthesis. """
    noise = torch.randn(1, 1, 256).to("cuda" if torch.cuda.is_available() else "cpu")
    wav = ljinference.inference(text, noise, diffusion_steps=4, embedding_scale=1)
    write("result.wav", 24000, wav)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/tts/")
async def generate_audio(text: str):
    try:
        run_generation()
        # Assuming text_to_speech returns the path of the generated audio file
        path_to_audio_file = "/app/text_to_speech/generated_files/test.wav"
        return FileResponse(
            path=path_to_audio_file, media_type="audio/mpeg", filename="speech.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

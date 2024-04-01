from scipy.io.wavfile import write
import text_to_speech.StyleTTS.ljinference
import test_to_speech.StyleTTS.torch

text = "Recent advances in large language models have brought immense value to the world, with their superior capabilities stemming from the massive number of parameters they utilize."

# text = """ StyleTTS 2 is a text-to-speech model that leverages style diffusion and adversarial training with large speech language models to achieve human-level text-to-speech synthesis. """
noise = torch.randn(1, 1, 256).to("cuda" if torch.cuda.is_available() else "cpu")
wav = ljinference.inference(text, noise, diffusion_steps=4, embedding_scale=1)
write("result.wav", 24000, wav)

import base64
import time
from beanie.odm.fields import WriteRules
from bson import ObjectId

from shared_components.models import AudioData, Job, Sentence
from shared_components.utils import run_async

from worker.tts_adapter import (
    LanguageNotSupportedException,
    send_generation_method_request,
    send_tts_request,
)


def update_progress(processed_sentences: int, all_sentences: int, job: Job):
    job.progress_percent = f"{(processed_sentences / all_sentences) * 100.0:.2f}"
    run_async(job.replace())


def generate(job: Job):
    run_async(job.fetch_all_links())
    sentences = job.sentences
    sentences_count = len(sentences)
    processed_sentences_count = 0
    print(f"Generating text for {sentences_count} sentences")
    for sentence in sentences:
        print(
            f"Starting generating sentence {sentence}, language {sentence.language}, fallback language {job.language}"
        )
        try:
            start_time = time.time()
            audio_data = send_tts_request(
                sentence.text,
                language=sentence.language,
                fallback_language=job.language,
            )
            generation_method = send_generation_method_request()
            sentence.generation_time = int(time.time() - start_time)
            audio_bytes = audio_data.export(format="wav").read()
            audio_data_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            audio_data = AudioData(data=audio_data_base64)
            run_async(audio_data.create())
            sentence.audio_data = audio_data
            sentence.generated = True
            sentence.generation_method = generation_method
            run_async(sentence.replace())
        except LanguageNotSupportedException as ex:
            # neither sentence language or whole text language are supported, skipping
            print(f"Error {ex}")
            continue
        processed_sentences_count += 1
        update_progress(
            processed_sentences=processed_sentences_count,
            all_sentences=sentences_count,
            job=job,
        )
    return sentences

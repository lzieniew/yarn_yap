from langdetect import detect
from shared_components.models import Job

from worker.tts_adapter import send_tts_request


def update_progress(processed_sentences: int, all_sentences: int, job: Job):
    job.progress_percent = (processed_sentences / all_sentences) * 100.0
    job.save()


def generate(sentences: list[str], job: Job):
    sentences_count = len(sentences)
    processed_sentences_count = 0
    print(f"Generating text for {sentences_count} sentences")
    segments = []
    for sentence in sentences:
        language = detect(sentence)
        segments.append(send_tts_request(sentence, language=language))
        processed_sentences_count += 1
        update_progress(
            processed_sentences=processed_sentences_count,
            all_sentences=sentences_count,
            job=job,
        )

    combined = sum(segments)
    output_filename = f"/app/{id}.wav"
    combined.export(output_filename, format="wav")
    return output_filename

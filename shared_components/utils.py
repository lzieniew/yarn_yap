import asyncio
import concurrent.futures


def run_async(coroutine):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)


def remove_audio_content_repr_from_sentences_in_job(job):
    for sentence in job.get_sorted_sentences():
        sentence.audio_data = (
            f"Audio data of length {len(sentence.audio_data)}"
            if sentence.audio_data
            else "empty"
        )


def remove_audio_content_repr_from_sentence(sentence):
    sentence.audio_data = (
        f"Audio data of length {len(sentence.audio_data)}"
        if sentence.audio_data
        else "empty"
    )

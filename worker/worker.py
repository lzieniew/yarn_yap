import time
from shared_components import Job
from shared_components.db_init import init_db
from shared_components.enums import JobStatus
from worker.fetcher import fetch_url
from worker.generator import generate
from worker.sanitizer import detect_whole_text_language, sanitize
from shared_components.utils import run_async
from worker.tts_adapter import check_if_tts_active, get_supported_languages


def process_job(job: Job):
    print(job.status)
    if job.status == JobStatus.GENERATED:
        return

    if job.status == JobStatus.CREATED:
        job.raw_text = fetch_url(job.url)
        job.status = JobStatus.FETCHED
        run_async(job.save())

    if job.status == JobStatus.FETCHED:
        job.language = detect_whole_text_language(job.raw_text)
        job.sanitized_text = sanitize(job.raw_text)
        job.status = JobStatus.SANITIZED
        run_async(job.save())

    if job.status == JobStatus.SANITIZED:
        if check_if_tts_active():
            start_time = time.time()  # Record start time
            get_supported_languages()
            generate(job)
            elapsed_time = time.time() - start_time
            job.generation_time = int(elapsed_time)
            job.status = JobStatus.GENERATED
            run_async(job.save())
        else:
            print("TTS server not active!")


def process_jobs():
    jobs = run_async(Job.find(Job.status != JobStatus.GENERATED).to_list())
    print(f"There are {len(jobs)} jobs to process")
    for job in jobs:
        process_job(job)


def main():
    run_async(init_db())
    while True:
        process_jobs()
        time.sleep(5)


if __name__ == "__main__":
    main()

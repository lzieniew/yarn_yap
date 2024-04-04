import time
import nltk
from shared_components import Job
from shared_components.db_init import init_db
from shared_components.enums import JobStatus
from worker.fetcher import fetch_url
from worker.generator import generate
from worker.sanitizer import sanitize
from shared_components.utils import run_async


def process_job(job: Job):
    print("Im a jooooooooob")
    print(job.status)
    if job.status == JobStatus.GENERATED:
        return

    if job.status == JobStatus.CREATED:
        job.raw_text = fetch_url(job.url)
        job.status = JobStatus.FETCHED
        run_async(job.save())

    if job.status == JobStatus.FETCHED:
        job.sanitized_text = sanitize(job.raw_text)
        job.status = JobStatus.SANITIZED
        run_async(job.save())

    if job.status == JobStatus.SANITIZED:
        job.audio_path = generate(job.sanitized_text, str(job.id))
        job.status = JobStatus.GENERATED
        run_async(job.save())


def process_jobs():
    jobs = run_async(Job.find(Job.status != JobStatus.GENERATED).to_list())
    print(f"There is {len(jobs)} jobs to process")
    for job in jobs:
        process_job(job)


def main():
    run_async(init_db())
    while True:
        process_jobs()
        time.sleep(5)


if __name__ == "__main__":
    main()

import time
from datetime import datetime
from pymongo import MongoClient
from shared_components import Job
from shared_components.enums import JobStatus
from fetcher import fetch_url
from generator import generate
from sanitizer import sanitize

# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017")
db = client["mydatabase"]
collection = db["jobs"]


def process_job(job: Job):
    if job.status == JobStatus.GENERATED:
        return

    if job.status == JobStatus.CREATED:
        job.raw_text = fetch_url(job.url)
        job.status = JobStatus.FETCHED
        job.save(collection=collection)

    if job.status == JobStatus.FETCHED:
        job.sanitized_text = sanitize(job.raw_text)
        job.status = JobStatus.SANITIZED
        job.save(collection=collection)

    if job.status == JobStatus.SANITIZED:
        job.audio_path = generate(job.sanitized_text)
        job.status = JobStatus.GENERATED
        job.save(collection=collection)


def process_jobs():
    jobs = list(collection.find())
    print(f"There is {len(jobs)} jobs in mongo")
    for job_dict in jobs:
        job = Job(**job_dict)
        process_job(job)


while True:
    #process_jobs()
    time.sleep(1)

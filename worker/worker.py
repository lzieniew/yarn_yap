import time
from datetime import datetime
from pymongo import MongoClient
from shared_components import Job

# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017")
db = client["mydatabase"]
collection = db["jobs"]


def process_jobs():
    jobs = list(collection.find())


    print(f"There is {len(jobs)} jobs in mongo")
    print(f"First job has status {jobs[0]['status']}")
    for job_dict in jobs:
        job = Job(**job_dict)
        print(job)

        pass



while True:
    process_jobs()
    time.sleep(5)

from typing import List
from app.models import Job
from fastapi import FastAPI
from pymongo import MongoClient


app = FastAPI()


# Connect to your MongoDB database
client = MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
collection = db["jobs"]


@app.post("/jobs/")
async def create_job(job: Job):
    job_dict = job.model_dump()
    result = collection.insert_one(job_dict)
    return {"_id": str(result.inserted_id)}


@app.get("/jobs/", response_model=List[Job])
async def list_jobs():
    jobs = list(collection.find({}))
    for job in jobs:
        job["_id"] = str(
            job["_id"]
        )  # Convert ObjectId to string for JSON serializability
    return jobs

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

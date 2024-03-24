from typing import List
from bson import ObjectId
from shared import JobStatus
from shared import Job, JobCreate
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient


app = FastAPI()


# Connect to your MongoDB database
client = MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
collection = db["jobs"]


@app.post("/jobs/")
async def create_job(job_create: JobCreate):
    job_data = job_create.model_dump()
    job = Job(**job_data, sanitized_text=None, status=JobStatus.CREATED)

    job_dict = job.model_dump()
    result = collection.insert_one(job_dict)
    return {"_id": str(result.inserted_id)}


@app.get("/jobs/", response_model=List[Job])
async def list_jobs():
    jobs = []
    for job_dict in collection.find({}):
        job_dict["id"] = str(job_dict.pop("_id"))
        job = Job.model_validate(job_dict)
        jobs.append(job)
    return jobs


@app.get("/jobs/{job_id}", response_model=Job)
async def get_job(job_id: str):
    try:
        job_dict = collection.find_one({"_id": ObjectId(job_id)})
        if job_dict:
            job_dict["id"] = str(job_dict.pop("_id"))
            job = Job.model_validate(job_dict)
            return job
        else:
            raise HTTPException(status_code=404, detail="Job not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

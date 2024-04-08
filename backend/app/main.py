from contextlib import asynccontextmanager
import os
from typing import List
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
from shared_components import JobStatus

from shared_components import Job, JobCreate
from shared_components.db_init import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/jobs/")
async def create_job(job_create: JobCreate):
    job_data = job_create.model_dump()
    status = JobStatus.CREATED if job_data["url"] else JobStatus.FETCHED
    job = Job(**job_data, sanitized_text=None, status=status)

    result = await job.create()
    return {"id": str(result.id)}


@app.get("/jobs/", response_model=List[Job])
async def list_jobs():
    all_jobs = await Job.find().to_list()
    return {"number_of_jobs": len(all_jobs), "jobs": all_jobs}


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id))

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job": job.model_dump()}


@app.get("/jobs/{job_id}/audio")
async def get_job_audio(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id))

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    audio_path = job.audio_path

    if not audio_path or not os.path.isfile(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(audio_path)


@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    Job.delete(Job.id == ObjectId(job_id))


@app.delete("/jobs")
async def delete_all_jobs():
    # Delete all jobs from the database
    await Job.delete_all()
    return {"message": "All jobs have been deleted."}

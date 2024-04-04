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
    return await Job.find().to_list()


@app.delete("/jobs")
async def delete_all_jobs():
    # Delete all jobs from the database
    await Job.delete_all()
    return {"message": "All jobs have been deleted."}


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


@app.get("/jobs/{job_id}/audio")
async def get_job_audio(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id))

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    audio_path = job.audio_path

    if not audio_path or not os.path.isfile(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(audio_path)

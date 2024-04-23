from contextlib import asynccontextmanager
from io import BytesIO
import base64
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
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


from fastapi.encoders import jsonable_encoder


@app.get("/jobs/")
async def list_jobs():
    all_jobs = await Job.find().to_list()
    encoded_jobs = jsonable_encoder(all_jobs)
    return {"number_of_jobs": len(all_jobs), "jobs": encoded_jobs}


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

    combined_audio_data = bytearray()
    for sentence in job.sanitized_text:
        if sentence.audio_data:
            audio_data = base64.b64decode(sentence.audio_data)
            combined_audio_data.extend(audio_data)

    if len(combined_audio_data) == 0:
        raise HTTPException(status_code=404, detail="No audio data available")

    # Create a BytesIO object from the combined audio data
    audio_bytes = BytesIO(combined_audio_data)

    # Return the audio data as a response
    return StreamingResponse(content=audio_bytes, media_type="audio/wav")


@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    return Job.delete(Job.id == ObjectId(job_id))


@app.delete("/jobs")
async def delete_all_jobs():
    # Delete all jobs from the database
    await Job.delete_all()
    return {"message": "All jobs have been deleted."}

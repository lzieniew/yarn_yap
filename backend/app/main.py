from time import time
from contextlib import asynccontextmanager
from io import BytesIO
import base64
from beanie.odm.documents import MergeStrategy
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from pydub.audio_segment import AudioSegment
from starlette.responses import StreamingResponse
import wave

from shared_components import JobStatus
from shared_components import Job, JobCreate
from shared_components.db_init import init_db
from shared_components.models import Sentence
from shared_components.utils import (
    remove_audio_content_repr_from_sentence,
    remove_audio_content_repr_from_sentences_in_job,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return True


@app.post("/jobs/")
async def create_job(job_create: JobCreate):
    job_data = job_create.model_dump()
    status = JobStatus.CREATED if job_data["url"] else JobStatus.FETCHED
    job = Job(**job_data, sentences=None, status=status)

    result = await job.create()
    return {"id": str(result.id)}


@app.get("/jobs/")
async def list_jobs():
    all_jobs = await Job.find(fetch_links=True).to_list()
    for job in all_jobs:
        remove_audio_content_repr_from_sentences_in_job(job)
    return {"number_of_jobs": len(all_jobs), "jobs": all_jobs}


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id), fetch_links=True)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    remove_audio_content_repr_from_sentences_in_job(job)
    return {"job": job.model_dump()}


@app.get("/jobs/{job_id}/sentences")
async def get_job_sentences(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id), fetch_links=True)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    for sentence in job.get_sorted_sentences():
        remove_audio_content_repr_from_sentence(sentence)

    return {"number_of_sentences": len(job.sentences), "sentences": job.sentences}


@app.get("/jobs/{job_id}/audio")
async def get_job_audio(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id), fetch_links=True)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if len(job.sentences) == 0:
        raise HTTPException(status_code=404, detail="No audio data available")

    combined_audio = None

    for sentence in job.get_sorted_sentences():
        if sentence.audio_data:
            audio_data = base64.b64decode(sentence.audio_data)
            audio_segment = AudioSegment.from_wav(BytesIO(audio_data))

            if combined_audio is None:
                combined_audio = audio_segment
            else:
                combined_audio += audio_segment

    output_audio_data = BytesIO()
    if combined_audio:
        combined_audio.export(output_audio_data, format="wav")
        output_audio_data.seek(0)
        return StreamingResponse(content=output_audio_data, media_type="audio/wav")
    else:
        raise HTTPException(status_code=404, detail="No audio combined")


@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id))
    await job.delete()
    return {"message": f"Job {job_id} was deleted."}


@app.delete("/jobs")
async def delete_all_jobs():
    await Sentence.delete_all()
    await Job.delete_all()
    return {"message": "All jobs have been deleted."}

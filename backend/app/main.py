from contextlib import asynccontextmanager
from io import BytesIO
import base64
from beanie.odm.documents import MergeStrategy
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydub.audio_segment import AudioSegment
from starlette.responses import StreamingResponse
import wave

from shared_components import JobStatus
from shared_components import Job, JobCreate
from shared_components.db_init import init_db
from shared_components.models import Sentence


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


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
    all_jobs_json = jsonable_encoder(
        all_jobs, exclude={"sentences": {"__all__": {"audio_data"}}}
    )

    return {"number_of_jobs": len(all_jobs), "jobs": all_jobs}


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id))

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job": job.model_dump()}


@app.get("/jobs/{job_id}/sentences")
async def get_job_sentences(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id), fetch_links=True)
    sentences = job.sentences
    all_sentences = []
    for sentence in sentences:
        sentence.sync(merge_strategy=MergeStrategy.remote)
        sentence_data = sentence.model_dump()
        audio_data = sentence_data.pop("audio_data")
        sentence_data["audio_data_summary"] = (
            f"Audio data of length: {len(audio_data)}"
            if audio_data
            else "No audio data"
        )
        all_sentences.append(sentence_data)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"number_of_sentences": len(sentences), "sentences": all_sentences}


@app.get("/jobs/{job_id}/audio")
async def get_job_audio(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id), fetch_links=True)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if len(job.sentences) == 0:
        raise HTTPException(status_code=404, detail="No audio data available")

    combined_audio = None

    for sentence in job.sentences:
        sentence.sync(merge_strategy=MergeStrategy.remote)
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
    # Delete all jobs from the database
    await Job.delete_all()
    await Sentence.delete_all()
    return {"message": "All jobs have been deleted."}

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
from pathlib import Path
from pydub import AudioSegment

from shared_components import JobStatus
from shared_components import Job, JobCreate
from shared_components.db_init import init_db
from shared_components.models import AudioData, Sentence


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
    all_jobs = await Job.find(fetch_links=True, nesting_depth=1).to_list()
    return {"number_of_jobs": len(all_jobs), "jobs": all_jobs}


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id), fetch_links=True)

    return {"job": job.model_dump()}


@app.get("/jobs/{job_id}/sentences")
async def get_job_sentences(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id), fetch_links=True)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"number_of_sentences": len(job.sentences), "sentences": job.sentences}


@app.get("/jobs/{job_id}/audio")
async def get_job_audio(job_id: str):
    job = await Job.find_one(
        Job.id == ObjectId(job_id), fetch_links=True, nesting_depth=1
    )

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if len(job.sentences) == 0:
        raise HTTPException(status_code=404, detail="No audio data available")

    output_file_path = Path(f"{job_id}.wav")

    # Check if the file already exists
    if output_file_path.exists():
        return FileResponse(
            str(output_file_path), media_type="audio/wav", filename=f"{job_id}.wav"
        )

    combined_audio = None

    sorted_sentences = job.get_sorted_sentences()
    counter = 0
    for sentence in sorted_sentences:
        print(f"Processing {counter} out of {len(sorted_sentences)} sentences")
        await sentence.fetch_all_links()
        if sentence.audio_data:
            audio_data = base64.b64decode(sentence.audio_data.data)
            audio_segment = AudioSegment.from_wav(BytesIO(audio_data))

            if combined_audio is None:
                combined_audio = audio_segment
            else:
                combined_audio += audio_segment
        counter += 1

    if combined_audio:
        # Export directly to file
        combined_audio.export(output_file_path, format="wav")
        return FileResponse(
            str(output_file_path), media_type="audio/wav", filename=f"{job_id}.wav"
        )
    else:
        raise HTTPException(status_code=404, detail="No audio combined")


@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    job = await Job.find_one(Job.id == ObjectId(job_id))
    await job.delete()
    return {"message": f"Job {job_id} was deleted."}


@app.delete("/jobs")
async def delete_all_jobs():
    AudioData.delete_all()
    await Sentence.delete_all()
    await Job.delete_all()
    return {"message": "All jobs have been deleted."}

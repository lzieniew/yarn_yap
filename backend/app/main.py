from app.models import Job, JobCreate
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, HttpUrl


app = FastAPI()
db = None


@app.on_event("startup")
async def startup_db_client():
    global db
    MONGODB_URL = "mongodb://mongodb:27017"  # Adjust as needed
    db = AsyncIOMotorClient(MONGODB_URL).yourdbname


@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()


@app.post("/jobs/", response_model=Job)
async def create_job(job_create: JobCreate):
    job_dict = job_create.dict()
    job_dict.update({"raw_text": None, "sanitized_text": None, "status": "pending"})
    result = await db["jobs"].insert_one(job_dict)
    created_job = await db["jobs"].find_one({"_id": result.inserted_id})
    if created_job is not None:
        return created_job
    raise HTTPException(status_code=500, detail="Job could not be created")

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from shared_components.models import Job, Sentence


mongo_fs = None


async def init_db():
    global mongo_fs
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    mongo_fs = GridFS(client)
    await init_beanie(database=client.jobs, document_models=[Job, Sentence])

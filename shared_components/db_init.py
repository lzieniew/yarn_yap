from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from shared_components.models import AudioData, Job, Sentence


async def init_db():
    global mongo_fs
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    await init_beanie(database=client.jobs, document_models=[Job, Sentence, AudioData])

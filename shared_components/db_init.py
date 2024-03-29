from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from shared_components.models import Job


async def init_db():
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    await init_beanie(database=client.jobs, document_models=[Job])

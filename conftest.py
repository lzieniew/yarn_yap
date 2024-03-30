import time
from beanie.odm.utils.init import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import pytest
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import docker
from shared_components.models import Job

from shared_components.utils import run_async


def wait_for_mongo_to_be_ready(timeout=10):
    start_time = time.time()
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=1000)
    while True:
        try:
            # The ping command is cheap and does not require auth.
            client.admin.command("ping")
            print("MongoDB is ready!")
            break
        except (ServerSelectionTimeoutError, ConnectionFailure):
            if time.time() - start_time > timeout:
                raise TimeoutError("Timed out waiting for MongoDB to be ready")
            print("Waiting for MongoDB to be ready...")
            time.sleep(0.5)


@pytest.fixture(scope="session", autouse=True)
def mongo_db():
    client = docker.from_env()
    mongo_container = client.containers.run(
        "mongo:latest",
        name="pytest-mongo",
        ports={"27017/tcp": 27017},
        detach=True,
        remove=True,
    )

    wait_for_mongo_to_be_ready()

    run_async(
        init_beanie(
            database=AsyncIOMotorClient("mongodb://localhost:27017").test_db,
            document_models=[Job],
        )
    )

    yield mongo_container

    # Cleanup
    mongo_container.stop()

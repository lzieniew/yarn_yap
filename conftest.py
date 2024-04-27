import time
from beanie.odm.utils.init import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import pytest
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import docker
from shared_components.models import Job, Sentence

from shared_components.utils import run_async


def wait_for_mongo_to_be_ready(timeout=10):
    start_time = time.time()
    client = MongoClient("mongodb://localhost:27018", serverSelectionTimeoutMS=1000)
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


def stop_test_mogno_if_running(client):
    try:
        existing_container = client.containers.get("pytest-mongo")
        print("Stopping existing 'pytest-mongo' container...")
        existing_container.stop()
        existing_container.wait()
    except docker.errors.NotFound:
        print("'pytest-mongo' container not found. Proceeding to create a new one.")


@pytest.fixture(scope="session", autouse=True)
def mongo_db():
    client = docker.from_env()
    stop_test_mogno_if_running(client)
    mongo_container = client.containers.run(
        "mongo:latest",
        name="pytest-mongo",
        ports={"27017/tcp": 27018},
        detach=True,
        remove=True,
    )

    wait_for_mongo_to_be_ready()

    run_async(
        init_beanie(
            database=AsyncIOMotorClient("mongodb://localhost:27018").test_db,
            document_models=[Job, Sentence],
        )
    )

    yield mongo_container

    # Cleanup
    mongo_container.stop()

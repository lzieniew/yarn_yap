import pytest
import docker
from time import sleep


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
    # Giving time for MongoDB to initialize
    sleep(10)

    yield mongo_container

    # Cleanup
    mongo_container.stop()

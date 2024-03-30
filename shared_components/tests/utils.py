import mongomock
import pytest
from beanie import init_beanie
from shared_components.models import Job


@pytest.fixture(scope="function")
async def mocked_db(mocker):
    # Patch Beanie's init_beanie function to use a mongomock MongoClient
    mocker.patch("beanie.init_beanie", new_callable=mongomock.MongoClient)
    await init_beanie(database="mocked_db", document_models=[Job])

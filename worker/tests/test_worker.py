import pytest
from shared_components.tests.utils import mocked_db


@pytest.mark.asyncio
async def test_worker(mocked_db):
    assert True

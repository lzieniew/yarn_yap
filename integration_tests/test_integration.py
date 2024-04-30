import os
from time import sleep
import pytest
import requests

from requests.exceptions import ConnectionError


def is_responsive(url):
    try:
        response = requests.get(url + "/health")
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    port = docker_services.port_for("web", 8000)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


def test_create_job(http_service):
    create_response = requests.post(
        http_service + "/jobs/", json={"raw_text": "First sentence. Second sentence"}
    )
    assert create_response.status_code == 200
    job_id = create_response.json()["id"]

    sleep(20)

    job_response = requests.get(f"{http_service}/jobs/{job_id}")
    assert job_response.status_code == 200
    assert 2 == len(job_response.json()["job"]["sentences"])
    assert "generated" == job_response.json()["job"]["status"]

    # response = requests.get(http_service + "/audio")
    # assert response.status_code == 200
    # assert response.headers['Content-Type'] == 'audio/wav'
    #
    # # Validate WAV file structure using pydub
    # audio_data = BytesIO(response.content)
    # try:
    #     audio = AudioSegment.from_file(audio_data, format="wav")
    #     assert len(audio) > 0  # Check that the audio length is greater than 0 milliseconds
    # except Exception as e:
    #     pytest.fail(f"Audio data is not a valid WAV file: {e}")

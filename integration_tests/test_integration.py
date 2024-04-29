import os
import time
import pytest
import requests


# Fixture to start and stop the Docker containers
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "docker-compose.yml")


# Fixture to wait for the API container to be ready
@pytest.fixture(scope="session")
def api_service(docker_services):
    """Ensure that the API service is up and responsive."""
    # Get the URL of the API service from the Docker container
    api_url = f"http://{docker_services.get_service_host('api', 8000)}"

    # Wait for the API service to be responsive
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(api_url)
    )

    return api_url


# Helper function to check if the API is responsive
def is_responsive(url):
    try:
        response = requests.get(url + "/health")
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False


# Test case for the integration test
def test_integration(api_service):
    # Send a request to the API to create a job
    response = requests.post(api_service + "/jobs", json={"text": "Hello, World!"})
    assert response.status_code == 201
    job_id = response.json()["id"]

    # Wait for a few seconds to allow the job to be processed
    time.sleep(5)

    # Check if the job status is "completed"
    response = requests.get(api_service + f"/jobs/{job_id}")
    assert response.status_code == 200
    # assert response.json()["status"] == "completed"

    # # Check if the mock audio file was generated
    # response = requests.get(api_service + f"/jobs/{job_id}/audio")
    # assert response.status_code == 200
    # assert response.headers["Content-Type"] == "audio/mpeg"

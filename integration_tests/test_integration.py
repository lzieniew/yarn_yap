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


def test_empty_base(http_service):
    response = requests.get(http_service + "/jobs/")
    assert response.status_code == 200
    assert response.json()["number_of_jobs"] == 0
    assert response.json()["jobs"] == []

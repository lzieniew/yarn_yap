from unittest.mock import patch
from shared_components.enums import JobStatus
from shared_components.models import Job
from shared_components.utils import run_async
from worker.worker import process_jobs


@patch("worker.worker.generate", return_value="/dummy/path.wav")
def test_worker(mock_generate, mongo_db):
    job = Job(raw_text="some test text", status=JobStatus.CREATED)
    run_async(job.create())

    process_jobs()
    jobs = run_async(Job.find().to_list())
    assert len(jobs) == 1
    assert jobs[0].status == JobStatus.GENERATED

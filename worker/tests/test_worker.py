from shared_components.enums import JobStatus
from shared_components.models import Job
from shared_components.utils import run_async
from worker.worker import process_jobs


def test_worker(mongo_db):
    job = Job(raw_text="some test text", status=JobStatus.CREATED)
    run_async(job.create())

    process_jobs()
    jobs = run_async(Job.find().to_list())
    assert len(jobs) == 1
    assert jobs[0].status == JobStatus.GENERATED

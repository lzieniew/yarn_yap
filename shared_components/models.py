from pydantic import BaseModel, model_validator
from beanie import Document

from .enums import JobStatus


class SentenceModel(BaseModel):
    text: str | None = None
    generated: bool | None = False
    generation_time: int | None = None
    language: str | None = None
    audio_data: bytes | None = None


class Sentence(Document, SentenceModel):
    pass


class JobModel(BaseModel):
    url: str | None = None
    raw_text: str | None = None
    sanitized_text: list[Sentence] | None = None
    language: str | None = None
    status: JobStatus
    progress_percent: str | None = None
    generation_time: int | None = None


class Job(Document, JobModel):
    pass


class JobCreate(BaseModel):
    url: str | None = None
    raw_text: str | None = None

    @model_validator(mode="after")
    def check_exactly_one_field_provided(cls, values):
        # Ensure exactly one of url or raw_text is provided
        if bool(values.url) == bool(values.raw_text):
            raise ValueError(
                "Exactly one of 'url' or 'raw_text' must be provided, not both or none."
            )
        return values

from typing import Dict, Optional
from typing_extensions import Any
from pydantic import BaseModel, Field, model_validator
from beanie import Document

from .enums import JobStatus


class Sentence(BaseModel):
    text: str | None = None
    generated: bool | False = False
    generation_time: int | None = None


class JobModel(BaseModel):
    url: str | None = None
    raw_text: str | None = None
    sanitized_text: list[Sentence] | None = None
    text_language: str | None = None
    audio_path: str | None = None
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

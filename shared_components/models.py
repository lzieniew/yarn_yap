from typing import Dict, Optional
from typing_extensions import Any
from bson import ObjectId
from pydantic import BaseModel, Field, model_validator

from .enums import JobStatus


class Job(BaseModel):
    url: str | None = None
    raw_text: str | None = None
    sanitized_text: str | None = None
    status: JobStatus


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

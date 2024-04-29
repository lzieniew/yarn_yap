from typing import List
from beanie.odm.fields import Link
from pydantic import BaseModel, model_validator
from beanie import Document

from .enums import GenerationMethod, JobStatus


class Sentence(Document):
    text: str | None = None
    generated: bool | None = False
    generation_time: int | None = None
    language: str | None = None
    audio_data: str | None = None
    generation_method: GenerationMethod | None = None
    sentence_number: int | None = None


class Job(Document):
    url: str | None = None
    raw_text: str | None = None
    sentences: List[Link[Sentence]] | None = None
    language: str | None = None
    status: JobStatus
    progress_percent: str | None = None
    generation_time: int | None = None

    def get_sorted_sentences(self) -> list[Sentence]:
        sentences = self.sentences
        if sentences:
            self.sentences.sort(key=lambda sentence: sentence.sentence_number)
            return sentences
        return []


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

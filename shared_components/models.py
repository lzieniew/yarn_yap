from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, model_validator
from beanie import Document

from .enums import JobStatus


class SentenceModel(BaseModel):
    text: str | None = None
    generated: bool | None = False
    generation_time: int | None = None
    language: str | None = None
    audio_data: str | None = None

    @property
    def audio_data_length(self) -> int:
        if self.audio_data:
            return len(self.audio_data)
        return 0


class Sentence(Document, SentenceModel):
    pass


class JobModel(BaseModel):
    url: str | None = None
    raw_text: str | None = None
    sanitized_text: list[PydanticObjectId] | None = None
    language: str | None = None
    status: JobStatus
    progress_percent: str | None = None
    generation_time: int | None = None

    async def fetch_sentences(self):
        if self.sanitized_text:
            # Pass filter as a dictionary
            sentences = await Sentence.find(
                {"_id": {"$in": self.sanitized_text}}
            ).to_list()
            return sentences
        return []

    async def fetch_sentences_info(self):
        if self.sanitized_text:
            # Pass filter as a dictionary
            sentences = await Sentence.find(
                {"_id": {"$in": self.sanitized_text}}
            ).to_list()
            return f"{len(sentences)} sentences"
        return f"No sentences"


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

from pydantic import BaseModel, HttpUrl
from typing import Optional


# Pydantic model for job creation
class JobCreate(BaseModel):
    url: HttpUrl


class Job(BaseModel):
    url: HttpUrl
    raw_text: Optional[str] = None
    sanitized_text: Optional[str] = None
    status: str = "pending"

    class Config:
        schema_extra = {
            "example": {
                "url": "http://example.com",
                "raw_text": "Example content from URL...",
                "sanitized_text": "Example content, sanitized...",
                "status": "pending",
            }
        }

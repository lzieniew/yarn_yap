from pydantic import BaseModel


class Job(BaseModel):
    url: str
    raw_text: str
    sanitized_text: str
    status: str

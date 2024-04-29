from enum import Enum


class JobStatus(str, Enum):
    CREATED = "created"
    FETCHED = "waiting to sanitize"
    SANITIZED = "sanitized"
    GENERATED = "generated"


class GenerationMethod(str, Enum):
    GPU = "GPU"
    CPU = "CPU"
    EXTERNAL_SERVICE = "External service"

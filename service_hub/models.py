from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RequestStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class ServiceRequestCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=3, max_length=1000)
    service: str
    region: str = "us-west"
    priority: Priority = Priority.MEDIUM


class ServiceRequest(ServiceRequestCreate):
    id: UUID = Field(default_factory=uuid4)
    status: RequestStatus = RequestStatus.OPEN
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    audit: list[str] = Field(default_factory=lambda: ["request.created"])


class StatusUpdate(BaseModel):
    status: RequestStatus


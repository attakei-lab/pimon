"""Domain-models."""
from datetime import datetime, timezone

from pydantic import BaseModel, validator


class Message(BaseModel):
    """Received and fetched message."""

    account: str
    uid: int
    sender: str
    subject: str
    received_at: datetime

    @validator("subject")
    def subject_is_removed_crlf(cls, v: str):  # noqa: D102
        return v.replace("\r", "").replace("\n", "")

    @validator("received_at")
    def received_at_is_utc(cls, v: datetime):  # noqa: D102
        return v.astimezone(timezone.utc)

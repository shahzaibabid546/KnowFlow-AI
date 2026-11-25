# Pydantic chat request/response schemas will be added here.

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field
from uuid import uuid4


# Message Schema
class ChatMessage(BaseModel):

    message_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    role: Literal["user", "assistant"]

    content: str

    sources: list[str] = Field(default_factory=list)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# Chat Session Schema
class ChatSession(BaseModel):

    session_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    messages: list[ChatMessage] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# Chat Session Response Schema
class ChatSessionResponse(BaseModel):

    session_id: str

    message: str = "Chat session created successfully."

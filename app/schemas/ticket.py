# Pydantic ticket request/response schemas will be added here.

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


# Support Ticket Schema
class SupportTicket(BaseModel):

    ticket_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    customer_id: str

    session_id: str

    subject: str

    description: str

    status: Literal[
        "open",
        "in_progress",
        "resolved",
        "closed"
    ] = "open"

    priority: Literal[
        "low",
        "normal",
        "high",
        "urgent"
    ] = "normal"

    assigned_to: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# Ticket Creation Schema
class TicketCreate(BaseModel):

    customer_id: str

    session_id: str

    subject: str

    description: str

    priority: Literal[
        "low",
        "normal",
        "high",
        "urgent"
    ] = "normal"


# Ticket Update Schema
class TicketUpdate(BaseModel):

    status: Literal[
        "open",
        "in_progress",
        "resolved",
        "closed"
    ] | None = None

    priority: Literal[
        "low",
        "normal",
        "high",
        "urgent"
    ] | None = None

    assigned_to: str | None = None

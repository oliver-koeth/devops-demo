from typing import Literal, Optional

from pydantic import BaseModel

IncidentSeverity = Literal["P1", "P2", "P3", "P4"]
IncidentStatus = Literal["Open", "Closed"]


class IncidentNote(BaseModel):
    timestamp: str
    author: str
    text: str


class Incident(BaseModel):
    id: str
    title: str
    severity: IncidentSeverity
    status: IncidentStatus
    service: str
    createdAt: str
    updatedAt: str
    notes: list[IncidentNote]


class IncidentCreate(BaseModel):
    title: str
    severity: IncidentSeverity
    status: IncidentStatus = "Open"
    service: str


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    severity: Optional[IncidentSeverity] = None
    status: Optional[IncidentStatus] = None
    service: Optional[str] = None


class IncidentNoteCreate(BaseModel):
    author: str
    text: str

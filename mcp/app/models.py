from typing import Literal

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


class Runbook(BaseModel):
    id: str
    title: str
    tags: list[str]
    content: str
    createdAt: str
    updatedAt: str

from typing import Optional

from pydantic import BaseModel


class Runbook(BaseModel):
    id: str
    title: str
    tags: list[str]
    content: str
    createdAt: str
    updatedAt: str


class RunbookCreate(BaseModel):
    title: str
    tags: list[str]
    content: str


class RunbookUpdate(BaseModel):
    title: Optional[str] = None
    tags: Optional[list[str]] = None
    content: Optional[str] = None

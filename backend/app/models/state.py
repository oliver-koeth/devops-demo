from pydantic import BaseModel

from app.models.incident import Incident
from app.models.runbook import Runbook


class AppState(BaseModel):
    schemaVersion: int
    incidents: list[Incident]
    runbooks: list[Runbook]

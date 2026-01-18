from fastapi import Request

from app.services.incidents import IncidentService
from app.services.runbooks import RunbookService


def get_incident_service(request: Request) -> IncidentService:
    return request.app.state.incident_service


def get_runbook_service(request: Request) -> RunbookService:
    return request.app.state.runbook_service

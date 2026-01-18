from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.dependencies import get_incident_service
from app.models.incident import Incident, IncidentCreate, IncidentNoteCreate, IncidentUpdate
from app.services.incidents import IncidentService

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[Incident])
def list_incidents(
    q: str | None = None,
    status: str | None = None,
    severity: str | None = None,
    service: str | None = None,
    incident_service: IncidentService = Depends(get_incident_service),
) -> list[Incident]:
    return incident_service.list_incidents(q=q, status=status, severity=severity, service=service)


@router.post("", response_model=Incident, status_code=201)
def create_incident(
    payload: IncidentCreate, incident_service: IncidentService = Depends(get_incident_service)
) -> Incident:
    return incident_service.create_incident(payload)


@router.get("/{incident_id}", response_model=Incident)
def get_incident(
    incident_id: str, incident_service: IncidentService = Depends(get_incident_service)
) -> Incident:
    try:
        return incident_service.get_incident(incident_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Incident not found") from exc


@router.put("/{incident_id}", response_model=Incident)
def update_incident(
    incident_id: str,
    payload: IncidentUpdate,
    incident_service: IncidentService = Depends(get_incident_service),
) -> Incident:
    try:
        return incident_service.update_incident(incident_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Incident not found") from exc


@router.delete("/{incident_id}", status_code=204)
def delete_incident(
    incident_id: str, incident_service: IncidentService = Depends(get_incident_service)
) -> Response:
    try:
        incident_service.delete_incident(incident_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Incident not found") from exc
    return Response(status_code=204)


@router.post("/{incident_id}/notes", response_model=Incident)
def add_note(
    incident_id: str,
    payload: IncidentNoteCreate,
    incident_service: IncidentService = Depends(get_incident_service),
) -> Incident:
    try:
        return incident_service.add_note(incident_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Incident not found") from exc


@router.post("/{incident_id}/close", response_model=Incident)
def close_incident(
    incident_id: str, incident_service: IncidentService = Depends(get_incident_service)
) -> Incident:
    try:
        return incident_service.close_incident(incident_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Incident not found") from exc


@router.post("/{incident_id}/reopen", response_model=Incident)
def reopen_incident(
    incident_id: str, incident_service: IncidentService = Depends(get_incident_service)
) -> Incident:
    try:
        return incident_service.reopen_incident(incident_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Incident not found") from exc

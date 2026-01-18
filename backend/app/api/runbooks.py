from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.dependencies import get_runbook_service
from app.models.runbook import Runbook, RunbookCreate, RunbookUpdate
from app.services.runbooks import RunbookService

router = APIRouter(prefix="/runbooks", tags=["runbooks"])


@router.get("", response_model=list[Runbook])
def list_runbooks(
    q: str | None = None,
    tag: str | None = None,
    runbook_service: RunbookService = Depends(get_runbook_service),
) -> list[Runbook]:
    return runbook_service.list_runbooks(q=q, tag=tag)


@router.post("", response_model=Runbook, status_code=201)
def create_runbook(
    payload: RunbookCreate, runbook_service: RunbookService = Depends(get_runbook_service)
) -> Runbook:
    return runbook_service.create_runbook(payload)


@router.get("/{runbook_id}", response_model=Runbook)
def get_runbook(
    runbook_id: str, runbook_service: RunbookService = Depends(get_runbook_service)
) -> Runbook:
    try:
        return runbook_service.get_runbook(runbook_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Runbook not found") from exc


@router.put("/{runbook_id}", response_model=Runbook)
def update_runbook(
    runbook_id: str,
    payload: RunbookUpdate,
    runbook_service: RunbookService = Depends(get_runbook_service),
) -> Runbook:
    try:
        return runbook_service.update_runbook(runbook_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Runbook not found") from exc


@router.delete("/{runbook_id}", status_code=204)
def delete_runbook(
    runbook_id: str, runbook_service: RunbookService = Depends(get_runbook_service)
) -> Response:
    try:
        runbook_service.delete_runbook(runbook_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Runbook not found") from exc
    return Response(status_code=204)

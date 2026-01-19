from typing import Iterable

from mcp.server.fastmcp import FastMCP

from app.client import BackendClient, BackendNotFoundError, BackendUnavailableError
from app.models import Incident, IncidentSeverity, IncidentStatus, Runbook


def _clean_params(**kwargs: str | None) -> dict[str, str]:
    return {key: value for key, value in kwargs.items() if value is not None}


def _map_list(items: Iterable[dict], model):
    return [model.model_validate(item) for item in items]


def register_tools(mcp: FastMCP, client: BackendClient) -> None:
    @mcp.tool()
    async def list_incidents(
        q: str | None = None,
        status: IncidentStatus | None = None,
        severity: IncidentSeverity | None = None,
        service: str | None = None,
    ) -> list[Incident]:
        """List incidents from the backend."""
        params = _clean_params(q=q, status=status, severity=severity, service=service)
        try:
            data = await client.list_incidents(params=params or None)
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return _map_list(data, Incident)

    @mcp.tool()
    async def get_incident(incident_id: str) -> Incident:
        """Fetch a single incident by id."""
        try:
            data = await client.get_incident(incident_id)
        except BackendNotFoundError as exc:
            raise RuntimeError("Incident not found") from exc
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return Incident.model_validate(data)

    @mcp.tool()
    async def list_runbooks(q: str | None = None, tag: str | None = None) -> list[Runbook]:
        """List runbooks from the backend."""
        params = _clean_params(q=q, tag=tag)
        try:
            data = await client.list_runbooks(params=params or None)
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return _map_list(data, Runbook)

    @mcp.tool()
    async def get_runbook(runbook_id: str) -> Runbook:
        """Fetch a single runbook by id."""
        try:
            data = await client.get_runbook(runbook_id)
        except BackendNotFoundError as exc:
            raise RuntimeError("Runbook not found") from exc
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return Runbook.model_validate(data)

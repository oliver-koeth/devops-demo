from __future__ import annotations

from typing import Iterable
from urllib.parse import parse_qs

from mcp.server.fastmcp import FastMCP

from app.client import BackendClient, BackendNotFoundError, BackendUnavailableError
from app.models import Incident, Runbook


def _clean_params(**kwargs: str | None) -> dict[str, str]:
    return {key: value for key, value in kwargs.items() if value is not None}


def _parse_query(query: str) -> dict[str, str]:
    cleaned = query[1:] if query.startswith("?") else query
    parsed = parse_qs(cleaned, keep_blank_values=False)
    return {key: values[0] for key, values in parsed.items() if values}


def _map_list(items: Iterable[dict], model):
    return [model.model_validate(item).model_dump() for item in items]


def _map_item(item: dict, model) -> dict:
    return model.model_validate(item).model_dump()


def register_resources(mcp: FastMCP, client: BackendClient) -> None:
    @mcp.resource(
        "incidents://",
        name="incidents",
        title="Incidents",
        description="List incidents from the backend.",
        mime_type="application/json",
    )
    async def incidents_collection() -> list[dict]:
        try:
            data = await client.list_incidents()
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return _map_list(data, Incident)

    @mcp.resource(
        "incidents://?{query}",
        name="incidents-query",
        title="Incidents (filtered)",
        description="List incidents using query filters.",
        mime_type="application/json",
    )
    async def incidents_collection_filtered(query: str) -> list[dict] | dict:
        if "=" not in query and not query.startswith("?"):
            try:
                data = await client.get_incident(query)
            except BackendNotFoundError as exc:
                raise RuntimeError("not found") from exc
            except BackendUnavailableError as exc:
                raise RuntimeError("backend unavailable") from exc
            return _map_item(data, Incident)
        parsed = _parse_query(query)
        params = _clean_params(
            q=parsed.get("q"),
            status=parsed.get("status"),
            severity=parsed.get("severity"),
            service=parsed.get("service"),
        )
        try:
            data = await client.list_incidents(params=params or None)
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return _map_list(data, Incident)

    @mcp.resource(
        "incidents://{incident_id}",
        name="incident",
        title="Incident",
        description="Incident details by id.",
        mime_type="application/json",
    )
    async def incident_item(incident_id: str) -> dict:
        try:
            data = await client.get_incident(incident_id)
        except BackendNotFoundError as exc:
            raise RuntimeError("not found") from exc
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return _map_item(data, Incident)

    @mcp.resource(
        "runbooks://",
        name="runbooks",
        title="Runbooks",
        description="List runbooks from the backend.",
        mime_type="application/json",
    )
    async def runbooks_collection() -> list[dict]:
        try:
            data = await client.list_runbooks()
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return _map_list(data, Runbook)

    @mcp.resource(
        "runbooks://?{query}",
        name="runbooks-query",
        title="Runbooks (filtered)",
        description="List runbooks using query filters.",
        mime_type="application/json",
    )
    async def runbooks_collection_filtered(query: str) -> list[dict] | dict:
        if "=" not in query and not query.startswith("?"):
            try:
                data = await client.get_runbook(query)
            except BackendNotFoundError as exc:
                raise RuntimeError("not found") from exc
            except BackendUnavailableError as exc:
                raise RuntimeError("backend unavailable") from exc
            return _map_item(data, Runbook)
        parsed = _parse_query(query)
        params = _clean_params(q=parsed.get("q"), tag=parsed.get("tag"))
        try:
            data = await client.list_runbooks(params=params or None)
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return _map_list(data, Runbook)

    @mcp.resource(
        "runbooks://{runbook_id}",
        name="runbook",
        title="Runbook",
        description="Runbook details by id.",
        mime_type="application/json",
    )
    async def runbook_item(runbook_id: str) -> dict:
        try:
            data = await client.get_runbook(runbook_id)
        except BackendNotFoundError as exc:
            raise RuntimeError("not found") from exc
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        return _map_item(data, Runbook)

from typing import Iterable

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

from app.client import BackendClient, BackendNotFoundError, BackendUnavailableError
from app.models import Incident, IncidentSeverity, IncidentStatus, Runbook
from app.widgets import Widget, widgets_by_id, widget_meta


def _clean_params(**kwargs: str | None) -> dict[str, str]:
    return {key: value for key, value in kwargs.items() if value is not None}


def _map_list(items: Iterable[dict], model):
    return [model.model_validate(item) for item in items]


def _map_list_dump(items: Iterable[dict], model) -> list[dict]:
    return [model.model_validate(item).model_dump() for item in items]


def _map_item_dump(item: dict, model) -> dict:
    return model.model_validate(item).model_dump()


def _widget_response_text(widget: Widget, **kwargs: str) -> str:
    return widget.response_text.format(**kwargs)


def _widget_result(widget: Widget, text: str, structured: dict) -> CallToolResult:
    return CallToolResult(
        content=[TextContent(type="text", text=text)],
        structuredContent=structured,
        _meta=widget_meta(widget),
    )


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

    incident_list_widget = widgets_by_id["incident_list_widget"]

    @mcp.tool(
        name=incident_list_widget.id,
        title=incident_list_widget.title,
        description="Show incidents in a widget.",
        meta=widget_meta(incident_list_widget),
    )
    async def show_incident_list_widget(
        q: str | None = None,
        status: IncidentStatus | None = None,
        severity: IncidentSeverity | None = None,
        service: str | None = None,
    ) -> CallToolResult:
        params = _clean_params(q=q, status=status, severity=severity, service=service)
        try:
            data = await client.list_incidents(params=params or None)
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        incidents = _map_list_dump(data, Incident)
        structured = {"items": incidents, "filters": params}
        text = _widget_response_text(incident_list_widget)
        return _widget_result(incident_list_widget, text=text, structured=structured)

    incident_detail_widget = widgets_by_id["incident_detail_widget"]

    @mcp.tool(
        name=incident_detail_widget.id,
        title=incident_detail_widget.title,
        description="Show incident details in a widget.",
        meta=widget_meta(incident_detail_widget),
    )
    async def show_incident_detail_widget(incident_id: str) -> CallToolResult:
        try:
            data = await client.get_incident(incident_id)
        except BackendNotFoundError as exc:
            raise RuntimeError("Incident not found") from exc
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        incident = _map_item_dump(data, Incident)
        structured = {"incidentId": incident_id, "item": incident}
        text = _widget_response_text(incident_detail_widget, incident_id=incident_id)
        return _widget_result(incident_detail_widget, text=text, structured=structured)

    runbook_list_widget = widgets_by_id["runbook_list_widget"]

    @mcp.tool(
        name=runbook_list_widget.id,
        title=runbook_list_widget.title,
        description="Show runbooks in a widget.",
        meta=widget_meta(runbook_list_widget),
    )
    async def show_runbook_list_widget(q: str | None = None, tag: str | None = None) -> CallToolResult:
        params = _clean_params(q=q, tag=tag)
        try:
            data = await client.list_runbooks(params=params or None)
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        runbooks = _map_list_dump(data, Runbook)
        structured = {"items": runbooks, "filters": params}
        text = _widget_response_text(runbook_list_widget)
        return _widget_result(runbook_list_widget, text=text, structured=structured)

    runbook_detail_widget = widgets_by_id["runbook_detail_widget"]

    @mcp.tool(
        name=runbook_detail_widget.id,
        title=runbook_detail_widget.title,
        description="Show runbook details in a widget.",
        meta=widget_meta(runbook_detail_widget),
    )
    async def show_runbook_detail_widget(runbook_id: str) -> CallToolResult:
        try:
            data = await client.get_runbook(runbook_id)
        except BackendNotFoundError as exc:
            raise RuntimeError("Runbook not found") from exc
        except BackendUnavailableError as exc:
            raise RuntimeError("backend unavailable") from exc
        runbook = _map_item_dump(data, Runbook)
        structured = {"runbookId": runbook_id, "item": runbook}
        text = _widget_response_text(runbook_detail_widget, runbook_id=runbook_id)
        return _widget_result(runbook_detail_widget, text=text, structured=structured)

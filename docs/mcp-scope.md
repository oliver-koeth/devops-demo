# MCP Server Scope (Stage 4)

This note documents the current MCP server scope in Stage 4 and outlines the
resource model planned for ChatGPT Apps integration in Stage 5. No Stage 5
implementation is included here.

## Stage 4 Scope
- Read-only MCP server that calls the FastAPI backend over HTTP.
- Focused on incidents and runbooks only.
- Transport: Streamable HTTP.

## Implemented Tools (Stage 4)
- `list_incidents(q, status, severity, service)` -> list incidents
- `get_incident(incident_id)` -> fetch a single incident by id
- `list_runbooks(q, tag)` -> list runbooks
- `get_runbook(runbook_id)` -> fetch a single runbook by id

## Resource Model for ChatGPT Apps (Stage 5 Plan)
Resources mirror the tool surface to keep schemas stable and minimal.

### Collections
- `incidents://` (supports `q`, `status`, `severity`, `service`)
- `runbooks://` (supports `q`, `tag`)

Example URIs:
- `incidents://?status=Open&severity=P1`
- `incidents://?q=latency&service=Payments API`
- `runbooks://?tag=incident`

### Items
- `incidents://{id}`
- `runbooks://{id}`

Example URIs:
- `incidents://1234`
- `runbooks://abcd`

## Notes
- Item resources map directly to `get_incident` and `get_runbook`.
- Collection resources map directly to `list_incidents` and `list_runbooks`.
- Stage 5 will add resource wiring and any additional metadata as needed.

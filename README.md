# DevOps Runbook Assistant (Stage 5)

## Purpose
This repository contains a staged demo application. Stage 5 expands the MCP server for ChatGPT-native integration with resources alongside the existing Angular frontend and FastAPI backend.

## Current Scope (Stage 5)
- Angular frontend in `frontend/` using standalone components and Angular router.
- FastAPI backend in `backend/` with file-based persistence and seed data.
- MCP server in `mcp/` providing read-only tools and resources for incidents and runbooks (see `docs/mcp-scope.md`).
- REST API under `/api/v1` with Swagger docs at `/docs` and OpenAPI JSON at `/openapi.json`.

## Out of Scope (Not Yet Implemented)
- Authentication, authorization, or security hardening.
- Deployment tooling.
- Stage 6+ features beyond the current MCP resource scope.

## Stage 5: ChatGPT-native MCP Resources
Stage 5 adds MCP resources that mirror the tool surface so ChatGPT-native clients can discover
and render incidents/runbooks via stable resource URIs. See `docs/mcp-scope.md` for the exact URI
patterns and payload scope.

High-level resource list:
- Incident collection and item resources (`incidents://`, `incidents://{id}`).
- Runbook collection and item resources (`runbooks://`, `runbooks://{id}`).
- Filtered collection resources via query URIs (`incidents://?…`, `runbooks://?…`).

## Repository Structure
- `frontend/` — Angular application (Stage 3 scope).
- `backend/` — FastAPI service with file persistence (Stage 3).
- `mcp/` — MCP server (Stage 4) for read-only tool access.
- `docs/` — Architecture notes and demo scripts.

## Run the Backend (FastAPI)
This backend uses Poetry for dependency management.

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`, with:
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Backend Persistence
State is stored in `backend/.tmp/state.json` by default. The file is created on startup if missing or invalid and is not committed to Git.
Set `BACKEND_STATE_PATH` to override the persistence file path (useful for tests).

### Backend Tests
```bash
cd backend
poetry install
poetry run pytest
```

Test strategy:
- **Unit tests** cover the services and file persistence layer (create/update/delete, filtering, status changes, state file writes).
- **Integration tests** exercise the FastAPI routes end-to-end using `TestClient`.

## Run the MCP Server (Stage 4/5)
The MCP server runs as a separate Python process and calls the backend via HTTP.

```bash
cd mcp

export BACKEND_BASE_URL=http://localhost:8000
export MCP_HOST=127.0.0.1
export MCP_PORT=8090

poetry install --no-root
poetry run python -m app.main
```

The MCP Streamable HTTP endpoint will be available at `http://127.0.0.1:8090`.

### Typical Local Flow
1. Start the backend.
2. Start the MCP server.
3. Optionally run the frontend.

### MCP Integration Tests
```bash
cd mcp
poetry install --no-root --extras dev
poetry run pytest
```

### MCP Inspector Tests
```bash
npx @modelcontextprotocol/inspector
```

Now configure the server in the MCP Inspector UI with the URL `http://localhost:8090/mcp`
and the proxy token copied from the log of the MCP Inspector in the UI.

### MCP Inspector (Stage 5 Resources)
1. Start the backend and MCP server.
2. Run the Inspector: `npx @modelcontextprotocol/inspector`.
3. Select the **HTTP** transport and connect to `http://localhost:8090/mcp`.
4. Open the **Resources** tab, refresh to see resource URIs, and read:
   - `incidents://` or `runbooks://` for index resources.
   - `incidents://{id}` or `runbooks://{id}` for item resources.
   - Filtered URIs such as `incidents://?status=Open` or `runbooks://?tag=incident`.

Limitations:
- The Inspector validates resource discovery and payloads.
- Final UI rendering behavior is validated in a ChatGPT client later.

## Run the Frontend (Angular)
```bash
cd frontend
npm install
npm run start
```
The dev server will be available at `http://localhost:4200` and will call the backend at `http://localhost:8000/api/v1`.

## Build Production Bundle
```bash
cd frontend
npm install
npm run build
```

## Frontend Tests (Playwright)
```bash
cd frontend
npm install
npm run test
```

## Staged Development Notes
- Stage 5 will add ChatGPT-native integration.
- Keep changes incremental and avoid implementing future-stage features early.

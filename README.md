# DevOps Runbook Assistant (Stage 3)

## Purpose
This repository contains a staged demo application. Stage 3 introduces a FastAPI backend with file-based persistence and updates the Angular frontend to consume the backend API for incident + runbook workflows.

## Current Scope (Stage 3)
- Angular frontend in `frontend/` using standalone components and Angular router.
- FastAPI backend in `backend/` with file-based persistence and seed data.
- REST API under `/api/v1` with Swagger docs at `/docs` and OpenAPI JSON at `/openapi.json`.

## Out of Scope (Not Yet Implemented)
- MCP server and ChatGPT-native integration (Stages 4/5).
- Authentication, authorization, or security hardening.
- Deployment tooling.

## Repository Structure
- `frontend/` — Angular application (Stage 3 scope).
- `backend/` — FastAPI service with file persistence (Stage 3).
- `mcp/` — Placeholder for MCP server code (Stage 4/5).
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
State is stored in `backend/.tmp/state.json`. The file is created on startup if missing or invalid and is not committed to Git.

### Backend Tests
```bash
cd backend
poetry install
poetry run pytest
```

Test strategy:
- **Unit tests** cover the services and file persistence layer (create/update/delete, filtering, status changes, state file writes).
- **Integration tests** exercise the FastAPI routes end-to-end using `TestClient`.

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

## Staged Development Notes
- Stage 4/5 will add an MCP server and ChatGPT-native integration.
- Keep changes incremental and avoid implementing future-stage features early.

# Stage 3 Codex Prompt (Backend)

## Role & Context

You are acting as a senior full-stack engineer implementing **Stage 3** of a staged demo application for a DevOps audience.

Stage 2 already exists and provides an Angular frontend that persists Incidents and Runbooks in browser `localStorage` with seed/sample data.  
In Stage 3 you will introduce a FastAPI backend with filesystem persistence and modify the frontend to use the backend API instead of `localStorage`.

---

## Scope for This Step (Stage 3)

You **must** implement:
- A FastAPI backend under `backend/`
- File-based persistence to a temporary file (excluded from git)
- The same hard-coded sample data as the frontend used in Stage 2 (as initial state)
- REST API endpoints with OpenAPI documentation
- Backend unit and integration tests
- Updates to the Angular frontend to use the backend API

You **must not**:
- Add any MCP server code (Stage 4+)
- Add authentication, authorization, or security hardening
- Overengineer performance, concurrency, or scaling

---

## High-level Architecture Intent

Starting in Stage 3, the backend becomes the system of record.  
The frontend is reduced to a thin client that calls backend REST endpoints.  
A clean API boundary must be preserved so that an MCP server can later call the backend via the same interface.

---

## Backend Requirements (FastAPI)

### Project Scaffolding

- Use Python 3.11+ (follow any existing repo version preference).
- Create a standard structure under `backend/`, for example:
```
backend/
app/
main.py
api/              # routers
models/           # Pydantic schemas
services/         # business logic
persistence/      # file store
seed/             # seed data
core/             # settings, constants
tests/
pyproject.toml      # preferred, or requirements.txt
README.md           # optional (root README must be updated regardless)
```

- Use a modern dependency manager:
- Prefer `pyproject.toml` with Poetry or uv/pip-tools
- Keep dependencies minimal

---

### Persistence (Temp File, Write-on-change)

- Persist **all state** to a single JSON file in a temp-like path.
- The file **must not** be committed to git.
- Write the full file on every mutation (create, update, delete, add note, close/reopen).
- Use a clear default location, e.g. `backend/.tmp/state.json`.
- Automatically create the directory if it does not exist.
- On backend startup:
- Load the state file if it exists
- Otherwise initialize with seed data and write it immediately

- Include a simple schema version field in the file (e.g. `"schemaVersion": 1`) to support future migrations.

---

### Domain Models (Match Frontend)

Implement the same entities and fields as in Stage 2.

**Incidents**
- `id` (string)
- `title` (string, required)
- `severity` ("P1" | "P2" | "P3" | "P4")
- `status` ("Open" | "Closed")
- `service` (string, required)
- `createdAt` (ISO string)
- `updatedAt` (ISO string)
- `notes`: array of `{ timestamp, author, text }`

**Runbooks**
- `id` (string)
- `title` (string, required)
- `tags`: string[]
- `content` (string)
- `createdAt` (ISO string)
- `updatedAt` (ISO string)

Use Pydantic models for input and output.  
Generate IDs server-side (UUID strings) and set timestamps server-side.  
Validate required fields and return appropriate HTTP status codes.

---

### API Contract (REST)

Expose a clean REST API under a versioned prefix.

- Base prefix: `/api/v1`

**Incidents**
- `GET    /api/v1/incidents`
- `POST   /api/v1/incidents`
- `GET    /api/v1/incidents/{id}`
- `PUT    /api/v1/incidents/{id}`
- `DELETE /api/v1/incidents/{id}`
- `POST   /api/v1/incidents/{id}/notes`
- `POST   /api/v1/incidents/{id}/close`
- `POST   /api/v1/incidents/{id}/reopen`

**Runbooks**
- `GET    /api/v1/runbooks`
- `POST   /api/v1/runbooks`
- `GET    /api/v1/runbooks/{id}`
- `PUT    /api/v1/runbooks/{id}`
- `DELETE /api/v1/runbooks/{id}`

**Other**
- `GET /healthz`

Enable CORS for local development so the Angular frontend can call the backend.

Ensure OpenAPI documentation is available and documented in the README:
- `/docs`
- `/openapi.json`

---

### Business Logic Organization

- Isolate file persistence behind a storage abstraction (e.g. `FileStateStore`).
- Keep domain logic in services (e.g. `IncidentService`, `RunbookService`).
- API routers should remain thin.
- Every mutation must:
- Update `updatedAt`
- Persist state to disk

---

### Error Handling

- Return `404` for unknown IDs.
- Use FastAPI’s default `422` for validation errors.
- If the state file is corrupted:
- Log a warning
- Reset to seed data
- Rewrite the file

---

### Run Configuration

Provide a simple local run command, for example:

```bash
uvicorn app.main:app --reload --port 8000
```

## Frontend Changes (Angular)

- Replace the `localStorage` persistence layer with an API client layer.
- UI and UX must remain functionally identical.
- Implement Angular services that call backend endpoints.
- Preserve `data-testid` attributes for Playwright where possible.
- Update frontend configuration to target the backend API  
  (e.g. `http://localhost:8000/api/v1`).

**Important:**
- Do not remove seed data logic from the frontend; seeding now belongs to backend startup.
- The frontend should render exactly what the backend returns.

---

## Testing Requirements (Backend)

Create both **unit** and **integration** tests.

### Unit Tests
- Test services and persistence in isolation.
- Use temporary files/directories for persistence.
- Validate:
  - CRUD operations for incidents and runbooks
  - Note addition updates `updatedAt` and persists
  - Close/reopen behavior
  - Search and filtering logic
  - File writes on each mutation
  - Startup behavior (existing file vs seed)

### Integration Tests
- Use FastAPI `TestClient` or `httpx`.
- Validate full flows:
  - Incident lifecycle (create → update → note → close → reopen → delete)
  - Runbook lifecycle
  - Search and filter parameters
  - `/openapi.json` availability
  - `/healthz` availability

Use `pytest`, keep dependencies minimal, and ensure tests do not write outside the repository.

---

## README & Documentation Updates

Update the root `README.md` to reflect Stage 3:
- High-level architecture (frontend + backend, no MCP yet)
- How to run the backend
- How to access OpenAPI documentation
- Backend test strategy (unit vs integration)
- How to run the frontend against the backend
- Where the temporary persistence file is stored
- Explicitly state that security/auth is intentionally out of scope

Update `AGENTS.md` to:
- Reinforce stage boundaries (Stage 4+ introduces MCP)
- Define backend conventions:
  - Service and persistence separation
  - No file writes from routers
  - Consistent use of Pydantic
  - API versioning under `/api/v1`

---

## Repo Hygiene

- Add persistence paths to `.gitignore` (e.g. `backend/.tmp/`, state JSON files).
- Add minimal logging if useful (do not overdo).
- Ensure `npm run build` still works for the frontend.
- Ensure the backend runs via a single documented command.

---

## Output Format

1. Show the updated directory tree for:
   - `backend/`
   - `frontend/` (if changed)
   - Modified root-level files (`README.md`, `AGENTS.md`, `.gitignore`)

2. Provide exact run instructions for:
   - Backend dev server
   - Backend tests
   - Frontend dev server (pointing at backend)

3. Provide a brief summary of:
   - What was implemented in Stage 3
   - What was explicitly not implemented (MCP, auth, etc.)

---

## Important Notes

- If Playwright cannot run due to missing browser binaries:
  - Do not attempt OS-level installs
  - Keep Playwright configuration intact
  - Note the limitation explicitly
- Backend seed data must match the frontend’s existing sample data.  
  If necessary, locate it in the frontend code and port it verbatim.

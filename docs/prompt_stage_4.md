# Stage 4 Codex Prompt (MCP Server - tools only)

## Role & Context

You are acting as a senior full-stack engineer implementing **Stage 4** of a staged demo application for a DevOps audience.

Create a branch named **`Implement Stage 4 MCP server`**.

Stage 3 already exists:
- An Angular frontend that uses a FastAPI backend for persistence
- A FastAPI backend running locally (default) at `http://localhost:8000` with API under `/api/v1`
- Backend persistence to a temporary JSON file with seed data on first start
- Backend unit and integration tests
- Frontend Playwright E2E tests (do **not** remove or weaken documentation about them)

In Stage 4, you will add an MCP server running as its own Python process that exposes **read-only tools**
for incidents and runbooks by calling the backend API.

---

## Scope for This Step (Stage 4)

You **must** implement:
- A Python MCP server under `mcp/` that runs as its own process
- MCP tools to read incidents and runbooks from the backend (read-only)
- True end-to-end integration tests for the MCP server using a real backend instance
- README updates that add MCP instructions **without removing** existing frontend/backend information

You **must not**:
- Add any UI resources for ChatGPT-native app capability (Stage 5)
- Add authentication or authorization
- Add write tools that mutate incidents or runbooks
- Change backend or frontend behavior beyond what is required to enable MCP

---

## MCP Server Requirements

### Language & Location

- Implement the MCP server in Python under `mcp/`.
- Keep a clean, minimal structure, for example:
```
mcp/
app/
main.py
client.py        # backend API client
tools.py         # tool definitions and handlers
models.py        # Pydantic models for tool I/O (if useful)
core.py          # configuration / environment
tests/
pyproject.toml   # preferred, or requirements.txt
README.md        # optional (root README must be updated regardless)
```

- Use Python 3.11+ if consistent with the backend.

---

### Process & Configuration

- The MCP server **must** run as its own process, separate from the backend.
- It **must** communicate with the backend via HTTP using the same public API as the frontend.
- Backend base URL:
- Default: `http://localhost:8000`
- Configurable via `BACKEND_BASE_URL` environment variable
- Backend API prefix: `/api/v1`

- Provide a simple local run command and document it in the root README.
- Do not add Docker or Docker Compose in this stage.

---

### MCP Tools (Read-only)

Expose conventional, read-only tools that call the backend API and return structured data.

**Incidents tools**
- `list_incidents`
- Inputs: optional filters matching backend query params:
  - `q` (search string)
  - `status` ("Open" | "Closed")
  - `severity` ("P1" | "P2" | "P3" | "P4")
  - `service` (string)
- Output: list of incidents (summaries or full objects, depending on backend response)

- `get_incident`
- Input: `id` (string)
- Output: incident detail

**Runbooks tools**
- `list_runbooks`
- Inputs:
  - `q` (search string)
  - `tag` (string)
- Output: list of runbooks (or summaries)

- `get_runbook`
- Input: `id` (string)
- Output: runbook detail

**Tool behavior**
- Backend `404` → MCP error indicating “not found”
- Backend unreachable → MCP error indicating “backend unavailable”
- Do not implement retries beyond a simple request timeout

**Data contracts**
- Align tool schemas strictly with backend responses
- Do not invent or transform fields
- Keep schemas explicit and stable (important for Stage 5)

---

### Backend API Client

- Implement a small HTTP client used by tool handlers.
- Use `httpx` (preferred) or `requests`.
- Include sensible timeouts (e.g. 5 seconds).
- Centralize base URL and route construction.
- Map backend errors consistently.

---

## Integration Test Requirements (MCP)

You **must** implement true integration tests:

- Spin up a real backend instance during tests:
- Use a temporary persistence file
- Ensure backend is seeded with sample data
- Run on a random free port

- Start the MCP server in tests (subprocess or in-process, depending on SDK),
but it must behave as a separate process boundary.
- Configure `BACKEND_BASE_URL` to point to the test backend

**Minimum test cases**
1. `list_incidents` returns seeded incidents  
2. `get_incident` returns a known seeded incident  
3. `list_runbooks` returns seeded runbooks  
4. `get_runbook` returns a known seeded runbook  
5. `get_incident` with an unknown ID returns a clear “not found” error  
6. Backend unavailable produces a clear error

**Notes**
- Use `pytest`
- Keep tests deterministic
- Do not rely on hard-coded ports
- Avoid flakiness by waiting for backend readiness

---

## Backend Changes (Only If Necessary)

Avoid backend changes. If strictly required for tests:
- Allow configuring the persistence file path via an environment variable
- Allow forcing or resetting seed data for test runs

Any such changes must be minimal and backward compatible.

---

## README & Documentation Updates

Update the root `README.md` to add an MCP section:
- What Stage 4 introduces (read-only MCP server)
- How to run the MCP server
- Environment variables:
- `BACKEND_BASE_URL` (default `http://localhost:8000`)
- Typical local workflow:
1. Start backend
2. Start MCP server
3. Optionally run frontend

- Document how to run MCP integration tests.

Do **not** remove or overwrite:
- Frontend Playwright test instructions
- Backend OpenAPI documentation instructions
- Backend test strategy documentation

Extend the README instead.

Update `AGENTS.md`:
- Add Stage 4 conventions:
- MCP server must call backend via HTTP only
- Read-only tools only in Stage 4
- Keep tool schemas stable for Stage 5 resources

---

## Repo Hygiene

- Add any new virtualenv, cache, or test artifacts to `.gitignore`.
- Do not commit temporary state files.
- Keep dependencies minimal.
- Ensure all commands are copy/paste runnable.

---

## Output Format

1. Show the updated directory tree for:
 - `mcp/`
 - Any changed backend files (only if necessary)
 - Modified root-level files (`README.md`, `AGENTS.md`, `.gitignore`)

2. Provide exact run instructions for:
 - Backend dev server (if needed)
 - MCP server
 - MCP integration tests

3. Provide a brief summary:
 - What was added in Stage 4
 - What was explicitly **not** added (auth, write tools, UI resources, Stage 5)

---

## Important Note About Test Execution Environments

If the environment cannot execute certain tests due to missing system dependencies:
- Do not attempt OS-level installs
- Keep tests and configuration correct
- Note the limitation explicitly

(Playwright may have such constraints; do not modify Playwright setup in this stage.)

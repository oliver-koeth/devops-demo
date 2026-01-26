# DevOps Runbook Assistant (Stage 5)

## Purpose
This repository contains a staged demo application that shows how to develop applications for ChatGPT Apps SDK with ChatGPT Codex.

## Project Overview & Architecture

This project demonstrates how a conventional web application can be incrementally evolved into a **ChatGPT-native App** using the **Model Context Protocol (MCP)**. The architecture is deliberately split into independent components with clear responsibilities: a web frontend, a backend system of record, and an MCP server acting as an AI adapter. Each component can be developed, tested, and reasoned about in isolation while sharing a common domain model. The same backend APIs are consumed by both human-facing UIs and AI-facing integrations, ensuring consistency and reuse.

### Frontend
The frontend is a modern Angular web application that provides a human-facing UI for managing incidents and runbooks. It implements routing, forms, and basic UX flows and is end-to-end tested using Playwright. In early stages it persists state locally, and in later stages it consumes backend APIs without changing the user experience. This demonstrates a standard web client that remains useful even after AI integration is introduced.

The frontend has been developed with [this prompt](./docs/prompt_stage_2.md)

### Backend
The backend is implemented using FastAPI and acts as the authoritative system of record. It exposes a versioned REST API, persists state to a temporary filesystem-backed JSON file, and automatically publishes OpenAPI documentation. Business logic, persistence, and API routing are clearly separated and covered by unit and integration tests. The backend is designed to be consumed equally by the frontend and the MCP server.

The backend has been developed with [this prompt](./docs/prompt_stage_3.md)


### MCP Server
The MCP server is a separate Python process that bridges the backend application into AI systems using MCP. It communicates with the backend exclusively over HTTP and exposes structured tools and resources without embedding business logic. In later stages it also exposes UI resources that allow ChatGPT to render interactive HTML widgets. This separation keeps AI concerns isolated while enabling rich integrations.

The MCP server has been developed with [this prompt](./docs/prompt_stage_4.md). Then the ChatGPT Apps SDK specifics were added with [this prompt](./docs/prompt_stage_5.md)

### Repository Structure
- `frontend/` — Angular application (Stage 3 scope).
- `backend/` — FastAPI service with file persistence (Stage 3).
- `mcp/` — MCP server (Stage 4) for read-only tool access.
- `docs/` — Architecture notes, prompts and demo scripts.

The instructions on how to run the components can be found in the `README.md` files of the repective subfolders:

## Staged Development Approach

### Stage 1 — Repository Initialization
The first stage establishes the repository structure, documentation, and development conventions. No application code is written at this point. The goal is to create a clear foundation that supports incremental development and AI-assisted contributions without ambiguity.

Created with [this prompt](./docs/prompt_stage_1.md)

### Stage 2 — Frontend MVP
In Stage 2, a standalone Angular frontend is implemented with local browser persistence. Incidents and runbooks can be created, viewed, and edited through a simple UI, and behavior is verified using Playwright end-to-end tests. This stage focuses on UX, routing, and data modeling without backend dependencies.

Created with [this prompt](./docs/prompt_stage_2.md)

### Stage 3 — Backend Introduction
Stage 3 introduces a FastAPI backend that replaces local frontend persistence. The backend becomes the system of record, persisting state to the filesystem and exposing a REST API with OpenAPI documentation. The frontend is updated to use this API without changing its behavior, and backend logic is covered by unit and integration tests.

Created with [this prompt](./docs/prompt_stage_3.md)

### Stage 4 — MCP Server (Tools)
In Stage 4, a dedicated MCP server is added as a separate process. It exposes read-only tools for incidents and runbooks by calling the backend API and can be inspected visually using MCP Inspector. This stage enables safe, testable AI access to application data without UI or write capabilities.

Created with [this prompt](./docs/prompt_stage_4.md)

### Stage 5 — ChatGPT App Integration
Stage 5 extends the MCP server with UI resources that allow ChatGPT to render interactive widgets directly in conversations. Tools are explicitly linked to UI templates using structured metadata, following the ChatGPT Apps SDK pattern. This final stage demonstrates a full ChatGPT-native application built on top of an existing web and API architecture.

Created with [this prompt](./docs/prompt_stage_5.md)

Widget resources:
- Incident list widget (`ui://widget/incident-list.html`)
- Incident detail widget (`ui://widget/incident-detail.html`)
- Runbook list widget (`ui://widget/runbook-list.html`)
- Runbook detail widget (`ui://widget/runbook-detail.html`)

---

# TODO: This need to be moved to the individual readmes of the components

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

In case you want to test from ChatGPT client, start ngrok to expose
local MCP server to internet. Make sure the env variable `NGROK_AUTHTOKEN` is set.
As this token does not change frequently you can include it in your `.zshrc` or
equivalent.

```bash
ngrok http 8090
```

### Typical Local Flow
1. Start the backend.
2. Start the MCP server.
2. Optinally start ngrok.
3. Optionally run the frontend.

### MCP Integration Tests
```bash
cd mcp
poetry install --no-root --extras dev
poetry run pytest
```

### ChatGPT App (Developer Mode)
1. Start the backend and MCP server.
2. (Optional) Run the MCP Inspector to verify tools/resources (see below).
3. In ChatGPT Developer Mode, create a new app and point to:
   - MCP Server URL: `https://YOUR_PUBLIC_URL/mcp`
   - Auth: none
4. When calling widget tools, ChatGPT fetches the widget HTML via MCP 
   resources and renders the UI directly inside the chat experience.

### MCP Inspector Tests
```bash
npx @modelcontextprotocol/inspector
```

Now configure the server in the MCP Inspector UI with the URL 
`http://localhost:8090/mcp` or when using ngrok you can also use the ngrok URL 
`https://<generated>.ngrok-free.dev/mcp` Do not forget to copy the session proxy token
from the log of the MCP Inspector in the UI.

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
The dev server will be available at `http://localhost:4200` and will 
call the backend at `http://localhost:8000/api/v1`.

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
- Stage 5 adds ChatGPT-native integration with widget resources and widget tools.
- Keep changes incremental and avoid implementing future-stage features early.

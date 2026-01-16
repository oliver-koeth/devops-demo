# DevOps Demo Application (Staged Repository)

## Purpose
This repository provides a clean, staged starting point for a DevOps-focused demo application. The goal is to incrementally build a modern web application and supporting services while showcasing DevOps practices such as structured planning, clear boundaries between stages, and maintainable repository organization.

## Roadmap (Staged, No Implementation Yet)
1. **Stage 0 (This repo state)**: Initialize project structure and documentation only.
2. **Stage 1**: Add a modern Angular frontend that stores demo data in browser local storage.
3. **Stage 2**: Introduce a Python backend service that persists data to the filesystem.
4. **Stage 3**: Add an MCP server exposing search over incident data.
5. **Stage 4**: Integrate with a native ChatGPT app via MCP with UI resources.

## Current Scope (Stage 0)
- Repository structure and documentation only.
- No application code, UI screens, backend APIs, or MCP server code.
- No scaffolding for Angular or Python projects yet.

## Out of Scope (For Now)
- Implementing any frontend UI.
- Implementing any backend services.
- Implementing MCP server functionality.
- Adding build tooling, dependencies, or CI/CD pipelines.

## Repository Structure
- `frontend/` — Placeholder for the Angular app (to be added later).
- `backend/` — Placeholder for the Python service (to be added later).
- `mcp/` — Placeholder for MCP server code (to be added later).
- `docs/` — Architecture notes, prompting strategy, and demo scripts.

## Working Agreements
- Keep changes small and incremental.
- Do not implement future stages early.
- Prefer clear, minimal documentation over premature code.

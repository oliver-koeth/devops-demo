# Agent Guidance

This repository is being built in **small, staged steps**. All contributors (including AI agents) must keep changes minimal, scoped, and aligned to the current stage.

## How to Work Here
- Make changes in **small, incremental steps**.
- Do **not** implement future-stage features early.
- Prefer documentation and structure over premature code.
- If unsure, add a short note to `docs/` rather than writing code.

## Stage Discipline

- **Stage 3**: Angular frontend backed by a FastAPI service with file-based persistence.
- **Stage 4 (current)** will add an MCP server.
- Stage 5 will add ChatGPT-native integration.
- If a request conflicts with the current stage, flag it clearly and stop.

## Stage Extensions
- For Stage 4+, avoid MCP work unless explicitly requested.
- Prefer to extend documentation in `docs/` when uncertain.

## Stage 4 MCP Conventions
- MCP server must call the backend via HTTP API only (no in-process imports from backend services).
- MCP tools are read-only in Stage 4.
- Keep MCP tool schemas stable to support Stage 5 resources.

## Backend Conventions (Stage 3)
- Keep routers thin; no direct file writes from API routes.
- Use services + persistence abstractions for business logic.
- Use Pydantic models for all input/output schemas.
- Keep API versioning under `/api/v1`.

## Output Expectations
- Keep repository changes clean and professional.
- Avoid scaffolding tools until explicitly requested in a later stage.

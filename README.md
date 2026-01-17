# DevOps Runbook Assistant (Stage 2)

## Purpose
This repository contains a staged demo application. The current stage delivers a standalone Angular MVP that stores data in browser localStorage and supports incident + runbook workflows for a DevOps runbook assistant.

## Current Scope (Stage 2)
- Angular frontend in `frontend/` using standalone components and Angular router.
- localStorage persistence with schema versioning and seed data.
- Playwright E2E tests for core workflows.

## Out of Scope (Not Yet Implemented)
- Python backend service (Stage 3).
- MCP server and ChatGPT-native integration (Stages 4/5).
- Deployment tooling.

## Repository Structure
- `frontend/` — Angular application (Stage 2 scope).
- `backend/` — Placeholder for Python service (Stage 3).
- `mcp/` — Placeholder for MCP server code (Stage 4/5).
- `docs/` — Architecture notes and demo scripts.

## Run the App (Frontend)
```bash
cd frontend
npm install
npm run start
```
The dev server will be available at `http://localhost:4200`.

## Run Playwright Tests
```bash
cd frontend
npm install
npx playwright install --with-deps
npm run test
```

## Build Production Bundle
```bash
cd frontend
npm install
npm run build
```

## Staged Development Notes
- Stage 3 will introduce a Python backend and remove localStorage.
- Stage 4/5 will add an MCP server and ChatGPT-native integration.
- Keep changes incremental and avoid implementing future-stage features early.

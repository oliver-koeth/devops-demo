# Backend (FastAPI)

## Overview
The backend is a FastAPI service that acts as the system of record for incidents and runbooks. It exposes a versioned REST API and persists state to a local JSON file.

## Prerequisites
- Python 3.11+
- Poetry

## Install Dependencies
```bash
cd backend
poetry install
```

## Run (Dev Server)
```bash
cd backend
poetry run uvicorn app.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000`.

### Persistence
By default, state is stored at `backend/.tmp/state.json`. Set `BACKEND_STATE_PATH` to override the location (useful for tests).

## Test
```bash
cd backend
poetry install
poetry run pytest
```

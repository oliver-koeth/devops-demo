import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, incidents, runbooks
from app.core.config import DEFAULT_STATE_PATH, STATE_PATH_ENV
from app.persistence.file_store import FileStateStore
from app.seed.data import seed_state
from app.services.incidents import IncidentService
from app.services.runbooks import RunbookService


def create_app(state_path: Path | None = None) -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    app = FastAPI(title="DevOps Runbook Assistant API", version="1.0.0")

    env_state_path = os.getenv(STATE_PATH_ENV)
    resolved_state_path = state_path or (Path(env_state_path) if env_state_path else None)
    store = FileStateStore(path=resolved_state_path or DEFAULT_STATE_PATH, seed_provider=seed_state)
    app.state.incident_service = IncidentService(store)
    app.state.runbook_service = RunbookService(store)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(health.router)
    app.include_router(incidents.router, prefix="/api/v1")
    app.include_router(runbooks.router, prefix="/api/v1")

    return app


app = create_app()

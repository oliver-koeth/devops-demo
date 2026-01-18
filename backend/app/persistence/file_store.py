import json
import logging
from pathlib import Path
from typing import Callable

from app.models.state import AppState


class FileStateStore:
    def __init__(self, path: Path, seed_provider: Callable[[], AppState], logger: logging.Logger | None = None):
        self._path = path
        self._seed_provider = seed_provider
        self._logger = logger or logging.getLogger(__name__)
        self._state = self._load_or_seed()

    def get_state(self) -> AppState:
        return self._state

    def save_state(self, state: AppState) -> None:
        self._state = state
        self._write_state(state)

    def _load_or_seed(self) -> AppState:
        if self._path.exists():
            try:
                raw = json.loads(self._path.read_text(encoding="utf-8"))
                state = AppState.model_validate(raw)
                return state
            except Exception as exc:  # noqa: BLE001 - log and reset to seed data
                self._logger.warning("State file invalid, resetting to seed data: %s", exc)
        state = self._seed_provider()
        self._write_state(state)
        return state

    def _write_state(self, state: AppState) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = state.model_dump(mode="json")
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

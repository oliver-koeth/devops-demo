from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models.runbook import Runbook, RunbookCreate, RunbookUpdate
from app.persistence.file_store import FileStateStore


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _matches_term(value: str, term: Optional[str]) -> bool:
    if not term:
        return True
    return term.lower() in value.lower()


class RunbookService:
    def __init__(self, store: FileStateStore):
        self._store = store

    def list_runbooks(self, q: Optional[str] = None, tag: Optional[str] = None) -> list[Runbook]:
        runbooks = self._store.get_state().runbooks
        filtered = [
            runbook
            for runbook in runbooks
            if _matches_term(runbook.title, q)
            or any(_matches_term(tag_value, q) for tag_value in runbook.tags)
        ]
        if tag:
            filtered = [runbook for runbook in filtered if tag in runbook.tags]
        return sorted(filtered, key=lambda runbook: runbook.updatedAt, reverse=True)

    def get_runbook(self, runbook_id: str) -> Runbook:
        for runbook in self._store.get_state().runbooks:
            if runbook.id == runbook_id:
                return runbook
        raise KeyError(runbook_id)

    def create_runbook(self, payload: RunbookCreate) -> Runbook:
        now = _now_iso()
        runbook = Runbook(
            id=str(uuid4()),
            title=payload.title,
            tags=payload.tags,
            content=payload.content,
            createdAt=now,
            updatedAt=now,
        )
        state = self._store.get_state()
        state.runbooks.insert(0, runbook)
        self._store.save_state(state)
        return runbook

    def update_runbook(self, runbook_id: str, payload: RunbookUpdate) -> Runbook:
        state = self._store.get_state()
        for index, runbook in enumerate(state.runbooks):
            if runbook.id == runbook_id:
                updated = runbook.model_copy(
                    update={
                        "title": payload.title or runbook.title,
                        "tags": payload.tags if payload.tags is not None else runbook.tags,
                        "content": payload.content or runbook.content,
                        "updatedAt": _now_iso(),
                    }
                )
                state.runbooks[index] = updated
                self._store.save_state(state)
                return updated
        raise KeyError(runbook_id)

    def delete_runbook(self, runbook_id: str) -> None:
        state = self._store.get_state()
        next_runbooks = [runbook for runbook in state.runbooks if runbook.id != runbook_id]
        if len(next_runbooks) == len(state.runbooks):
            raise KeyError(runbook_id)
        state.runbooks = next_runbooks
        self._store.save_state(state)

from pathlib import Path

from app.models.runbook import RunbookCreate, RunbookUpdate
from app.persistence.file_store import FileStateStore
from app.seed.data import seed_state
from app.services.runbooks import RunbookService


def _build_service(tmp_path: Path) -> RunbookService:
    state_path = tmp_path / "state.json"
    store = FileStateStore(state_path, seed_state)
    return RunbookService(store)


def test_create_update_delete_runbook(tmp_path: Path) -> None:
    service = _build_service(tmp_path)
    state_path = tmp_path / "state.json"

    initial_contents = state_path.read_text(encoding="utf-8")
    created = service.create_runbook(
        RunbookCreate(title="API rollback", tags=["release"], content="Rollback steps")
    )
    assert created.title == "API rollback"
    after_create = state_path.read_text(encoding="utf-8")
    assert after_create != initial_contents

    updated = service.update_runbook(
        created.id,
        RunbookUpdate(title="API rollback guide", tags=["release", "rollback"], content="Steps"),
    )
    assert updated.tags == ["release", "rollback"]
    after_update = state_path.read_text(encoding="utf-8")
    assert after_update != after_create

    service.delete_runbook(created.id)
    assert all(runbook.id != created.id for runbook in service.list_runbooks())


def test_list_filters(tmp_path: Path) -> None:
    service = _build_service(tmp_path)
    filtered = service.list_runbooks(q="database")
    assert any("Database" in runbook.title for runbook in filtered)

    tag_filtered = service.list_runbooks(tag="redis")
    assert all("redis" in runbook.tags for runbook in tag_filtered)

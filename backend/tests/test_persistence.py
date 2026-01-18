import json
from pathlib import Path

from app.persistence.file_store import FileStateStore
from app.seed.data import seed_state


def test_store_seeds_when_missing(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    store = FileStateStore(state_path, seed_state)

    assert state_path.exists()
    assert store.get_state().schemaVersion == 1


def test_store_resets_when_corrupt(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    state_path.write_text("not-json", encoding="utf-8")

    store = FileStateStore(state_path, seed_state)

    payload = json.loads(state_path.read_text(encoding="utf-8"))
    assert payload["schemaVersion"] == 1
    assert store.get_state().schemaVersion == 1

import json
from pathlib import Path

from app.models.incident import IncidentCreate, IncidentNoteCreate, IncidentUpdate
from app.persistence.file_store import FileStateStore
from app.seed.data import seed_state
from app.services.incidents import IncidentService


def _build_service(tmp_path: Path) -> tuple[IncidentService, Path]:
    state_path = tmp_path / "state.json"
    store = FileStateStore(state_path, seed_state)
    return IncidentService(store), state_path


def test_create_update_delete_incident(tmp_path: Path) -> None:
    service, state_path = _build_service(tmp_path)

    initial_contents = state_path.read_text(encoding="utf-8")
    created = service.create_incident(
        IncidentCreate(title="API outage", severity="P2", status="Open", service="Gateway")
    )
    assert created.title == "API outage"
    after_create = state_path.read_text(encoding="utf-8")
    assert after_create != initial_contents

    updated = service.update_incident(
        created.id,
        IncidentUpdate(title="API outage resolved", severity="P3", status="Closed", service="Gateway"),
    )
    assert updated.status == "Closed"
    after_update = state_path.read_text(encoding="utf-8")
    assert after_update != after_create

    service.delete_incident(created.id)
    assert all(incident.id != created.id for incident in service.list_incidents())
    assert json.loads(state_path.read_text(encoding="utf-8"))["incidents"]


def test_add_note_and_status_updates(tmp_path: Path) -> None:
    service, _ = _build_service(tmp_path)
    incident = service.list_incidents()[0]

    updated = service.add_note(incident.id, IncidentNoteCreate(author="SRE", text="Investigating"))
    assert updated.notes[-1].author == "SRE"

    closed = service.close_incident(incident.id)
    assert closed.status == "Closed"

    reopened = service.reopen_incident(incident.id)
    assert reopened.status == "Open"


def test_list_filters(tmp_path: Path) -> None:
    service, _ = _build_service(tmp_path)
    all_incidents = service.list_incidents()
    assert all_incidents

    filtered = service.list_incidents(q="checkout")
    assert any("Checkout" in incident.title for incident in filtered)

    status_filtered = service.list_incidents(status="Closed")
    assert all(incident.status == "Closed" for incident in status_filtered)

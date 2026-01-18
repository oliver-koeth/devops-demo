from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def _client(tmp_path: Path) -> TestClient:
    app = create_app(state_path=tmp_path / "state.json")
    return TestClient(app)


def test_health_and_openapi(tmp_path: Path) -> None:
    client = _client(tmp_path)
    assert client.get("/healthz").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_incident_flow(tmp_path: Path) -> None:
    client = _client(tmp_path)

    create_response = client.post(
        "/api/v1/incidents",
        json={"title": "API outage", "severity": "P2", "status": "Open", "service": "Gateway"},
    )
    assert create_response.status_code == 201
    incident_id = create_response.json()["id"]

    detail = client.get(f"/api/v1/incidents/{incident_id}")
    assert detail.status_code == 200

    update = client.put(
        f"/api/v1/incidents/{incident_id}",
        json={"title": "API outage resolved", "severity": "P3", "status": "Closed"},
    )
    assert update.status_code == 200

    note = client.post(
        f"/api/v1/incidents/{incident_id}/notes",
        json={"author": "SRE", "text": "Investigating"},
    )
    assert note.status_code == 200

    close = client.post(f"/api/v1/incidents/{incident_id}/close")
    assert close.status_code == 200
    assert close.json()["status"] == "Closed"

    reopen = client.post(f"/api/v1/incidents/{incident_id}/reopen")
    assert reopen.status_code == 200
    assert reopen.json()["status"] == "Open"

    delete = client.delete(f"/api/v1/incidents/{incident_id}")
    assert delete.status_code == 204


def test_runbook_flow_and_filters(tmp_path: Path) -> None:
    client = _client(tmp_path)

    create_response = client.post(
        "/api/v1/runbooks",
        json={"title": "API rollback", "tags": ["release"], "content": "Rollback steps"},
    )
    assert create_response.status_code == 201
    runbook_id = create_response.json()["id"]

    detail = client.get(f"/api/v1/runbooks/{runbook_id}")
    assert detail.status_code == 200

    update = client.put(
        f"/api/v1/runbooks/{runbook_id}",
        json={"title": "API rollback guide", "tags": ["release", "rollback"], "content": "Steps"},
    )
    assert update.status_code == 200

    list_response = client.get("/api/v1/runbooks", params={"q": "rollback"})
    assert list_response.status_code == 200

    delete = client.delete(f"/api/v1/runbooks/{runbook_id}")
    assert delete.status_code == 204

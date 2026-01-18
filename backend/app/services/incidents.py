from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models.incident import Incident, IncidentCreate, IncidentNote, IncidentNoteCreate, IncidentUpdate
from app.persistence.file_store import FileStateStore


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _matches_term(value: str, term: Optional[str]) -> bool:
    if not term:
        return True
    return term.lower() in value.lower()


class IncidentService:
    def __init__(self, store: FileStateStore):
        self._store = store

    def list_incidents(
        self,
        q: Optional[str] = None,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        service: Optional[str] = None,
    ) -> list[Incident]:
        incidents = self._store.get_state().incidents
        filtered = [
            incident
            for incident in incidents
            if _matches_term(incident.title, q)
            or _matches_term(incident.service, q)
        ]
        if status:
            filtered = [incident for incident in filtered if incident.status == status]
        if severity:
            filtered = [incident for incident in filtered if incident.severity == severity]
        if service:
            filtered = [incident for incident in filtered if incident.service == service]
        return sorted(filtered, key=lambda incident: incident.createdAt, reverse=True)

    def get_incident(self, incident_id: str) -> Incident:
        for incident in self._store.get_state().incidents:
            if incident.id == incident_id:
                return incident
        raise KeyError(incident_id)

    def create_incident(self, payload: IncidentCreate) -> Incident:
        now = _now_iso()
        incident = Incident(
            id=str(uuid4()),
            title=payload.title,
            severity=payload.severity,
            status=payload.status,
            service=payload.service,
            createdAt=now,
            updatedAt=now,
            notes=[],
        )
        state = self._store.get_state()
        state.incidents.insert(0, incident)
        self._store.save_state(state)
        return incident

    def update_incident(self, incident_id: str, payload: IncidentUpdate) -> Incident:
        state = self._store.get_state()
        for index, incident in enumerate(state.incidents):
            if incident.id == incident_id:
                updated = incident.model_copy(
                    update={
                        "title": payload.title or incident.title,
                        "service": payload.service or incident.service,
                        "severity": payload.severity or incident.severity,
                        "status": payload.status or incident.status,
                        "updatedAt": _now_iso(),
                    }
                )
                state.incidents[index] = updated
                self._store.save_state(state)
                return updated
        raise KeyError(incident_id)

    def delete_incident(self, incident_id: str) -> None:
        state = self._store.get_state()
        next_incidents = [incident for incident in state.incidents if incident.id != incident_id]
        if len(next_incidents) == len(state.incidents):
            raise KeyError(incident_id)
        state.incidents = next_incidents
        self._store.save_state(state)

    def add_note(self, incident_id: str, payload: IncidentNoteCreate) -> Incident:
        state = self._store.get_state()
        for index, incident in enumerate(state.incidents):
            if incident.id == incident_id:
                note = IncidentNote(timestamp=_now_iso(), author=payload.author, text=payload.text)
                updated = incident.model_copy(
                    update={
                        "notes": [*incident.notes, note],
                        "updatedAt": _now_iso(),
                    }
                )
                state.incidents[index] = updated
                self._store.save_state(state)
                return updated
        raise KeyError(incident_id)

    def close_incident(self, incident_id: str) -> Incident:
        return self._set_status(incident_id, "Closed")

    def reopen_incident(self, incident_id: str) -> Incident:
        return self._set_status(incident_id, "Open")

    def _set_status(self, incident_id: str, status: str) -> Incident:
        state = self._store.get_state()
        for index, incident in enumerate(state.incidents):
            if incident.id == incident_id:
                updated = incident.model_copy(update={"status": status, "updatedAt": _now_iso()})
                state.incidents[index] = updated
                self._store.save_state(state)
                return updated
        raise KeyError(incident_id)

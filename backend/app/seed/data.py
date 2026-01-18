from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.config import SCHEMA_VERSION
from app.models.incident import Incident, IncidentNote
from app.models.runbook import Runbook
from app.models.state import AppState


def _isoformat(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def seed_state() -> AppState:
    now = datetime.now(timezone.utc)
    incident_created = _isoformat(now - timedelta(hours=5))
    incident_updated = _isoformat(now - timedelta(hours=2))
    secondary_created = _isoformat(now - timedelta(hours=24))

    incidents = [
        Incident(
            id=str(uuid4()),
            title="Checkout latency spikes in us-east-1",
            severity="P1",
            status="Open",
            service="Payments API",
            createdAt=incident_created,
            updatedAt=incident_updated,
            notes=[
                IncidentNote(
                    timestamp=incident_created,
                    author="On-call Bot",
                    text="Pager triggered for elevated latency. Investigating recent deploy.",
                ),
                IncidentNote(
                    timestamp=incident_updated,
                    author="A. Rivera",
                    text="Rolled back to 2024.08.12 build; seeing partial recovery.",
                ),
            ],
        ),
        Incident(
            id=str(uuid4()),
            title="CI queue backlog for staging",
            severity="P3",
            status="Closed",
            service="CI Orchestrator",
            createdAt=secondary_created,
            updatedAt=secondary_created,
            notes=[
                IncidentNote(
                    timestamp=secondary_created,
                    author="L. Chen",
                    text="Scaled runners and cleared backlog. Monitoring for recurrence.",
                )
            ],
        ),
    ]

    runbooks = [
        Runbook(
            id=str(uuid4()),
            title="Database failover checklist",
            tags=["database", "failover", "postgres"],
            content=(
                "1. Confirm replica health\n"
                "2. Pause write-heavy jobs\n"
                "3. Promote replica\n"
                "4. Validate app connectivity"
            ),
            createdAt=secondary_created,
            updatedAt=secondary_created,
        ),
        Runbook(
            id=str(uuid4()),
            title="Cache eviction response",
            tags=["cache", "redis"],
            content=(
                "If cache eviction storms occur:\n"
                "- Increase memory threshold\n"
                "- Review key TTLs\n"
                "- Enable lazy freeing"
            ),
            createdAt=incident_created,
            updatedAt=incident_created,
        ),
    ]

    return AppState(schemaVersion=SCHEMA_VERSION, incidents=incidents, runbooks=runbooks)

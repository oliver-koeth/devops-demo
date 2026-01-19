from __future__ import annotations

from dataclasses import dataclass, field

import httpx

from app.core import API_PREFIX, DEFAULT_TIMEOUT_SECONDS, get_backend_base_url


class BackendUnavailableError(RuntimeError):
    pass


class BackendNotFoundError(RuntimeError):
    pass


@dataclass
class BackendClient:
    base_url: str = field(default_factory=get_backend_base_url)
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}{API_PREFIX}{path}"

    async def _get(self, path: str, params: dict[str, str] | None = None) -> object:
        url = self._build_url(path)
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.get(url, params=params)
        except httpx.RequestError as exc:
            raise BackendUnavailableError("backend unavailable") from exc

        if response.status_code == 404:
            raise BackendNotFoundError("not found")

        response.raise_for_status()
        return response.json()

    async def list_incidents(self, params: dict[str, str] | None = None) -> list[dict]:
        data = await self._get("/incidents", params=params)
        return list(data)

    async def get_incident(self, incident_id: str) -> dict:
        data = await self._get(f"/incidents/{incident_id}")
        return dict(data)

    async def list_runbooks(self, params: dict[str, str] | None = None) -> list[dict]:
        data = await self._get("/runbooks", params=params)
        return list(data)

    async def get_runbook(self, runbook_id: str) -> dict:
        data = await self._get(f"/runbooks/{runbook_id}")
        return dict(data)

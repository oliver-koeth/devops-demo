import json
import os
import socket
import subprocess
import sys
import time
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path

import httpx
import pytest
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
MCP_DIR = REPO_ROOT / "mcp"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _wait_for_backend(base_url: str, timeout_seconds: float = 10.0) -> None:
    deadline = time.time() + timeout_seconds
    url = f"{base_url}/healthz"
    while time.time() < deadline:
        try:
            response = httpx.get(url, timeout=1.0)
            if response.status_code == 200:
                return
        except httpx.RequestError:
            pass
        time.sleep(0.2)
    raise RuntimeError("Backend did not become ready in time")


def _wait_for_mcp(base_url: str, timeout_seconds: float = 10.0) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            response = httpx.get(base_url, timeout=1.0)
            if response.status_code < 500:
                return
        except httpx.RequestError:
            pass
        time.sleep(0.2)
    raise RuntimeError("MCP server did not become ready in time")


@pytest.fixture(scope="session")
def backend_url(tmp_path_factory: pytest.TempPathFactory) -> str:
    port = _find_free_port()
    base_url = f"http://127.0.0.1:{port}"
    state_path = tmp_path_factory.mktemp("backend-state") / "state.json"

    env = os.environ.copy()
    env["BACKEND_STATE_PATH"] = str(state_path)

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=BACKEND_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        _wait_for_backend(base_url)
        yield base_url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@contextmanager
def _mcp_server(backend_url: str):
    port = _find_free_port()
    base_url = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    env["BACKEND_BASE_URL"] = backend_url
    env["MCP_HOST"] = "127.0.0.1"
    env["MCP_PORT"] = str(port)

    process = subprocess.Popen(
        [sys.executable, "-m", "app.main"],
        cwd=MCP_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        _wait_for_mcp(base_url)
        yield base_url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture(scope="session")
def mcp_url(backend_url: str) -> str:
    with _mcp_server(backend_url) as base_url:
        yield base_url


@asynccontextmanager
async def _mcp_session(mcp_base_url: str):
    async with streamable_http_client(mcp_base_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


def _extract_payload(result):
    structured = getattr(result, "structured_content", None)
    if structured is not None:
        return structured
    content = getattr(result, "content", None) or []
    if content:
        first = content[0]
        text = getattr(first, "text", None)
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    return result


def _as_dict(item):
    if hasattr(item, "model_dump"):
        return item.model_dump()
    if hasattr(item, "dict"):
        return item.dict()
    return item


@pytest.mark.asyncio
async def test_list_incidents_returns_seeded_data(mcp_url: str) -> None:
    async with _mcp_session(mcp_url) as session:
        result = await session.call_tool("list_incidents", {})
        payload = _extract_payload(result)
        assert isinstance(payload, list)
        assert len(payload) >= 2


@pytest.mark.asyncio
async def test_get_incident_returns_expected_incident(mcp_url: str) -> None:
    async with _mcp_session(mcp_url) as session:
        list_result = await session.call_tool("list_incidents", {})
        incidents = [_as_dict(item) for item in _extract_payload(list_result)]
        incident_id = incidents[0]["id"]

        result = await session.call_tool("get_incident", {"incident_id": incident_id})
        payload = _as_dict(_extract_payload(result))
        assert payload["id"] == incident_id


@pytest.mark.asyncio
async def test_list_runbooks_returns_seeded_data(mcp_url: str) -> None:
    async with _mcp_session(mcp_url) as session:
        result = await session.call_tool("list_runbooks", {})
        payload = _extract_payload(result)
        assert isinstance(payload, list)
        assert len(payload) >= 2


@pytest.mark.asyncio
async def test_get_runbook_returns_expected_runbook(mcp_url: str) -> None:
    async with _mcp_session(mcp_url) as session:
        list_result = await session.call_tool("list_runbooks", {})
        runbooks = [_as_dict(item) for item in _extract_payload(list_result)]
        runbook_id = runbooks[0]["id"]

        result = await session.call_tool("get_runbook", {"runbook_id": runbook_id})
        payload = _as_dict(_extract_payload(result))
        assert payload["id"] == runbook_id


@pytest.mark.asyncio
async def test_get_incident_unknown_id_returns_not_found(mcp_url: str) -> None:
    async with _mcp_session(mcp_url) as session:
        with pytest.raises(Exception) as excinfo:
            await session.call_tool("get_incident", {"incident_id": "missing-id"})
        assert "not found" in str(excinfo.value).lower()


@pytest.mark.asyncio
async def test_backend_unavailable_returns_error() -> None:
    unavailable_port = _find_free_port()
    backend_url = f"http://127.0.0.1:{unavailable_port}"
    with _mcp_server(backend_url) as base_url:
        async with _mcp_session(base_url) as session:
            with pytest.raises(Exception) as excinfo:
                await session.call_tool("list_incidents", {})
            assert "backend unavailable" in str(excinfo.value).lower()

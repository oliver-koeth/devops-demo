import os

API_PREFIX = "/api/v1"
DEFAULT_BACKEND_BASE_URL = "http://localhost:8000"
DEFAULT_TIMEOUT_SECONDS = 5.0
BACKEND_BASE_URL_ENV = "BACKEND_BASE_URL"
MCP_HOST_ENV = "MCP_HOST"
MCP_PORT_ENV = "MCP_PORT"
DEFAULT_MCP_HOST = "127.0.0.1"
DEFAULT_MCP_PORT = 8090


def get_backend_base_url() -> str:
    return os.getenv(BACKEND_BASE_URL_ENV, DEFAULT_BACKEND_BASE_URL).rstrip("/")


def get_mcp_host() -> str:
    return os.getenv(MCP_HOST_ENV, DEFAULT_MCP_HOST)


def get_mcp_port() -> int:
    value = os.getenv(MCP_PORT_ENV)
    if not value:
        return DEFAULT_MCP_PORT
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Invalid {MCP_PORT_ENV}: {value}") from exc

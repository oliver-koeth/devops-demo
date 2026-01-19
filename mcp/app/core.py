import os

API_PREFIX = "/api/v1"
DEFAULT_BACKEND_BASE_URL = "http://localhost:8000"
DEFAULT_TIMEOUT_SECONDS = 5.0
BACKEND_BASE_URL_ENV = "BACKEND_BASE_URL"


def get_backend_base_url() -> str:
    return os.getenv(BACKEND_BASE_URL_ENV, DEFAULT_BACKEND_BASE_URL).rstrip("/")

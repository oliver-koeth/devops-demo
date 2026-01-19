from pathlib import Path

SCHEMA_VERSION = 1
STATE_PATH_ENV = "BACKEND_STATE_PATH"
DEFAULT_STATE_PATH = Path(__file__).resolve().parents[2] / ".tmp" / "state.json"

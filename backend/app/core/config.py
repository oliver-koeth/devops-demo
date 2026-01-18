from pathlib import Path

SCHEMA_VERSION = 1
DEFAULT_STATE_PATH = Path(__file__).resolve().parents[2] / ".tmp" / "state.json"

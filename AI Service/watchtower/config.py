from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "watchtower.db"
DEFAULT_JSONL_DIR = BASE_DIR / "data" / "jsonl"

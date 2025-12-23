from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
QDRANT_DIR = BASE_DIR / "qdrant_db"
CHECKPOINT_DB = BASE_DIR / "memory.db"

UPLOAD_DIR.mkdir(exist_ok=True)
QDRANT_DIR.mkdir(exist_ok=True)

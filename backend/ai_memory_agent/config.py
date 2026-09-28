import os
from datetime import datetime, timezone
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

def utc_now() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)

# Load .env file if available
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseModel):
    # App Settings
    APP_NAME: str = "AI Security Operations & Compliance Memory Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    # Hindsight Memory Configuration
    HINDSIGHT_API_KEY: str = os.getenv("HINDSIGHT_API_KEY", "")
    HINDSIGHT_BASE_URL: str = os.getenv("HINDSIGHT_BASE_URL", "http://localhost:8888")
    HINDSIGHT_BANK_ID: str = os.getenv("HINDSIGHT_BANK_ID", "secops-org-memory")
    # Set to true to enforce local biomimetic engine, or false to attempt live client first
    FORCE_LOCAL_HINDSIGHT: bool = os.getenv("FORCE_LOCAL_HINDSIGHT", "false").lower() in ("true", "1", "yes")

    # Local Storage Configuration
    LOCAL_DB_PATH: Path = DATA_DIR / "hindsight_memory.duckdb"
    LOCAL_JSON_BACKUP: Path = DATA_DIR / "memory_snapshot.json"

    # LLM Provider Configuration
    # Options: "auto", "gemini", "openai", "expert" (offline deterministic security reasoning)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "auto")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()

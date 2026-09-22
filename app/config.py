import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load local environment variables from .env.
# The .env file is ignored by Git and should never be committed.
load_dotenv(PROJECT_ROOT / ".env")


WORKSPACE_DIR = PROJECT_ROOT / "workspace"
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "agent.db"


AGENT_PROVIDER = os.getenv(
    "AGENT_PROVIDER",
    "mock",
).strip().lower()


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    "",
).strip()


OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna",
).strip()
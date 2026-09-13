from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "agent.db"

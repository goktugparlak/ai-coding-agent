from pathlib import Path

from app.config import WORKSPACE_DIR as DEFAULT_WORKSPACE_DIR
from app.exceptions import WorkspaceError

WORKSPACE_DIR = DEFAULT_WORKSPACE_DIR


def get_safe_path(filename: str) -> Path:
    workspace = WORKSPACE_DIR.resolve()
    file_path = (workspace / filename).resolve()

    if file_path != workspace and workspace not in file_path.parents:
        raise WorkspaceError("Path is outside the workspace.")

    return file_path


def list_files() -> list[str]:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

    return sorted(
        path.relative_to(WORKSPACE_DIR).as_posix()
        for path in WORKSPACE_DIR.rglob("*")
        if path.is_file()
    )


def read_file(filename: str) -> str:
    try:
        file_path = get_safe_path(filename)
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: '{filename}' was not found."
    except PermissionError:
        return f"Error: permission denied for '{filename}'."
    except WorkspaceError as error:
        return f"Error: {error}"


def write_file(filename: str, content: str) -> str:
    try:
        file_path = get_safe_path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"Successfully wrote to '{filename}'."
    except PermissionError:
        return f"Error: permission denied for '{filename}'."
    except WorkspaceError as error:
        return f"Error: {error}"

import subprocess
import sys
from pathlib import Path

from app.config import WORKSPACE_DIR as DEFAULT_WORKSPACE_DIR
from app.tools.file_tools import get_safe_path

WORKSPACE_DIR = DEFAULT_WORKSPACE_DIR


def run_python(filename: str, timeout: int = 10) -> str:
    """
    Run one Python file inside the workspace.

    This is intentionally narrower than arbitrary shell execution.
    It is a learning-project safety guard, not a full OS sandbox.
    """
    file_path = get_safe_path(filename)

    if not file_path.exists():
        return f"Error: '{filename}' was not found."

    if file_path.suffix.lower() != ".py":
        return "Error: only Python files can be executed."

    try:
        result = subprocess.run(
            [sys.executable, file_path.name],
            cwd=file_path.parent,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "Error: command timed out."
    except PermissionError:
        return "Error: permission denied while running command."

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if result.returncode == 0:
        return stdout or "Command completed successfully with no output."

    return stderr or f"Command failed with exit code {result.returncode}."

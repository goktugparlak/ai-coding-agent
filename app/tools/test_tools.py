import subprocess
import sys

from app.config import WORKSPACE_DIR as DEFAULT_WORKSPACE_DIR

WORKSPACE_DIR = DEFAULT_WORKSPACE_DIR


def run_tests(timeout: int = 30) -> str:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "Error: tests timed out."
    except PermissionError:
        return "Error: permission denied while running tests."

    output_parts = [
        part.strip()
        for part in (result.stdout, result.stderr)
        if part and part.strip()
    ]
    output = "\n".join(output_parts)

    if result.returncode == 0:
        return f"Tests passed.\n{output}".strip()

    # pytest exit code 5 means no tests were collected.
    if result.returncode == 5:
        return f"No tests were collected.\n{output}".strip()

    return f"Tests failed.\n{output}".strip()

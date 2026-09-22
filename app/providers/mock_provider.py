from app.providers.base import BaseProvider, ToolExecutor


HELP_TEXT = """Available commands:
- help
- list files
- read <filename>
- inspect <filename>
- write <filename> :: <content>
- run python <filename>
- run tests
- check project
- history

The project supports both deterministic mock mode and a real
OpenAI-powered provider.
"""


def format_tool_result(label: str, result: object) -> str:
    if isinstance(result, list):
        body = "\n".join(f"- {item}" for item in result)
        if not body:
            body = "(empty)"
    else:
        body = str(result)

    return f"{label}\n{body}"


def execute_safely(
    execute_tool: ToolExecutor,
    tool_name: str,
    arguments: dict,
    label: str,
) -> str:
    try:
        result = execute_tool(tool_name, arguments)
        return format_tool_result(label, result)
    except Exception as error:
        return f"{label}\nError: {error}"


class MockProvider(BaseProvider):
    """
    Deterministic provider used for development and automated tests.

    It does not call an external AI API.
    """

    name = "mock"
    llm_connected = False
    model = None

    def run(
        self,
        message: str,
        execute_tool: ToolExecutor,
    ) -> str:

        raw = message.strip()
        normalized = raw.lower()

        if not raw:
            return "Please enter a command."

        if normalized in {"help", "commands", "?"}:
            return HELP_TEXT

        if normalized in {"list files", "files", "ls"}:
            return execute_safely(
                execute_tool,
                "list_files",
                {},
                "Workspace files",
            )

        for prefix in ("read ", "inspect ", "show "):
            if normalized.startswith(prefix):

                filename = raw[len(prefix):].strip()

                if not filename:
                    return "Please provide a filename."

                return execute_safely(
                    execute_tool,
                    "read_file",
                    {"filename": filename},
                    f"Contents of {filename}",
                )

        if normalized.startswith("write "):

            payload = raw[6:].strip()

            if "::" not in payload:
                return "Usage: write <filename> :: <content>"

            filename, content = payload.split("::", 1)

            filename = filename.strip()
            content = content.strip()

            if not filename:
                return "Please provide a filename."

            return execute_safely(
                execute_tool,
                "write_file",
                {
                    "filename": filename,
                    "content": content,
                },
                f"Write {filename}",
            )

        if normalized.startswith("run python "):

            filename = raw[len("run python "):].strip()

            if not filename:
                return "Please provide a Python filename."

            return execute_safely(
                execute_tool,
                "run_python",
                {"filename": filename},
                f"Run {filename}",
            )

        if normalized in {
            "run tests",
            "test",
            "tests",
            "pytest",
        }:

            return execute_safely(
                execute_tool,
                "run_tests",
                {},
                "Test results",
            )

        if normalized in {
            "check project",
            "project status",
            "status",
        }:

            files = execute_safely(
                execute_tool,
                "list_files",
                {},
                "Workspace files",
            )

            tests = execute_safely(
                execute_tool,
                "run_tests",
                {},
                "Test results",
            )

            return (
                "Running a small project check.\n\n"
                f"{files}\n\n"
                f"{tests}"
            )

        if normalized == "history":
            return "__SHOW_HISTORY__"

        return (
            "I do not understand that command yet.\n\n"
            + HELP_TEXT
        )
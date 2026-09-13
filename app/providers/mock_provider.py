import shlex

from app.providers.base import BaseProvider, ProviderPlan, ToolAction


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

This portfolio version uses a deterministic mock provider, not a real LLM.
The provider layer can later be replaced by an OpenAI/local-model provider.
"""


class MockProvider(BaseProvider):
    """
    Deterministic rule-based provider.

    It demonstrates provider abstraction and tool orchestration without
    requiring an API key or paid model.
    """

    def plan(self, message: str) -> ProviderPlan:
        raw = message.strip()
        normalized = raw.lower()

        if not raw:
            return ProviderPlan("Please enter a command.")

        if normalized in {"help", "commands", "?"}:
            return ProviderPlan(HELP_TEXT)

        if normalized in {"list files", "files", "ls"}:
            return ProviderPlan(
                actions=[
                    ToolAction(
                        "list_files",
                        label="Workspace files",
                    )
                ]
            )

        for prefix in ("read ", "inspect ", "show "):
            if normalized.startswith(prefix):
                filename = raw[len(prefix):].strip()
                if not filename:
                    return ProviderPlan("Please provide a filename.")
                return ProviderPlan(
                    actions=[
                        ToolAction(
                            "read_file",
                            {"filename": filename},
                            f"Contents of {filename}",
                        )
                    ]
                )

        if normalized.startswith("write "):
            payload = raw[6:].strip()

            if "::" not in payload:
                return ProviderPlan(
                    "Usage: write <filename> :: <content>"
                )

            filename, content = payload.split("::", 1)
            filename = filename.strip()
            content = content.strip()

            if not filename:
                return ProviderPlan("Please provide a filename.")

            return ProviderPlan(
                actions=[
                    ToolAction(
                        "write_file",
                        {
                            "filename": filename,
                            "content": content,
                        },
                        f"Write {filename}",
                    )
                ]
            )

        if normalized.startswith("run python "):
            filename = raw[len("run python "):].strip()
            if not filename:
                return ProviderPlan("Please provide a Python filename.")
            return ProviderPlan(
                actions=[
                    ToolAction(
                        "run_python",
                        {"filename": filename},
                        f"Run {filename}",
                    )
                ]
            )

        if normalized in {"run tests", "test", "tests", "pytest"}:
            return ProviderPlan(
                actions=[
                    ToolAction(
                        "run_tests",
                        label="Test results",
                    )
                ]
            )

        if normalized in {
            "check project",
            "project status",
            "status",
        }:
            return ProviderPlan(
                message="Running a small project check.",
                actions=[
                    ToolAction(
                        "list_files",
                        label="Workspace files",
                    ),
                    ToolAction(
                        "run_tests",
                        label="Test results",
                    ),
                ],
            )

        if normalized == "history":
            # Agent handles persistence-specific commands.
            return ProviderPlan("__SHOW_HISTORY__")

        return ProviderPlan(
            "I do not understand that command yet.\n\n" + HELP_TEXT
        )

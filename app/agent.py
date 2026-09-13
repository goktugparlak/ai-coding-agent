from app.config import DATABASE_PATH
from app.database import HistoryStore
from app.providers.base import BaseProvider
from app.providers.mock_provider import MockProvider
from app.tools.registry import ToolRegistry


class CodingAgent:
    def __init__(
        self,
        provider: BaseProvider | None = None,
        tools: ToolRegistry | None = None,
        history: HistoryStore | None = None,
    ):
        self.provider = provider or MockProvider()
        self.tools = tools or ToolRegistry()
        self.history = history or HistoryStore(DATABASE_PATH)

    def run(self, message: str) -> str:
        plan = self.provider.plan(message)

        if plan.message == "__SHOW_HISTORY__":
            response = self._format_history()
            self.history.add(message, response)
            return response

        sections: list[str] = []

        if plan.message:
            sections.append(plan.message.strip())

        for action in plan.actions:
            try:
                result = self.tools.execute(
                    action.tool_name,
                    action.arguments,
                )
                sections.append(
                    self._format_tool_result(action.label, result)
                )
            except Exception as error:
                sections.append(
                    f"{action.label or action.tool_name}\n"
                    f"Error: {error}"
                )

        response = "\n\n".join(
            section for section in sections if section
        ).strip()

        if not response:
            response = "No response was produced."

        self.history.add(message, response)
        return response

    def _format_tool_result(self, label: str, result: object) -> str:
        heading = label or "Result"

        if isinstance(result, list):
            body = "\n".join(f"- {item}" for item in result)
            if not body:
                body = "(empty)"
        else:
            body = str(result)

        return f"{heading}\n{body}"

    def _format_history(self) -> str:
        rows = self.history.recent(limit=10)

        if not rows:
            return "No history yet."

        lines = ["Recent history:"]
        for row in reversed(rows):
            lines.append(
                f"- {row['created_at']} | "
                f"You: {row['user_message']} | "
                f"Agent: {row['agent_response'].splitlines()[0]}"
            )

        return "\n".join(lines)

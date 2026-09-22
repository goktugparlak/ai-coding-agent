from app.config import (
    AGENT_PROVIDER,
    DATABASE_PATH,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)
from app.database import HistoryStore
from app.providers.base import BaseProvider
from app.providers.mock_provider import MockProvider
from app.providers.openai_provider import OpenAIProvider
from app.tools.registry import ToolRegistry


def build_default_provider() -> BaseProvider:

    if AGENT_PROVIDER == "mock":
        return MockProvider()

    if AGENT_PROVIDER == "openai":

        if not OPENAI_API_KEY:
            raise RuntimeError(
                "AGENT_PROVIDER is set to 'openai', but "
                "OPENAI_API_KEY is missing."
            )

        return OpenAIProvider(
            api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL,
        )

    raise ValueError(
        f"Unknown AGENT_PROVIDER: {AGENT_PROVIDER}"
    )


class CodingAgent:
    def __init__(
        self,
        provider: BaseProvider | None = None,
        tools: ToolRegistry | None = None,
        history: HistoryStore | None = None,
    ):
        self.provider = provider or build_default_provider()
        self.tools = tools or ToolRegistry()
        self.history = history or HistoryStore(DATABASE_PATH)

    def run(self, message: str) -> str:

        message = message.strip()

        if not message:
            return "Please enter a message."

        try:
            response = self.provider.run(
                message,
                self.tools.execute,
            )

        except Exception as error:
            response = (
                "Provider error: "
                f"{error}"
            )

        if response == "__SHOW_HISTORY__":
            response = self._format_history()

        self.history.add(
            message,
            response,
        )

        return response

    def _format_history(self) -> str:

        rows = self.history.recent(limit=10)

        if not rows:
            return "No history yet."

        lines = ["Recent history:"]

        for row in reversed(rows):

            lines.append(
                f"- {row['created_at']} | "
                f"You: {row['user_message']} | "
                f"Agent: "
                f"{row['agent_response'].splitlines()[0]}"
            )

        return "\n".join(lines)
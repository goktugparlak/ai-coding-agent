from abc import ABC, abstractmethod
from collections.abc import Callable


ToolExecutor = Callable[[str, dict], object]


class BaseProvider(ABC):
    """
    Common interface for all agent providers.

    A provider decides how to respond to a user request and may use
    external tools through the supplied tool executor.
    """

    name = "base"
    llm_connected = False
    model: str | None = None

    @abstractmethod
    def run(
        self,
        message: str,
        execute_tool: ToolExecutor,
    ) -> str:
        raise NotImplementedError
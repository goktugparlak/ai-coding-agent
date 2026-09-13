from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ToolAction:
    tool_name: str
    arguments: dict = field(default_factory=dict)
    label: str = ""


@dataclass
class ProviderPlan:
    message: str = ""
    actions: list[ToolAction] = field(default_factory=list)


class BaseProvider(ABC):
    @abstractmethod
    def plan(self, message: str) -> ProviderPlan:
        """Translate a user message into zero or more tool actions."""
        raise NotImplementedError

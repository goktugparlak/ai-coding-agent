class AgentError(Exception):
    """Base exception for agent-related errors."""


class WorkspaceError(AgentError):
    """Raised when a workspace operation is unsafe or invalid."""


class ToolExecutionError(AgentError):
    """Raised when a tool cannot complete its operation."""

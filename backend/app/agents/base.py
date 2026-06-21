from abc import ABC, abstractmethod

from app.models import AgentMessage, AgentResult


class Agent(ABC):
    """Base interface for every specialist coding assistant agent."""

    @abstractmethod
    async def run(self, message: AgentMessage) -> AgentResult:
        """Process a handoff message and return structured artifacts."""

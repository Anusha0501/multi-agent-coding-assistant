from app.agents.coder import CodingAgent
from app.agents.planner import PlannerAgent
from app.agents.reviewer import ReviewerAgent
from app.agents.tester import TestingAgent
from app.models import AgentMessage, AgentResult, RepositorySnapshot


class AgentOrchestrator:
    """Coordinates sequential specialist agents for a coding task."""

    def __init__(self):
        self.agents = [PlannerAgent(), CodingAgent(), ReviewerAgent(), TestingAgent()]

    async def run(self, task: str, repository: RepositorySnapshot) -> tuple[list[AgentResult], str]:
        artifacts: dict[str, object] = {}
        results: list[AgentResult] = []
        for agent in self.agents:
            result = await agent.run(AgentMessage(task=task, repository=repository, artifacts=artifacts))
            results.append(result)
            artifacts[result.agent.value] = result.artifacts

        final_output = self._final_output(task, results)
        return results, final_output

    def _final_output(self, task: str, results: list[AgentResult]) -> str:
        sections = [f"Completed multi-agent workflow for: {task}"]
        for result in results:
            sections.append(f"- {result.agent.value}: {result.summary} ({result.status})")
        return "\n".join(sections)

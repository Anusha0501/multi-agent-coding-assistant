import asyncio

from app.models import RepositorySnapshot
from app.services.orchestrator import AgentOrchestrator


def test_orchestrator_runs_all_agents():
    repository = RepositorySnapshot(
        url="https://github.com/example/project",
        owner="example",
        name="project",
        files=[],
    )

    results, final_output = asyncio.run(AgentOrchestrator().run("Add a health endpoint", repository))

    assert [result.agent.value for result in results] == ["planner", "coder", "reviewer", "tester"]
    assert "Completed multi-agent workflow" in final_output

from app.agents.base import Agent
from app.models import AgentMessage, AgentName, AgentResult


class TestingAgent(Agent):
    async def run(self, message: AgentMessage) -> AgentResult:
        test_plan = [
            "Run backend unit tests with pytest.",
            "Run frontend build or component tests if UI files changed.",
            "Verify generated patches do not expose secrets or credentials.",
        ]
        generated_test = {
            "path": "assistant_generated/test_plan.md",
            "content": "\n".join(f"- {step}" for step in test_plan),
        }
        return AgentResult(
            agent=AgentName.TESTER,
            status="completed",
            summary="Created a validation plan for the final output.",
            artifacts={"test_plan": test_plan, "generated_tests": [generated_test]},
            handoff="Final output can summarize the plan, implementation, review, and tests.",
        )

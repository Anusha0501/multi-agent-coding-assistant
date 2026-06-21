from app.agents.base import Agent
from app.models import AgentMessage, AgentName, AgentResult


class PlannerAgent(Agent):
    async def run(self, message: AgentMessage) -> AgentResult:
        file_hints = [file.path for file in message.repository.files[:8]]
        plan = [
            "Clarify the requested behavior and acceptance criteria.",
            "Inspect relevant repository files before editing.",
            "Generate the smallest safe implementation patch.",
            "Review the patch for correctness, security, and maintainability.",
            "Create or update tests and provide execution commands.",
        ]
        return AgentResult(
            agent=AgentName.PLANNER,
            status="completed",
            summary="Created an implementation plan and delegation strategy.",
            artifacts={
                "plan": plan,
                "candidate_files": file_hints,
                "delegation": {
                    "coder": "Implement the plan using repository context.",
                    "reviewer": "Critique generated changes and identify risks.",
                    "tester": "Create validation strategy and tests.",
                },
            },
            handoff="Coder should use the plan and candidate files to produce proposed changes.",
        )

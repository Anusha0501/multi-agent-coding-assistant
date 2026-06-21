from app.agents.base import Agent
from app.models import AgentMessage, AgentName, AgentResult


class ReviewerAgent(Agent):
    async def run(self, message: AgentMessage) -> AgentResult:
        proposed_files = message.artifacts.get("coder", {}).get("proposed_files", [])
        findings = []
        if not proposed_files:
            findings.append("No code artifacts were produced by the coding agent.")
        if "test" not in message.task.lower():
            findings.append("Ensure tests are added or updated for the requested behavior.")
        approval = "approved_with_comments" if findings else "approved"
        return AgentResult(
            agent=AgentName.REVIEWER,
            status=approval,
            summary="Reviewed generated artifacts for quality and risk.",
            artifacts={"findings": findings, "risk_score": "medium" if findings else "low"},
            handoff="Tester should convert reviewer findings into executable validation steps.",
        )

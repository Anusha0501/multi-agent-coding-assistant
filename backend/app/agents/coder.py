from app.agents.base import Agent
from app.models import AgentMessage, AgentName, AgentResult


class CodingAgent(Agent):
    async def run(self, message: AgentMessage) -> AgentResult:
        plan = message.artifacts.get("planner", {}).get("plan", [])
        generated = {
            "path": "assistant_generated/implementation_notes.md",
            "content": "\n".join([
                "# Proposed Implementation",
                "",
                f"Task: {message.task}",
                "",
                "## Plan followed",
                *[f"- {step}" for step in plan],
                "",
                "## Patch strategy",
                "- Read the target files from the repository snapshot.",
                "- Make minimal, reviewable changes.",
                "- Add tests that describe public behavior.",
            ]),
        }
        return AgentResult(
            agent=AgentName.CODER,
            status="completed",
            summary="Generated implementation guidance and a proposed artifact.",
            artifacts={"proposed_files": [generated], "notes": "Swap this template with CrewAI/AutoGen LLM tool calls for real patching."},
            handoff="Reviewer should inspect proposed files and verify they satisfy the planner output.",
        )

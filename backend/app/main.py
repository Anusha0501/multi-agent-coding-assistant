from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import RunRequest, RunResponse
from app.services.github import GitHubRepoReader
from app.services.orchestrator import AgentOrchestrator

app = FastAPI(title="Multi-Agent Coding Assistant", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/runs", response_model=RunResponse)
async def create_run(request: RunRequest) -> RunResponse:
    try:
        repository = await GitHubRepoReader().read(str(request.repo_url))
    except Exception as exc:  # noqa: BLE001 - API boundary converts external failures to HTTP errors.
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    results, final_output = await AgentOrchestrator().run(request.task, repository)
    return RunResponse(task=request.task, repository=repository, results=results, final_output=final_output)

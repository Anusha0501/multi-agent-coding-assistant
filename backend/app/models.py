from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class AgentName(str, Enum):
    PLANNER = "planner"
    CODER = "coder"
    REVIEWER = "reviewer"
    TESTER = "tester"


class RepositoryFile(BaseModel):
    path: str
    content: str
    language: str | None = None


class RepositorySnapshot(BaseModel):
    url: HttpUrl
    owner: str
    name: str
    default_branch: str = "main"
    description: str | None = None
    files: list[RepositoryFile] = Field(default_factory=list)


class RunRequest(BaseModel):
    task: str = Field(min_length=5, max_length=4000)
    repo_url: HttpUrl


class AgentMessage(BaseModel):
    task: str
    repository: RepositorySnapshot
    artifacts: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    agent: AgentName
    status: str
    summary: str
    artifacts: dict[str, Any] = Field(default_factory=dict)
    handoff: str


class RunResponse(BaseModel):
    task: str
    repository: RepositorySnapshot
    results: list[AgentResult]
    final_output: str

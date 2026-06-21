# Multi-Agent Coding Assistant

An educational Devin / Cognition / OpenHands-style coding assistant built with **FastAPI**, **React**, and a lightweight agent orchestration layer inspired by CrewAI and AutoGen. The project demonstrates how a task moves through specialist agents:

```text
Task -> Planner Agent -> Coding Agent -> Reviewer Agent -> Testing Agent -> Final Output
```

The implementation is intentionally transparent so you can learn the mechanics behind multi-agent coding systems before swapping in production LLM calls, sandboxed execution, vector search, or full GitHub App authentication.

## What you will learn

### Multi-Agent Systems

A multi-agent system decomposes a complex objective into smaller responsibilities handled by specialized agents. Instead of asking one model to plan, edit, review, and test everything, each agent owns a narrower cognitive role. This improves traceability, makes prompts easier to tune, and allows future parallelization.

### Agent Communication

Agents communicate through structured messages, not loose prose. In this repository, each agent receives an `AgentMessage` containing:

- `task`: the user request
- `repository`: repository metadata and files
- `artifacts`: outputs from previous agents

Each agent returns an `AgentResult` with a status, explanation, artifacts, and handoff notes for the next agent.

### Agent Roles

| Agent | Responsibility | Inputs | Outputs |
| --- | --- | --- | --- |
| Planner Agent | Break the user task into implementation steps and identify impacted files | User task, repository summary | Plan, assumptions, delegation strategy |
| Coding Agent | Generate code changes or patch suggestions from the plan | Plan, repository files | Proposed files, code snippets, implementation notes |
| Reviewer Agent | Review generated code for correctness, maintainability, and security | Code artifacts, plan | Review findings, risk score, approval status |
| Testing Agent | Create tests and test commands for the generated code | Code artifacts, review notes | Test plan, generated tests, final readiness summary |

### Task Delegation

The planner decides what should be delegated. The orchestrator then passes artifacts from one agent to the next. This pattern mirrors real AI coding tools: a high-level controller coordinates specialist workers while preserving an auditable trail.

### Collaboration Patterns

- **Sequential handoff:** each agent waits for the previous result.
- **Critic loop:** reviewer can request changes from the coder.
- **Test-driven loop:** tester can generate failing tests before code is finalized.
- **Human-in-the-loop:** final artifacts are shown to the developer for approval.

## Features

### 1. GitHub Repo Reader

Fetches repository metadata and source files through the GitHub API. In production, use a GitHub App installation token; for local demos, set `GITHUB_TOKEN`.

**Industry examples**
- Devin/OpenHands clone repositories into a sandbox before planning edits.
- Enterprise assistants index code with embeddings and dependency graphs.

**Interview questions**
- How would you avoid sending secrets from a repository to an LLM?
- How would you handle monorepos with millions of files?

**Improvements**
- Add branch selection and pull request diff reading.
- Add tree-sitter parsing and embedding search.
- Add GitHub App auth instead of personal tokens.

### 2. Code Generation

The coding agent turns a plan into proposed file changes. The current implementation uses deterministic templates for safe local operation; replace `TemplateCodeGenerator` with your LLM provider of choice.

**Industry examples**
- Cursor and Copilot generate localized patches.
- OpenHands writes code inside a container and validates it with shell commands.

**Interview questions**
- How do you constrain an LLM to output valid patches?
- What is the difference between whole-file generation and diff generation?

**Improvements**
- Add JSON-schema constrained LLM outputs.
- Apply patches in a disposable workspace.
- Add retrieval-augmented context selection.

### 3. Code Review

The reviewer agent checks implementation artifacts for risks, missing tests, secrets, and maintainability issues.

**Industry examples**
- CodeRabbit and GitHub Copilot reviews summarize PR risks.
- Internal tools enforce architecture and security policies.

**Interview questions**
- How do you reduce false positives in AI code review?
- What security checks should run before code reaches an LLM?

**Improvements**
- Integrate Semgrep, Ruff, ESLint, and dependency scanners.
- Add policy-specific review prompts.
- Add reviewer-to-coder revision loops.

### 4. Test Creation

The testing agent proposes a test strategy and creates starter tests for generated code.

**Industry examples**
- Devin-style agents run unit tests, inspect failures, and iterate.
- CI bots generate regression tests from bug reports.

**Interview questions**
- How should an agent decide which tests to run?
- How do you prevent generated tests from asserting implementation details?

**Improvements**
- Execute tests in sandboxed containers.
- Add coverage-guided test generation.
- Add flaky-test detection.

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Then submit a task and GitHub repository URL from the UI or call the API directly:

```bash
curl -X POST http://localhost:8000/api/runs \
  -H 'content-type: application/json' \
  -d '{"task":"Add logging to the API","repo_url":"https://github.com/Anusha0501/multi-agent-coding-assistant"}'
```

## Architecture

```text
frontend React UI
      |
      v
FastAPI /api/runs
      |
      v
GitHubRepoReader -> AgentOrchestrator
                         |
                         v
Planner -> Coder -> Reviewer -> Tester -> FinalOutput
```

## Environment variables

| Variable | Description |
| --- | --- |
| `GITHUB_TOKEN` | Optional token for GitHub API requests |
| `VITE_API_URL` | Frontend API base URL, defaults to `http://localhost:8000` |

## Next production steps

1. Replace deterministic agent logic with CrewAI or AutoGen agents backed by an LLM.
2. Clone repos into isolated containers and apply generated patches.
3. Add streaming run events over WebSockets or Server-Sent Events.
4. Persist runs in Postgres with artifact storage.
5. Create GitHub pull requests through the GitHub API.

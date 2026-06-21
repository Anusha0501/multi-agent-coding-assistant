from __future__ import annotations

import os
from urllib.parse import urlparse

import httpx

from app.models import RepositoryFile, RepositorySnapshot


class GitHubRepoReader:
    """Reads lightweight repository context through the GitHub REST API."""

    def __init__(self, token: str | None = None, max_files: int = 20):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.max_files = max_files

    async def read(self, repo_url: str) -> RepositorySnapshot:
        owner, repo = self._parse_repo_url(repo_url)
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        async with httpx.AsyncClient(headers=headers, timeout=20) as client:
            meta_response = await client.get(f"https://api.github.com/repos/{owner}/{repo}")
            meta_response.raise_for_status()
            meta = meta_response.json()
            branch = meta.get("default_branch", "main")

            tree_response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}",
                params={"recursive": "1"},
            )
            tree_response.raise_for_status()
            tree = tree_response.json().get("tree", [])

            files: list[RepositoryFile] = []
            for item in tree:
                path = item.get("path", "")
                if item.get("type") != "blob" or not self._is_source_file(path):
                    continue
                content_response = await client.get(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}")
                if content_response.status_code >= 400:
                    continue
                payload = content_response.json()
                download_url = payload.get("download_url")
                if not download_url:
                    continue
                raw_response = await client.get(download_url)
                if raw_response.status_code >= 400:
                    continue
                files.append(RepositoryFile(path=path, content=raw_response.text[:8000], language=self._language(path)))
                if len(files) >= self.max_files:
                    break

        return RepositorySnapshot(
            url=repo_url,
            owner=owner,
            name=repo,
            default_branch=branch,
            description=meta.get("description"),
            files=files,
        )

    def _parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        parsed = urlparse(repo_url)
        parts = [part for part in parsed.path.split("/") if part]
        if parsed.netloc != "github.com" or len(parts) < 2:
            raise ValueError("repo_url must be a GitHub repository URL like https://github.com/owner/repo")
        return parts[0], parts[1].removesuffix(".git")

    def _is_source_file(self, path: str) -> bool:
        allowed = (".py", ".ts", ".tsx", ".js", ".jsx", ".md", ".json", ".yml", ".yaml")
        ignored = ("node_modules/", "dist/", "build/", ".git/", "coverage/")
        return path.endswith(allowed) and not path.startswith(ignored)

    def _language(self, path: str) -> str | None:
        return {
            ".py": "python",
            ".ts": "typescript",
            ".tsx": "typescript-react",
            ".js": "javascript",
            ".jsx": "javascript-react",
            ".md": "markdown",
            ".json": "json",
            ".yml": "yaml",
            ".yaml": "yaml",
        }.get("." + path.rsplit(".", 1)[-1])

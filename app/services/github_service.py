"""
GitHub API service for fetching repository data.
"""
import re
import base64
from typing import Dict, List, Optional, Tuple
import httpx

from app.config import settings, IGNORED_DIRS, SKIP_EXTENSIONS, IMPORTANT_FILES


GITHUB_API = "https://api.github.com"


def _headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "RepoLens-AI/1.0",
    }
    if settings.github_token:
        headers["Authorization"] = f"token {settings.github_token}"
    return headers


def validate_github_url(url: str) -> Tuple[bool, str, str]:
    """
    Validate and parse a GitHub repository URL.
    Returns (is_valid, owner, repository).
    """
    url = url.strip().rstrip("/")
    pattern = r"^https?://github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)/?$"
    match = re.match(pattern, url)
    if not match:
        return False, "", ""
    owner = match.group(1)
    repo = match.group(2)
    # Remove .git suffix if present
    if repo.endswith(".git"):
        repo = repo[:-4]
    return True, owner, repo


async def get_repo_metadata(owner: str, repo: str) -> Dict:
    """Fetch repository metadata from GitHub API."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}",
            headers=_headers(),
        )
        if response.status_code == 404:
            raise ValueError(f"Repository {owner}/{repo} not found or is private")
        if response.status_code == 403:
            raise ValueError("GitHub API rate limit exceeded. Please try again later.")
        response.raise_for_status()
        return response.json()


async def get_repo_languages(owner: str, repo: str) -> Dict[str, int]:
    """Fetch language breakdown from GitHub API."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/languages",
            headers=_headers(),
        )
        if response.status_code != 200:
            return {}
        return response.json()


async def get_repo_tree(owner: str, repo: str, branch: str = "HEAD") -> List[Dict]:
    """Fetch the complete repository file tree."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}",
            headers=_headers(),
            params={"recursive": "1"},
        )
        if response.status_code != 200:
            return []
        data = response.json()
        return data.get("tree", [])


async def get_file_content(owner: str, repo: str, path: str) -> Optional[str]:
    """Fetch and decode a file's content from GitHub."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
            headers=_headers(),
        )
        if response.status_code != 200:
            return None
        data = response.json()
        if data.get("type") != "file":
            return None
        size_kb = data.get("size", 0) / 1024
        if size_kb > settings.max_file_size_kb:
            return f"[File too large to analyze: {size_kb:.1f}KB]"
        content = data.get("content", "")
        encoding = data.get("encoding", "base64")
        if encoding == "base64":
            try:
                return base64.b64decode(content).decode("utf-8", errors="replace")
            except Exception:
                return None
        return content


def filter_tree(tree: List[Dict]) -> Tuple[List[Dict], List[str]]:
    """
    Filter the tree to exclude ignored directories and binary files.
    Returns (filtered_tree, ignored_paths).
    """
    filtered = []
    ignored = []

    for item in tree:
        path = item.get("path", "")
        item_type = item.get("type", "")

        # Skip ignored directories
        parts = path.split("/")
        if any(part in IGNORED_DIRS for part in parts):
            ignored.append(path)
            continue

        # Only include blobs (files), not trees (directories)
        if item_type != "blob":
            continue

        # Skip binary/large files by extension
        lower_path = path.lower()
        skip = False
        for ext in SKIP_EXTENSIONS:
            if lower_path.endswith(ext):
                skip = True
                break
        if skip:
            ignored.append(path)
            continue

        filtered.append(item)

    return filtered, ignored


def identify_important_files(tree_paths: List[str]) -> List[str]:
    """
    Identify which files in the tree should be prioritized for analysis.
    """
    important = []
    paths_set = set(tree_paths)

    # Check exact matches first
    for important_file in IMPORTANT_FILES:
        if important_file in paths_set:
            important.append(important_file)

    # Then look for common patterns
    for path in tree_paths:
        filename = path.split("/")[-1].lower()
        if filename in {"main.py", "app.py", "server.py", "index.py",
                        "index.js", "index.ts", "main.js", "main.ts",
                        "app.js", "app.ts"}:
            if path not in important:
                important.append(path)

    return important[:settings.max_files_to_analyze]


def build_directory_tree(tree_paths: List[str]) -> str:
    """Build a visual directory tree string from a list of paths."""
    if not tree_paths:
        return ""

    # Build nested dict structure
    def insert(node: dict, parts: List[str]) -> None:
        if not parts:
            return
        key = parts[0]
        if key not in node:
            node[key] = {}
        if len(parts) > 1:
            insert(node[key], parts[1:])

    root: dict = {}
    for path in sorted(tree_paths):
        parts = path.split("/")
        insert(root, parts)

    # Render tree
    lines = []

    def render(node: dict, prefix: str = "", name: str = "") -> None:
        if name:
            lines.append(f"{prefix}{name}/")
            prefix += "    "
        items = sorted(node.items())
        for i, (key, children) in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            ext_prefix = "    " if is_last else "│   "
            if children:
                lines.append(f"{prefix}{connector}{key}/")
                render(children, prefix + ext_prefix)
            else:
                lines.append(f"{prefix}{connector}{key}")

    render(root)
    return "\n".join(lines)

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    secret_key: str = "dev-secret-key-change-in-production-32chars"
    github_token: str = ""
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    debug: bool = False
    session_max_age: int = 86400
    max_files_to_analyze: int = 50
    max_file_size_kb: int = 100

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "static"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Directories to ignore during repository analysis
IGNORED_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", ".env",
    "dist", "build", ".next", "coverage", "__pycache__",
    ".pytest_cache", ".tox", "htmlcov", ".mypy_cache",
    "target", "vendor", ".cargo", "pkg", "out", ".output",
    ".nuxt", ".svelte-kit", "bower_components", ".cache",
    "tmp", "temp", "logs", ".idea", ".vscode",
}

# Important file patterns to prioritize
IMPORTANT_FILES = [
    "README.md", "readme.md", "README.rst",
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "requirements.txt", "requirements-dev.txt", "requirements-prod.txt",
    "pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "Pipfile.lock",
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    ".env.example", ".env.sample",
    "tsconfig.json", "jsconfig.json",
    "next.config.js", "next.config.ts", "next.config.mjs",
    "vite.config.js", "vite.config.ts",
    "tailwind.config.js", "tailwind.config.ts",
    "webpack.config.js",
    "Cargo.toml", "Cargo.lock",
    "go.mod", "go.sum",
    "pom.xml", "build.gradle", "build.gradle.kts",
    "Gemfile", "Gemfile.lock",
    "composer.json",
    ".github/workflows",
    "Makefile",
    "main.py", "app.py", "server.py", "index.js", "index.ts",
    "app/main.py", "src/main.py", "src/index.js", "src/index.ts",
]

# File extensions to skip (binaries, generated, large assets)
SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".bmp",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".zip", ".tar", ".gz", ".rar", ".7z",
    ".mp4", ".mp3", ".avi", ".mov", ".wav",
    ".exe", ".dll", ".so", ".dylib", ".a", ".lib",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".min.js", ".min.css",
    ".map",
    ".lock",
    ".pyc", ".pyo",
}

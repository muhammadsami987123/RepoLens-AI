# CONTRIBUTING.md — RepoLens AI

Thank you for your interest in contributing to RepoLens AI.

---

## Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/repolens-ai.git
cd repolens-ai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add OPENAI_API_KEY and SECRET_KEY

# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/ -v
```

---

## Code Style

- **Python 3.12+** — use modern syntax (`str | None`, `match/case`)
- **Type hints** on all function signatures
- **Async/await** for all I/O operations in routes and services
- **Pydantic v2** for all data models
- **No bare `except:`** — catch specific exception types
- Keep functions focused and small
- No external database — use `app/utils/storage.py` for all persistence

---

## Project Conventions

See [AGENTS.md](AGENTS.md) for the full development conventions used in this project.

Key rules:
- One router file per domain (`auth.py`, `analysis.py`, `reports.py`, `pages.py`)
- One service file per concern (see `app/services/`)
- No React/Vue — pure HTML + Tailwind + Vanilla JS
- No external databases — local JSON only
- All important files must be read before editing

---

## Making a Contribution

1. **Open an issue** first for significant changes — describe what and why
2. **Fork** the repository
3. **Create a branch:** `git checkout -b feature/your-feature-name`
4. **Write tests** for new functionality
5. **Run tests:** `pytest tests/ -v` — all must pass
6. **Check routes:** Verify all HTML pages load correctly
7. **Submit a PR** with a clear description of what changed and why

---

## What to Contribute

- Bug fixes
- New analysis capabilities (new service in `app/services/`)
- UI improvements (Tailwind only, no JS frameworks)
- Additional test coverage
- Documentation improvements
- Performance optimizations

## What NOT to Contribute

- External database integration (PostgreSQL, MongoDB, etc.)
- React/Vue/Next.js frontend
- Breaking changes to the JSON storage schema without migration
- Features that execute repository code
- Exposing the OpenAI API key to the frontend

---

## Reporting Issues

When reporting a bug, include:
- Python version
- OS
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages

For security vulnerabilities, see [SECURITY.md](SECURITY.md).

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

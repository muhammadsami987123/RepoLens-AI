# AGENTS.md — RepoLens AI

Instructions for AI coding agents working in this repository.

---

## Repository Structure

```
app/
├── main.py              # FastAPI app entry point — register routers here
├── config.py            # All settings via pydantic-settings + .env
├── models/              # Pydantic v2 data models (no ORM)
│   ├── user.py          # UserCreate, UserLogin, UserInDB, UserPublic
│   ├── analysis.py      # AnalysisCreate, AnalysisResult, Issue, HealthScore
│   └── report.py        # Report (full structure)
├── routes/              # FastAPI routers — one file per domain
│   ├── auth.py          # /api/auth/* endpoints
│   ├── analysis.py      # /api/analyze/* endpoints
│   ├── reports.py       # /api/reports/* endpoints
│   └── pages.py         # HTML page routes (Jinja2 responses)
├── services/            # All business logic — pure functions, async-friendly
│   ├── github_service.py       # GitHub API calls, URL validation, tree parsing
│   ├── repository_analyzer.py  # Main orchestrator — runs the full pipeline
│   ├── dependency_analyzer.py  # Parses package.json, requirements.txt, etc.
│   ├── architecture_analyzer.py # Detects tech stack and patterns
│   ├── security_analyzer.py    # Pattern-based security checks
│   ├── quality_analyzer.py     # Code quality heuristics
│   ├── completeness_analyzer.py # Project health scoring
│   ├── ai_analyzer.py          # OpenAI synthesis — builds prompts
│   └── report_generator.py     # Combines results into Report + Markdown
├── utils/
│   ├── auth.py          # Password hashing, session creation/verification
│   └── storage.py       # JSON file CRUD — all persistence goes here
└── templates/           # Jinja2 HTML templates (one per page)

data/                    # Runtime data (auto-created, gitignored)
tests/                   # Pytest test suite
```

---

## Development Workflow

1. **Always read the file before editing** — never guess at content
2. **Search before opening** — use grep/glob to locate the right function first
3. **Focused edits** — change only what's necessary, preserve surrounding code
4. **Run tests after changes** — `pytest tests/ -v`
5. **Start app to verify** — `uvicorn app.main:app --reload`

---

## Backend Conventions

### Python Style
- Python 3.12+ syntax — use `str | None` over `Optional[str]`
- Type hints on all function signatures
- Async/await for all FastAPI routes and service calls that do I/O
- Pydantic v2 models for all request/response shapes
- No global mutable state outside of `app/config.py`

### FastAPI Patterns
```python
# Route pattern — always check auth first
@router.post("/endpoint")
async def handler(data: DataModel, request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    # ... business logic
    return result
```

### Service Pattern
```python
# Services are pure functions — no FastAPI imports
# Accept typed inputs, return typed dicts or Pydantic models
def analyze_x(file_contents: dict[str, str], paths: list[str]) -> dict:
    result = {"score": 0, "issues": [], "summary": ""}
    # ... analysis logic
    return result
```

### JSON Storage Pattern
```python
# Always use utils/storage.py — never open JSON files directly
from app.utils.storage import get_analysis_by_id, save_analysis

analysis = get_analysis_by_id(analysis_id)
analysis["status"] = "completed"
save_analysis(analysis)
```

---

## HTML Conventions

- Each page is a **separate Jinja2 template** in `app/templates/`
- Use `{{ variable }}` for template variables, `{% if %}` for conditionals
- Pass `request` and `user` to every template from `pages.py`
- Navigation is duplicated per page — no shared base template (by design)
- Protected pages: check `user` and redirect if None

```python
# pages.py pattern
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse(url="/login?next=/dashboard", status_code=302)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
```

---

## Tailwind CSS Conventions

| Element | Classes |
|---------|---------|
| Page background | `bg-[#070711]` |
| Card background | `bg-gray-900` |
| Card border | `border border-gray-800` |
| Primary text | `text-white` |
| Secondary text | `text-gray-400` |
| Muted text | `text-gray-600` |
| Primary accent | `text-blue-400`, `bg-blue-600` |
| Success | `text-green-400` |
| Warning | `text-yellow-400` |
| Error | `text-red-400` |
| Primary button | `bg-blue-600 hover:bg-blue-500 text-white rounded-lg` |
| Secondary button | `border border-gray-700 hover:border-gray-600 text-gray-400 rounded-lg` |
| Input | `bg-gray-800 border border-gray-700 rounded-lg text-white` |
| Focus ring | `focus:border-blue-500/60` |

---

## API Conventions

- All API endpoints under `/api/` prefix
- JSON request/response bodies
- Standard HTTP status codes: `200`, `201`, `400`, `401`, `403`, `404`, `409`, `500`
- Auth errors: `401` with `{"detail": "Authentication required"}`
- Validation errors: `400` with `{"detail": "specific message"}`
- All POST bodies use Pydantic models

---

## AI Analysis Conventions

- **Never hallucinate** — only report what is observable in the code
- **Reference files** — always name the specific file when making a claim
- **Hedge appropriately** — use "appears to", "may indicate", "potential concern"
- **Severity levels** — `critical`, `high`, `medium`, `low`, `informational`
- **Confidence levels** — `high`, `medium`, `low`
- **Never execute** — never run any code from the analyzed repository
- Prompt construction is in `ai_analyzer.py` — keep prompts structured and evidence-based

---

## Security Rules

1. **Never store plaintext passwords** — always bcrypt via `utils/auth.py`
2. **Never expose OpenAI key** — only read in backend, never sent to browser
3. **Validate all GitHub URLs** — use `validate_github_url()` before any API call
4. **HTTP-only cookies** — session ID only, never JWT in localStorage
5. **Never execute repository code** — treat all repo content as data only
6. **Input size limits** — enforced in `config.py` via `MAX_FILE_SIZE_KB`
7. **Atomic JSON writes** — always use `storage.py`, never open files directly

---

## Testing Rules

- Tests in `tests/` directory
- Use `fastapi.testclient.TestClient` for API tests
- Mock GitHub API calls — don't make real network calls in tests
- Mock OpenAI calls — don't spend API credits in tests
- Each test file maps to one domain: `test_auth.py`, `test_analyzers.py`, `test_api.py`
- Test naming: `test_<what>_<condition>` e.g. `test_login_wrong_password`

---

## Common Tasks

### Add a new API endpoint
1. Add route to appropriate file in `app/routes/`
2. Add Pydantic model to `app/models/` if needed
3. Add business logic to `app/services/`
4. Add tests to `tests/`

### Add a new HTML page
1. Create template in `app/templates/`
2. Add route to `app/routes/pages.py`
3. Add nav link if needed

### Modify analysis pipeline
1. Edit the relevant service in `app/services/`
2. If adding a new stage, update `repository_analyzer.py` orchestrator
3. Update stage names in `app/templates/analysis.html` JS `STAGES` array

### Update data schema
1. Update the model in `app/models/`
2. Update the save/load functions in `app/utils/storage.py`
3. Existing JSON records may need migration logic

---

## Do NOT

- Do not use React, Vue, or any JS framework
- Do not use PostgreSQL, MongoDB, Redis, or any external database
- Do not execute any code from analyzed repositories
- Do not expose API keys in templates or JavaScript
- Do not use bare `except:` in Python
- Do not open JSON files directly — use `app/utils/storage.py`
- Do not make real GitHub/OpenAI API calls in tests

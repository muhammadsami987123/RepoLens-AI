# ARCHITECTURE.md — RepoLens AI

## System Overview

```
Browser
   ↓
HTML + Tailwind CSS + Vanilla JavaScript
   ↓  (fetch API, HTTP-only session cookie)
FastAPI (Python 3.12+)
   ↓
┌─────────────────────────────────────────────┐
│           Repository Analyzer               │
│  (app/services/repository_analyzer.py)      │
├──────────┬──────────┬────────┬──────────────┤
│ GitHub   │Dependency│Security│Completeness  │
│ Service  │Analyzer  │Analyzer│Analyzer      │
├──────────┴──────────┴────────┴──────────────┤
│         Architecture Analyzer               │
│         Quality Analyzer                    │
├─────────────────────────────────────────────┤
│         OpenAI Analysis Agent               │
│         (GPT-4o via structured prompts)     │
├─────────────────────────────────────────────┤
│         Report Generator                    │
│         (Markdown + JSON)                   │
└─────────────────────────────────────────────┘
   ↓
JSON File Storage
(data/analyses.json, data/reports.json)
```

---

## Component Breakdown

### Frontend Layer

- **Technology:** HTML5, Tailwind CSS (CDN), Vanilla JS (Fetch API)
- **Templates:** Jinja2 server-rendered HTML (`app/templates/`)
- **Pages:** `index`, `about`, `how-it-works`, `contact`, `login`, `signup`, `dashboard`, `analysis`, `result`, `reports`, `settings`
- **Auth:** Session cookie (`rl_session`) read from HTTP-only cookie
- **API calls:** `fetch('/api/...')` with `Content-Type: application/json`
- **Analysis polling:** `/api/analyze/{id}/status` polled every 1.5s during analysis

### FastAPI Layer (`app/`)

- **Entry point:** `app/main.py` — mounts routers, static files, error handlers
- **Configuration:** `app/config.py` — `pydantic-settings` reads `.env`
- **Routers:** `auth`, `analysis`, `reports`, `pages`
- **Background tasks:** Analysis runs as `BackgroundTask` in FastAPI — non-blocking
- **Authentication:** HTTP-only session cookie verified server-side per request

### Analysis Pipeline (`app/services/`)

All stages run sequentially in `repository_analyzer.py`:

```
Stage 1:  URL Validation        (github_service.validate_github_url)
Stage 2:  GitHub Metadata       (github_service.get_repo_metadata)
Stage 3:  Language Detection    (github_service.get_repo_languages)
Stage 4:  Repository Tree       (github_service.get_repo_tree → filter_tree)
Stage 5:  File Identification   (github_service.identify_important_files)
Stage 6:  Content Extraction    (github_service.get_file_content × N)
Stage 7:  Dependency Analysis   (dependency_analyzer.analyze_dependencies)
Stage 8:  Architecture Analysis (architecture_analyzer.analyze_architecture)
Stage 9:  Security Analysis     (security_analyzer.analyze_security)
Stage 10: Quality Analysis      (quality_analyzer.analyze_code_quality)
Stage 11: Completeness          (completeness_analyzer.analyze_completeness)
Stage 12: AI Synthesis          (ai_analyzer.synthesize_with_ai → OpenAI)
Stage 13: Report Generation     (report_generator.generate_report)
Stage 14: Complete
```

Each stage updates `analyses.json` with current `stage`, `progress`, `message`.

### GitHub Service (`app/services/github_service.py`)

- Validates GitHub URLs with regex
- Uses GitHub REST API v3 (public endpoints)
- Optionally authenticates with `GITHUB_TOKEN` for higher rate limits
- Filters file tree: removes `node_modules`, `.venv`, build directories, binaries
- Identifies important files (README, package.json, Dockerfile, etc.)
- Builds visual directory tree string

### AI Analyzer (`app/services/ai_analyzer.py`)

- Constructs structured prompts from all analysis context
- Sends to `gpt-4o` (configurable) with `response_format: json_object`
- Requests evidence-based, hedged analysis
- Falls back to static analysis summary if OpenAI key is missing
- **Never blindly dumps entire repository** — truncates and prioritizes

### Storage Layer (`app/utils/storage.py`)

- Pure Python, no ORM
- Atomic writes via temp file + `os.replace()`
- CRUD functions per entity: users, sessions, analyses, reports
- Data directory auto-created at startup

---

## Data Flow

```
User enters GitHub URL in browser
          ↓
POST /api/analyze (JSON)
          ↓
FastAPI validates auth (session cookie)
          ↓
Validates GitHub URL format
          ↓
Creates analysis record in analyses.json (status: pending)
          ↓
Starts BackgroundTask: run_analysis()
          ↓
Returns { analysis_id, status: "pending" }
          ↓
Browser polls GET /api/analyze/{id}/status every 1.5s
          ↓
Background task updates analyses.json at each stage
          ↓
When status = "completed" → browser redirects to /analysis/{id}
          ↓
GET /api/analyze/{id} + GET /api/reports/{report_id}
          ↓
Browser renders results dashboard
          ↓
User can download /api/reports/{id}/markdown or /api/reports/{id}/json
```

---

## Authentication Flow

```
POST /api/auth/signup or /api/auth/login
          ↓
Server verifies credentials (bcrypt)
          ↓
Creates session in sessions.json (random 32-byte token)
          ↓
Sets HTTP-only cookie: rl_session=<token>
          ↓
All subsequent requests include cookie automatically
          ↓
Protected routes call get_current_user_id(request)
    → reads cookie → looks up session → returns user_id
          ↓
If no valid session → 401 (API) or redirect to /login (HTML pages)
```

---

## JSON Storage Schema

### users.json
```json
[{
  "id": "uuid",
  "name": "Full Name",
  "email": "user@example.com",
  "hashed_password": "$2b$...",
  "created_at": "2026-08-25T10:00:00Z",
  "analyses_count": 5
}]
```

### sessions.json
```json
[{
  "id": "random-32-byte-token",
  "user_id": "uuid",
  "created_at": "2026-08-25T10:00:00Z"
}]
```

### analyses.json
```json
[{
  "id": "uuid",
  "user_id": "uuid",
  "repository_url": "https://github.com/owner/repo",
  "owner": "owner",
  "repository": "repo",
  "depth": "deep",
  "status": "completed",
  "stage": "completed",
  "progress": 100,
  "message": "Analysis complete",
  "health_score": { "overall": 87, "architecture": 90, ... },
  "technology_stack": ["Python", "FastAPI", "Docker"],
  "languages": { "Python": 85432 },
  "total_files": 124,
  "total_issues": 8,
  "completeness_category": "Mostly Complete",
  "created_at": "...",
  "completed_at": "...",
  "report_id": "uuid"
}]
```

### reports.json
```json
[{
  "id": "uuid",
  "analysis_id": "uuid",
  "user_id": "uuid",
  "owner": "owner",
  "repository": "repo",
  "repository_url": "...",
  "created_at": "...",
  "health_score": { ... },
  "executive_summary": "...",
  "architecture": "...",
  "issues": [...],
  "security_findings": [...],
  "completeness": { ... },
  "markdown_report": "# Repository Analysis Report\n...",
  "raw_analysis": { "arch": {...}, "deps": {...}, ... }
}]
```

---

## Security Design

- Passwords hashed with **bcrypt** (passlib) — never stored plaintext
- Sessions stored server-side in `sessions.json` — cookie holds only token ID
- `secure=True` on cookies in production (`DEBUG=false`)
- `httponly=True` on all session cookies — inaccessible to JavaScript
- OpenAI API key **only** in server-side `config.py` — never in HTML/JS responses
- Repository code is **never executed** — treated as text data only
- GitHub URL validation via strict regex before any API call
- Atomic JSON writes prevent file corruption

---

## File Size and Rate Limits

| Setting | Default | Config Key |
|---------|---------|------------|
| Max files analyzed | 50 | `MAX_FILES_TO_ANALYZE` |
| Max file size | 100 KB | `MAX_FILE_SIZE_KB` |
| Ignored dirs | 20+ | `IGNORED_DIRS` in config.py |
| GitHub API rate limit | 60/hr (unauth), 5000/hr (with token) | `GITHUB_TOKEN` |
| AI prompt truncation | ~8000 chars of file content | hardcoded in ai_analyzer.py |

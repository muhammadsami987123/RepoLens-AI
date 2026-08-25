# RepoLens AI

> **Understand Any GitHub Repository. Instantly.**

RepoLens AI is an AI-powered GitHub repository intelligence platform. Paste any public GitHub repository URL and receive a comprehensive technical analysis report — covering architecture, code quality, security, dependencies, and completeness.

---

## Features

- **Repository Intelligence** — Understand the complete structure, purpose, and organization of any public repository
- **Architecture Mapping** — Discover how components, services, APIs, and modules interact
- **Issue Detection** — Identify potential bugs, security concerns, configuration problems, and technical debt
- **Dependency Analysis** — Parse and summarize all package dependencies
- **AI Synthesis** — OpenAI synthesizes findings into evidence-based insights
- **Markdown Report** — Download a full 25-section technical report
- **Project Health Score** — Scored assessment across 8 dimensions
- **Authentication** — Secure email/password auth with bcrypt and HTTP-only sessions

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12+, FastAPI, Uvicorn |
| AI | OpenAI API (GPT-4o) |
| Frontend | HTML5, Tailwind CSS, Vanilla JavaScript |
| Storage | Local JSON files (no external DB) |
| Auth | bcrypt, HTTP-only cookies |

---

## Architecture

```
Browser (HTML + Tailwind + Vanilla JS)
    ↓
FastAPI (Python)
    ↓
GitHub Repository Analyzer
    ├── Repository Scanner (github_service.py)
    ├── File Analyzer
    ├── Dependency Analyzer
    ├── Architecture Analyzer
    ├── Security Analyzer
    ├── Quality Analyzer
    ├── Completeness Analyzer
    └── AI Analyzer (OpenAI GPT-4o)
    ↓
Report Generator
    ↓
Markdown + JSON Output
```

---

## AI Analysis Pipeline

```
GitHub URL
    ↓ URL Validation
    ↓ Repository Metadata
    ↓ File Tree Scan
    ↓ Important File Identification
    ↓ File Content Extraction
    ↓ Technology Detection
    ↓ Dependency Analysis
    ↓ Architecture Analysis
    ↓ Code Quality Analysis
    ↓ Security Analysis
    ↓ Completeness Analysis
    ↓ OpenAI Synthesis
    ↓ Professional Markdown Report
```

---

## Repository Analysis Process

1. **URL Validation** — Validates GitHub URL format (must be `https://github.com/owner/repo`)
2. **Metadata Fetch** — Stars, forks, description, default branch via GitHub API
3. **Tree Scan** — Full file tree with filtering (ignores `node_modules`, `.venv`, `dist`, etc.)
4. **Important File Detection** — Prioritizes `README.md`, `package.json`, `requirements.txt`, `Dockerfile`, etc.
5. **Content Extraction** — Reads key files up to configurable size limits
6. **Static Analysis** — Dependency, architecture, security, and quality checks
7. **AI Synthesis** — Structured prompt sent to OpenAI with all gathered evidence
8. **Report Generation** — 25-section Markdown document produced

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/repolens-ai.git
cd repolens-ai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for AI synthesis |
| `SECRET_KEY` | Yes | Session signing key (min 32 chars) |
| `OPENAI_MODEL` | No | OpenAI model (default: `gpt-4o`) |
| `GITHUB_TOKEN` | No | GitHub PAT — increases rate limit from 60 to 5000 req/hr |
| `DEBUG` | No | Enable debug mode (default: `false`) |
| `MAX_FILES_TO_ANALYZE` | No | Max files to inspect per repo (default: `50`) |
| `MAX_FILE_SIZE_KB` | No | Max file size to read (default: `100`) |

---

## Running Locally

```bash
uvicorn app.main:app --reload --port 8000
```

Open [http://localhost:8000](http://localhost:8000)

---

## API Documentation

When `DEBUG=true`, Swagger UI is available at `/api/docs`.

### Authentication

```
POST /api/auth/signup     — Create account
POST /api/auth/login      — Sign in
POST /api/auth/logout     — Sign out
GET  /api/auth/me         — Current user
```

### Analysis

```
POST /api/analyze                    — Start analysis
GET  /api/analyze/{id}               — Get analysis details
GET  /api/analyze/{id}/status        — Poll analysis status
GET  /api/analyze                    — List all analyses
```

### Reports

```
GET /api/reports                     — List reports
GET /api/reports/{id}                — Get report (JSON)
GET /api/reports/{id}/markdown       — Download Markdown
GET /api/reports/{id}/json           — Download JSON
```

---

## Pages

| Route | Access | Description |
|-------|--------|-------------|
| `/` | Public | Landing page |
| `/about` | Public | About page |
| `/how-it-works` | Public | Pipeline explanation |
| `/contact` | Public | Contact form |
| `/login` | Public | Sign in |
| `/signup` | Public | Create account |
| `/dashboard` | Protected | Analysis history |
| `/analysis` | Protected | Start new analysis |
| `/analysis/{id}` | Protected | View analysis result |
| `/reports` | Protected | Report history |
| `/settings` | Protected | Account settings |

---

## Data Storage

Local JSON files in `data/` directory (auto-created):

```
data/
├── users.json       — User accounts (hashed passwords)
├── sessions.json    — Active sessions
├── analyses.json    — Analysis records and status
└── reports.json     — Generated reports
```

> Note: `data/` is excluded from git. No external database required.

---

## Usage

1. Sign up at `/signup`
2. Paste any public GitHub URL (e.g. `https://github.com/tiangolo/fastapi`)
3. Select analysis depth (Standard / Deep / Architecture / Security)
4. Watch the live analysis progress
5. Explore results: Overview, Architecture, Issues, Security, Completeness
6. Download the Markdown or JSON report

---

## Screenshots

> *(Add screenshots here after first run)*

- Landing page with hero URL input
- Live analysis progress with staged pipeline
- Results dashboard with tabs
- Full Markdown report with download

---

## Example Report Structure

```markdown
# Repository Analysis Report

## 1. Executive Summary
## 2. Repository Overview
## 3. Purpose of the Project
## 4. Technology Stack
## 5. Repository Structure
## 6. Architecture
## 7. Data Flow
## 8. Important Files
## 9. Dependencies
## 10. Configuration
## 11. API Structure
## 12. Database Structure
## 13. Authentication
## 14. Code Quality
## 15. Security Analysis
## 16. Performance Considerations
## 17. Potential Issues
## 18. Possible Runtime Errors
## 19. Project Completeness
## 20. How To Install
## 21. How To Run
## 22. How To Build
## 23. How To Deploy
## 24. Recommended Improvements
## 25. Final Assessment
```

---

## Roadmap

- [ ] GitHub OAuth authentication
- [ ] Private repository support (with PAT)
- [ ] Side-by-side repository comparison
- [ ] Scheduled re-analysis / change detection
- [ ] Team workspaces
- [ ] VS Code extension

---

## Running Tests

```bash
pytest tests/ -v
```

---

## License

MIT License — see [LICENSE](LICENSE)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*Built with FastAPI + OpenAI + Tailwind CSS*

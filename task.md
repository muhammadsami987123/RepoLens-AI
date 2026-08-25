

**GitHub URL → AI analyzes repository → architecture + issues + setup + completeness + technical report → Markdown export.**

For your requirements, I'd keep the implementation intentionally lightweight: **FastAPI + Python + HTML + Tailwind + Vanilla JS + local JSON storage**, with the UI getting most of the attention.


````md
# RepoLens AI
## Autonomous GitHub Repository Analysis Platform

You are a Senior Full-Stack Engineer, AI Agent Engineer, Python Engineer, UI/UX Designer, and Product Architect.

Build a complete, professional, portfolio-ready application called:

# RepoLens AI

### Tagline
> Understand Any GitHub Repository. Instantly.

RepoLens AI allows a user to paste any public GitHub repository URL and have an AI-powered analysis system inspect the repository and generate a comprehensive technical report.

The application should explain:

- What the repository is
- Why it exists
- What problem it solves
- How the repository works
- Complete repository structure
- Technology stack
- Application architecture
- Important files
- Entry points
- Dependencies
- Data flow
- API structure
- Database structure if present
- Configuration
- Environment variables
- How to install it
- How to run it
- How to build it
- How to deploy it
- Potential bugs
- Code quality problems
- Security concerns
- Performance concerns
- Missing pieces
- Incomplete features
- Possible runtime errors
- Technical debt
- Overall project completeness
- Recommended improvements

The final output must also be exportable as a professional Markdown report.

---

# IMPORTANT PRODUCT DIRECTION

This is NOT a generic chatbot.

It is an:

> AI-powered GitHub Repository Intelligence Platform.

The main experience should be:

```text
GitHub URL
     ↓
Repository Discovery
     ↓
Repository Structure Analysis
     ↓
Code Analysis
     ↓
Architecture Analysis
     ↓
Dependency Analysis
     ↓
Configuration Analysis
     ↓
Issue Detection
     ↓
Completeness Analysis
     ↓
AI Synthesis
     ↓
Professional Report
````

The application must make this process visually understandable.

---

# TECHNOLOGY STACK

## Backend

Use:

* Python 3.12+
* FastAPI
* Pydantic
* Uvicorn
* OpenAI SDK
* GitHub public repository access
* Python standard library wherever possible

Use OpenAI API for the AI analysis layer.

Do NOT expose the OpenAI API key to the browser.

---

# FRONTEND

Use ONLY:

* HTML5
* Tailwind CSS
* Vanilla JavaScript
* Fetch API

Do NOT use:

* React
* Next.js
* Vue
* Angular
* Svelte

Use FastAPI HTML routing.

Every major page must be a separate HTML file.

---

# DATA STORAGE

Do NOT use PostgreSQL, MongoDB, Redis, Supabase, Firebase, or another external database.

Use local JSON files.

Example:

```text
data/
    users.json
    analyses.json
    reports.json
    sessions.json
```

Create the files automatically if they do not exist.

Use safe file operations and avoid corrupting JSON data.

---

# PROJECT DOCUMENTATION

Before implementing the application, create:

```text
CLAUDE.md
AGENTS.md
README.md
ARCHITECTURE.md
SECURITY.md
CONTRIBUTING.md
LICENSE
.env.example
.gitignore
```

Use the MIT License.

---

# CLAUDE.md

Document:

* project purpose
* architecture
* coding conventions
* frontend rules
* backend rules
* AI analysis rules
* JSON storage rules
* security requirements
* testing requirements
* development commands

---

# AGENTS.md

Create instructions for future AI coding agents.

Include:

* repository structure
* development workflow
* backend conventions
* HTML conventions
* Tailwind conventions
* API conventions
* AI analysis conventions
* security rules
* testing rules

---

# README.md

Create a professional GitHub README.

Include:

* Product overview
* Features
* Architecture
* Tech stack
* AI analysis pipeline
* Repository analysis process
* Installation
* Environment variables
* Running locally
* Usage
* Screenshots section
* Example report
* API documentation
* Roadmap
* License

---

# ARCHITECTURE.md

Document:

```text
Browser
   ↓
HTML + Tailwind + Vanilla JS
   ↓
FastAPI
   ↓
GitHub Repository Analyzer
   ↓
Repository Scanner
   ↓
File Analyzer
   ↓
Dependency Analyzer
   ↓
Architecture Analyzer
   ↓
OpenAI Analysis Agent
   ↓
Report Generator
   ↓
Markdown / JSON
```

---

# APPLICATION ROUTES

Create these HTML routes:

```text
/
 /about
 /how-it-works
 /contact
 /login
 /signup
 /dashboard
 /analysis
 /reports
 /settings
```

Protected routes:

```text
/dashboard
/analysis
/reports
/settings
```

If the user is not authenticated, redirect to:

```text
/login
```

---

# LANDING PAGE

The homepage is extremely important.

Make it visually impressive and professional.

Design inspiration:

* Linear
* Vercel
* GitHub
* Raycast
* modern AI developer tools

Do not make it look like a generic AI SaaS template.

---

# NAVBAR

Create:

```text
RepoLens AI

Analyze
How It Works
About
Contact

Sign In
Get Started
```

Navbar should be:

* responsive
* sticky
* clean
* minimal
* professional

---

# HERO SECTION

Main heading:

# Understand Any GitHub Repository With AI

Supporting text:

> Paste a GitHub repository URL and let RepoLens AI analyze its architecture, code structure, dependencies, configuration, potential issues, and completeness.

Hero should contain the main interaction.

Create a large GitHub URL input:

```text
┌─────────────────────────────────────────────────────────────┐
│  https://github.com/owner/repository              Analyze → │
└─────────────────────────────────────────────────────────────┘
```

Above/below it:

```text
Public GitHub repositories supported
```

Primary button:

```text
Analyze Repository
```

---

# HERO VISUAL

Below the input, show a premium preview card.

Example:

```text
Repository Intelligence

Repository
facebook/react

Stack
TypeScript · JavaScript · Node.js

Files
2,481

Dependencies
142

Architecture
Monorepo

Health
87 / 100
```

This should feel like a real developer intelligence product.

---

# FEATURES SECTION

Create feature cards:

### Repository Intelligence

Understand the complete repository structure.

### Architecture Mapping

Discover how components, services, APIs, and modules interact.

### Issue Detection

Identify potential bugs, security concerns, configuration issues, and technical debt.

### Setup Guide

Generate installation and execution instructions.

### AI Report

Generate a complete technical Markdown report.

### Project Health

Determine whether the project appears complete, incomplete, experimental, or production-ready.

---

# HOW IT WORKS

Create a visual 4-step section.

```text
01
Paste Repository

02
AI Scans Repository

03
AI Understands Architecture

04
Get Technical Report
```

---

# REPORT PREVIEW

Show a beautiful report preview containing:

```text
Repository Overview

Architecture

Technology Stack

Repository Structure

Important Files

Dependencies

Data Flow

Configuration

Potential Issues

Security Analysis

Performance Analysis

Project Completeness

How To Run

Recommended Improvements
```

---

# AUTHENTICATION

Create:

```text
/login
/signup
```

## Login

Fields:

```text
Email
Password
Remember me
Forgot password
Sign In
```

## Signup

Fields:

```text
Name
Email
Password
Confirm Password
Create Account
```

Add visual OAuth buttons:

```text
Continue with Google
Continue with GitHub
Continue with Apple
```

These may remain integration-ready UI unless OAuth credentials are configured.

Do not pretend OAuth is functional if credentials are unavailable.

---

# AUTHENTICATION IMPLEMENTATION

Implement functional email/password authentication.

Use:

* password hashing
* secure session handling
* HTTP-only cookies
* server-side authentication checks

Never store plaintext passwords.

Store users in:

```text
data/users.json
```

---

# DASHBOARD

Create:

```text
/dashboard
```

Dashboard should show:

```text
Repository Analyses

+ New Analysis
```

Stats:

```text
Repositories Analyzed
Reports Generated
Issues Detected
Average Health Score
```

Recent analyses:

```text
Repository
Status
Health
Issues
Analyzed
Actions
```

Example:

```text
facebook/react
Completed
94/100
12 issues
2 minutes ago
View Report
```

---

# NEW ANALYSIS

Create a large input interface:

```text
Analyze a Repository

GitHub Repository URL

[ https://github.com/... ]

[ Analyze Repository ]
```

Optional configuration:

```text
Analysis Depth

○ Standard
● Deep
○ Architecture Only
○ Security Focus
```

Keep the interface simple.

---

# REPOSITORY ANALYSIS LOADER

This is one of the most important UI components.

After clicking Analyze:

Show a full-screen or large premium analysis workspace.

Do NOT show a generic spinner.

Show actual analysis stages.

Example:

```text
Analyzing Repository

████████████████████░░░░ 82%

✓ Repository discovered
✓ Repository metadata loaded
✓ File structure analyzed
✓ Dependencies analyzed
● Architecture analysis
○ Code quality analysis
○ Security analysis
○ AI synthesis
○ Report generation
```

Animate the progress.

Show live status messages.

Example:

```text
Scanning source files...
Analyzing package dependencies...
Detecting application entry points...
Mapping repository architecture...
Looking for configuration issues...
Preparing technical report...
```

The progress should correspond to real backend stages where possible.

Do NOT fake 100% progress instantly.

---

# REPOSITORY ANALYZER

Create a Python service:

```text
app/services/repository_analyzer.py
```

Responsibilities:

* validate GitHub URL
* extract owner/repository
* retrieve repository metadata
* retrieve repository tree
* inspect files
* detect languages
* detect frameworks
* detect package managers
* detect configuration
* detect entry points
* identify important files

---

# GITHUB SUPPORT

Support public GitHub repositories.

Validate URLs such as:

```text
https://github.com/facebook/react
https://github.com/tiangolo/fastapi
```

Reject:

* invalid URLs
* unsupported hosts
* malformed repositories

Architecture should allow GitHub API authentication later.

---

# FILE ANALYSIS

Analyze important files first.

Examples:

```text
README.md
package.json
requirements.txt
pyproject.toml
Dockerfile
docker-compose.yml
.env.example
tsconfig.json
next.config.*
vite.config.*
tailwind.config.*
package-lock.json
pnpm-lock.yaml
yarn.lock
Cargo.toml
go.mod
pom.xml
build.gradle
```

Detect source directories such as:

```text
src/
app/
pages/
components/
lib/
api/
server/
backend/
frontend/
tests/
```

Do not blindly send an entire massive repository to the AI model.

Create a controlled analysis pipeline.

---

# LARGE REPOSITORY HANDLING

Implement sensible limits.

For example:

* ignore `.git`
* ignore generated files
* ignore binaries
* ignore large assets
* ignore build output
* ignore `node_modules`
* ignore virtual environments
* ignore cache directories

Examples:

```text
.git/
node_modules/
.venv/
venv/
dist/
build/
.next/
coverage/
__pycache__/
```

For very large repositories:

1. Analyze repository tree
2. Identify important files
3. Analyze configuration
4. Analyze representative source files
5. Analyze architecture
6. Send summarized context to OpenAI

Do not blindly upload the entire repository.

---

# REPOSITORY STRUCTURE ANALYSIS

Generate a visual and textual tree.

Example:

```text
project/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   └── main.py
├── tests/
├── templates/
├── static/
├── requirements.txt
├── README.md
└── Dockerfile
```

Explain every important directory.

---

# TECHNOLOGY DETECTION

Detect:

* programming languages
* frameworks
* libraries
* databases
* package managers
* build tools
* testing frameworks
* deployment technologies

Display:

```text
Technology Stack

Python
FastAPI
PostgreSQL
Docker
Pytest
OpenAI SDK
```

---

# ARCHITECTURE ANALYSIS

Generate:

```text
Architecture Overview
```

Explain:

* frontend
* backend
* APIs
* services
* database
* external integrations
* authentication
* background jobs
* queues if present

Create a visual architecture diagram where possible.

---

# DATA FLOW

Explain:

```text
User
 ↓
Frontend
 ↓
API
 ↓
Service Layer
 ↓
Database
 ↓
External Services
```

Adapt this to the actual repository.

Do not invent architecture.

---

# IMPORTANT FILE ANALYSIS

For each important file:

```text
File
Purpose
Role
Dependencies
Potential Issues
```

Example:

```text
app/main.py

Purpose:
FastAPI application entry point.

Role:
Initializes the API server and registers routes.

Potential concerns:
...
```

---

# DEPENDENCY ANALYSIS

Analyze dependency files.

Show:

```text
Dependencies

Production
Development
Testing
```

Detect:

* outdated-looking packages where possible
* duplicated dependencies
* suspicious dependencies
* missing dependency declarations
* dependency conflicts where detectable

Do not claim a package is vulnerable unless verified through a reliable vulnerability source.

Instead use language such as:

> Potential concern: dependency appears outdated and should be checked against current security advisories.

---

# CODE QUALITY ANALYSIS

Look for:

* duplicated logic
* overly large modules
* unclear naming
* missing error handling
* missing validation
* dead-looking code
* hardcoded configuration
* excessive coupling
* missing tests
* inconsistent structure

Clearly distinguish:

```text
Confirmed observation
Potential concern
Recommendation
```

Never hallucinate bugs.

---

# SECURITY ANALYSIS

Check for obvious patterns such as:

* hardcoded secrets
* unsafe environment handling
* insecure authentication
* missing authorization
* unsafe input handling
* exposed API keys
* dangerous shell execution
* insecure CORS
* debug mode
* unsafe file operations

Never claim a vulnerability with certainty unless the code clearly demonstrates it.

Use severity:

```text
Critical
High
Medium
Low
Informational
```

---

# PROJECT COMPLETENESS

Generate a project health assessment.

Categories:

```text
Production Ready
Mostly Complete
MVP / Prototype
Incomplete
Experimental
Unknown
```

Create a score:

```text
Project Health

██████████████████░░ 86/100
```

Break score into:

```text
Architecture
Code Quality
Testing
Documentation
Security
Configuration
Deployment Readiness
Completeness
```

Explain why the score was assigned.

---

# ERROR & FAILURE ANALYSIS

Identify possible runtime problems.

Examples:

```text
Missing environment variable
Missing dependency
Incorrect startup command
Database configuration issue
Potential import error
Missing migration
Incomplete configuration
Missing build step
```

Separate:

```text
Likely Issue
Possible Issue
Requires Verification
```

---

# HOW TO RUN

Generate an actual repository-specific guide.

Example:

```bash
git clone ...
cd project

python -m venv .venv
pip install -r requirements.txt

cp .env.example .env

uvicorn app.main:app --reload
```

For Node:

```bash
npm install
npm run dev
```

Do not invent commands.

Derive commands from repository files.

---

# REPORT GENERATION

Generate a comprehensive Markdown report.

Structure:

```md
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

Only include sections that are relevant to the repository.

---

# RESULTS PAGE

After analysis completes, redirect to:

```text
/analysis/{analysis_id}
```

Create a professional analysis dashboard.

Top section:

```text
facebook/react

Analysis Complete

Health Score
94/100

Technology
React · TypeScript · JavaScript

Files
2,481

Issues
12
```

---

# RESULT NAVIGATION

Create tabs:

```text
Overview
Architecture
Structure
Technology
Dependencies
Issues
Security
Completeness
How To Run
Report
```

---

# OVERVIEW

Show:

```text
Repository Purpose
Architecture Summary
Technology Stack
Project Health
Major Findings
```

---

# ARCHITECTURE TAB

Display:

* architecture diagram
* components
* services
* data flow
* integrations

---

# STRUCTURE TAB

Interactive repository tree.

Allow expanding:

```text
src/
app/
components/
lib/
tests/
```

Clicking a file should show:

```text
Purpose
Importance
Analysis
```

---

# ISSUES TAB

Display issue cards.

Example:

```text
HIGH

Missing error handling

File:
src/api/client.py

Why it matters:
...

Recommendation:
...
```

Filters:

```text
All
Critical
High
Medium
Low
```

---

# SECURITY TAB

Show:

```text
Security Score

Potential Secrets
Authentication
Authorization
Input Validation
Configuration
Dependencies
```

---

# COMPLETENESS TAB

Show:

```text
Project Completeness

Documentation      92%
Testing             71%
Configuration       89%
Architecture        94%
Security            83%
Deployment          78%
```

Use beautiful progress bars.

---

# REPORT TAB

Render the generated Markdown beautifully.

Provide:

```text
Copy Markdown
Download Markdown
Download JSON
Print Report
```

Download:

```text
repository-analysis.md
repository-analysis.json
```

---

# MARKDOWN EXPORT

The Markdown file should be complete enough that a developer can give it to another AI coding tool and understand the repository.

Include:

```text
Repository identity
Purpose
Architecture
Structure
Important files
Stack
Dependencies
Configuration
Issues
Security
Testing
Deployment
Recommendations
```

---

# REPORT SIDEBAR

Display:

```text
REPORT

Executive Summary
Architecture
Technology
Structure
Dependencies
Issues
Security
Completeness
Setup
Recommendations
```

Clicking a section should scroll to it.

---

# REPORT SEARCH

Add search:

```text
Search report...
```

Highlight matching sections.

---

# COPY FEATURES

Every important code block should have:

```text
Copy
```

button.

---

# REPORT HISTORY

Create:

```text
/reports
```

Show previously generated reports.

Example:

```text
facebook/react
Analyzed Aug 25, 2026
94/100
View Report

tiangolo/fastapi
Analyzed Aug 25, 2026
91/100
View Report
```

---

# LOCAL JSON DATA

Store:

```text
data/users.json
data/analyses.json
data/reports.json
data/sessions.json
```

Example analysis:

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "repository_url": "https://github.com/owner/repo",
  "owner": "owner",
  "repository": "repo",
  "status": "completed",
  "health_score": 87,
  "created_at": "...",
  "report_path": "..."
}
```

---

# API ENDPOINTS

Create:

```text
POST /api/auth/signup
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me

POST /api/analyze
GET  /api/analyze/{id}
GET  /api/analyze/{id}/status

GET  /api/reports
GET  /api/reports/{id}

GET  /api/reports/{id}/markdown
GET  /api/reports/{id}/json

POST /api/contact

GET /api/health
```

---

# ANALYSIS PIPELINE

Implement:

```text
Repository URL
      ↓
URL Validation
      ↓
GitHub Metadata
      ↓
Repository Tree
      ↓
Important File Detection
      ↓
File Content Extraction
      ↓
Technology Detection
      ↓
Dependency Analysis
      ↓
Architecture Analysis
      ↓
Code Quality Analysis
      ↓
Security Analysis
      ↓
Completeness Analysis
      ↓
OpenAI Synthesis
      ↓
Markdown Report
```

Create separate Python services.

Example:

```text
app/
├── main.py
├── config.py
├── models/
├── routes/
│   ├── auth.py
│   ├── analysis.py
│   ├── reports.py
│   └── pages.py
├── services/
│   ├── github_service.py
│   ├── repository_analyzer.py
│   ├── dependency_analyzer.py
│   ├── architecture_analyzer.py
│   ├── security_analyzer.py
│   ├── quality_analyzer.py
│   ├── completeness_analyzer.py
│   ├── ai_analyzer.py
│   └── report_generator.py
├── utils/
└── templates/
```

---

# AI ANALYSIS

Use the OpenAI API for synthesis.

The AI must receive structured repository information.

Do not simply send:

> "Analyze this repository."

Instead construct structured analysis prompts containing:

```text
Repository metadata
Repository tree
Important configuration files
Dependency information
Relevant source excerpts
Detected technologies
Static analysis findings
```

Ask the AI to:

* reason from evidence
* avoid hallucinating
* identify uncertainty
* distinguish facts from recommendations
* reference files when making claims

---

# EVIDENCE SYSTEM

Important findings should reference repository files.

Example:

```text
Potential issue

File:
src/auth/service.py

Evidence:
Authentication errors are caught broadly without differentiated handling.

Confidence:
High
```

This makes the product more credible.

---

# UI STYLE

Use Tailwind CSS.

Create a sophisticated developer-focused design.

Preferred:

* near-black / deep slate workspace
* white typography
* subtle gray borders
* restrained blue/purple accent
* subtle gradients
* clean cards
* professional charts
* compact controls
* smooth transitions

Avoid:

* excessive rounded cards
* giant empty spaces
* excessive emojis
* childish illustrations
* generic dashboard templates

---

# LOADING EXPERIENCE

Use a beautiful repository analysis animation.

Show:

```text
Repository discovered
        ↓
Reading structure
        ↓
Understanding dependencies
        ↓
Mapping architecture
        ↓
Inspecting configuration
        ↓
Analyzing code quality
        ↓
Checking security
        ↓
Evaluating completeness
        ↓
Generating report
```

Each step should transition smoothly.

---

# RESPONSIVE DESIGN

Fully support:

* desktop
* laptop
* tablet
* mobile

On mobile:

* stack cards
* collapse navigation
* make repository input full width
* make report tabs horizontally scrollable
* make repository tree usable
* keep buttons touch-friendly

Do not simply shrink the desktop UI.

---

# CONTACT PAGE

Create:

```text
Name
Email
Subject
Message
Send Message
```

Store contact submissions locally if needed.

---

# ABOUT PAGE

Explain:

> RepoLens AI helps developers understand unfamiliar repositories without manually reading thousands of files.

Show:

```text
Understand
Analyze
Diagnose
Document
Improve
```

---

# HOW IT WORKS PAGE

Explain the pipeline:

```text
01
Repository Discovery

02
Structural Analysis

03
Code Intelligence

04
AI Reasoning

05
Report Generation
```

Use visual diagrams.

---

# SETTINGS

Create:

```text
Profile
Preferences
Analysis Settings
```

Keep this lightweight.

---

# SECURITY

Implement:

* password hashing
* secure cookies
* authentication
* authorization
* input validation
* URL validation
* GitHub URL restrictions
* safe JSON writes
* request size limits
* OpenAI key protection
* safe report generation
* no arbitrary code execution

Important:

The application must NEVER execute arbitrary code from the analyzed repository.

The repository is analyzed as data only.

---

# ERROR STATES

Create polished error UI for:

### Invalid GitHub URL

```text
Invalid repository URL

Please provide a valid public GitHub repository.
```

### Repository Not Found

```text
Repository not found

Check that the repository exists and is publicly accessible.
```

### Analysis Failed

```text
Analysis interrupted

We couldn't complete the repository analysis.

Try again.
```

### API Limit

```text
Repository analysis temporarily unavailable.

Please try again later.
```

---

# EMPTY STATES

Create professional empty states.

Example:

```text
No repositories analyzed yet.

Paste a GitHub URL and start your first analysis.

[ Analyze Repository ]
```

---

# DEMO REPOSITORIES

Provide optional examples on the homepage:

```text
Try an example

FastAPI
React
Next.js
LangChain
```

These should only populate the URL field, not automatically start analysis.

---

# PERFORMANCE

Prioritize:

* asynchronous FastAPI operations
* efficient repository retrieval
* limited file scanning
* structured AI context
* caching where reasonable
* avoiding repeated repository downloads
* efficient JSON writes

---

# TESTING

Create tests for:

```text
URL validation
GitHub URL parsing
Authentication
Authorization
JSON persistence
Repository structure parsing
Technology detection
Dependency detection
Report generation
Markdown export
API endpoints
```

Add basic end-to-end tests for:

```text
Signup
Login
Analyze repository
View analysis
Download report
Logout
```

---

# FINAL USER FLOW

The complete experience should be:

```text
Landing Page
     ↓
Paste GitHub URL
     ↓
Click Analyze
     ↓
Login if required
     ↓
Analysis Workspace
     ↓
Repository Discovery
     ↓
Structure Analysis
     ↓
Architecture Analysis
     ↓
Code Analysis
     ↓
Security Analysis
     ↓
Completeness Analysis
     ↓
AI Synthesis
     ↓
Results Dashboard
     ↓
Explore Findings
     ↓
Open Full Report
     ↓
Copy Markdown
     ↓
Download Markdown
```

---

# IMPORTANT UX RULE

The homepage should make the product understandable in less than 10 seconds.

A visitor should immediately understand:

> "I paste a GitHub repository URL and this AI tells me everything important about the project."

---

# FINAL QUALITY BAR

This is a portfolio project.

It should look like a real developer SaaS product.

Prioritize:

1. Homepage
2. Repository input
3. Analysis animation
4. Results dashboard
5. Report experience
6. Architecture visualization
7. Issue analysis
8. Authentication
9. Responsive design
10. Documentation

Do not create fake buttons.

Do not create fake analysis data in the actual workflow.

Do not claim the AI found something unless it has evidence.

Do not execute repository code.

Do not expose API keys.

Do not use React.

Use:

Python + FastAPI + OpenAI API + HTML + Tailwind CSS + Vanilla JavaScript + Local JSON.

---

# BUILD ORDER

Follow this exact order:

## Phase 1: Foundation

Create:

```text
CLAUDE.md
AGENTS.md
README.md
ARCHITECTURE.md
SECURITY.md
CONTRIBUTING.md
LICENSE
.env.example
.gitignore
```

Set up:

* FastAPI
* project structure
* configuration
* JSON storage
* authentication foundation
* HTML routing

---

## Phase 2: Product

Build:

* landing page
* login
* signup
* dashboard
* analysis workflow
* GitHub integration
* repository scanner
* AI analyzer
* report generator
* results dashboard
* Markdown export
* report history
* about
* how it works
* contact
* settings
* responsive UI

---

## Phase 3: QA

Run:

* backend tests
* API tests
* authentication tests
* analysis tests
* export tests
* UI checks
* responsive checks

Fix all errors.

Check every route.

Check authentication protection.

Check JSON persistence.

Check invalid repository handling.

Check report downloads.

---

# FINAL COMMAND

After implementation:

1. Start the application.
2. Test all routes.
3. Test signup.
4. Test login.
5. Test a public GitHub repository.
6. Verify analysis progress.
7. Verify results.
8. Verify Markdown generation.
9. Verify download.
10. Verify logout.
11. Fix all runtime errors.
12. Fix all UI issues.
13. Ensure the application is ready for a professional screen-recorded demo.

Do not stop at scaffolding.

Build the complete working product.

```
```

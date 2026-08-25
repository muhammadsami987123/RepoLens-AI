# SECURITY.md — RepoLens AI

## Security Policy

### Reporting a Vulnerability

If you discover a security vulnerability in RepoLens AI, please report it responsibly:

- **Do not** open a public GitHub issue for security vulnerabilities
- Email the maintainer directly with details
- Include: description, steps to reproduce, potential impact, and suggested fix
- We will acknowledge within 48 hours and aim to patch within 7 days

---

## Security Design

### Authentication

- **Password hashing:** bcrypt via `passlib[bcrypt]` — industry-standard adaptive hash
- **No plaintext passwords:** Passwords are hashed before storage and never logged
- **Session management:** Random 32-byte URL-safe tokens stored server-side in `sessions.json`
- **HTTP-only cookies:** Session cookie (`rl_session`) is inaccessible to JavaScript
- **Secure cookies:** `Secure=True` enforced when `DEBUG=false`
- **SameSite:** `SameSite=Lax` prevents CSRF for most attack vectors
- **No JWT in localStorage:** Sessions are server-side only

### API Security

- All protected routes verify session cookie before processing
- Returns `401 Unauthorized` for unauthenticated API requests
- Returns `403 Forbidden` for unauthorized resource access (e.g. other users' reports)
- Input validation via Pydantic v2 models on all POST bodies
- Request bodies rejected if they don't match expected schema

### Repository Analysis Safety

- **No code execution:** Repository files are read as text data only — never executed
- **URL validation:** Strict regex enforcement — only `https://github.com/owner/repo` accepted
- **File size limits:** Files over `MAX_FILE_SIZE_KB` (default 100KB) are not fully read
- **File count limits:** Maximum `MAX_FILES_TO_ANALYZE` (default 50) files fetched per analysis
- **Directory filtering:** `node_modules`, `.venv`, `dist`, `build` etc. are excluded
- **Binary filtering:** Images, archives, executables are skipped

### OpenAI API Key Protection

- API key loaded only in `app/config.py` via environment variable
- Never included in API responses, HTML templates, or JavaScript
- Never logged or exposed in error messages
- Falls back gracefully if key is missing (returns static analysis only)

### Data Storage

- **Atomic writes:** JSON files written via temp file + `os.replace()` — prevents corruption
- **No external database:** All data in local `data/` directory
- **File permissions:** Ensure `data/` directory is not web-accessible
- **User data isolation:** Reports and analyses filtered by `user_id` on every query

### Input Validation

- GitHub URL: validated against `^https?://github\.com/[owner]/[repo]$` before any API call
- Email: format check before account creation
- Password: minimum 8 character length enforcement
- Name: minimum 2 character length enforcement

---

## Known Limitations

1. **Rate limiting:** No per-IP or per-user rate limiting on analysis endpoints (consider adding for production)
2. **Session expiry:** Sessions do not expire automatically — implement TTL check for production
3. **CSRF:** `SameSite=Lax` provides partial protection — consider `SameSite=Strict` or CSRF tokens for forms
4. **File locking:** JSON writes are atomic but not multi-process safe (single-instance deployment assumed)
5. **GitHub token:** Not required, but without it the 60 req/hr limit may cause analysis failures

---

## Production Hardening Checklist

- [ ] Set a strong `SECRET_KEY` (min 32 chars, cryptographically random)
- [ ] Set `DEBUG=false`
- [ ] Set `GITHUB_TOKEN` for higher API rate limits
- [ ] Ensure `data/` directory is not accessible from the web
- [ ] Run behind a reverse proxy (nginx) with HTTPS
- [ ] Enable HTTPS — required for `Secure` cookie flag to work
- [ ] Consider adding rate limiting middleware
- [ ] Rotate `SECRET_KEY` periodically (invalidates all sessions)
- [ ] Monitor `data/sessions.json` size — clean up expired sessions periodically

---

## Dependencies

Security-relevant dependencies:

| Package | Purpose | Version |
|---------|---------|---------|
| `passlib[bcrypt]` | Password hashing | 1.7.4 |
| `python-jose` | JWT utilities (reserved) | 3.3.0 |
| `pydantic` | Input validation | 2.9.2 |
| `httpx` | HTTP client (replaces requests) | 0.27.2 |

Keep all dependencies updated. Run `pip list --outdated` regularly.

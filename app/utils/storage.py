"""
Thread-safe JSON file storage utilities.
"""
import json
import os
import tempfile
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import DATA_DIR

_write_lock = asyncio.Lock()


def _read_json(file_path: Path) -> Any:
    """Synchronously read a JSON file, returning empty list/dict if missing."""
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return []


def _write_json(file_path: Path, data: Any) -> None:
    """Atomically write JSON data to file via temp file + rename."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = file_path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, file_path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


# --- Users ---

def get_all_users() -> List[Dict]:
    return _read_json(DATA_DIR / "users.json")


def get_user_by_id(user_id: str) -> Optional[Dict]:
    for user in get_all_users():
        if user.get("id") == user_id:
            return user
    return None


def get_user_by_email(email: str) -> Optional[Dict]:
    for user in get_all_users():
        if user.get("email", "").lower() == email.lower():
            return user
    return None


def save_user(user: Dict) -> None:
    users = get_all_users()
    for i, u in enumerate(users):
        if u.get("id") == user["id"]:
            users[i] = user
            _write_json(DATA_DIR / "users.json", users)
            return
    users.append(user)
    _write_json(DATA_DIR / "users.json", users)


# --- Sessions ---

def get_all_sessions() -> List[Dict]:
    return _read_json(DATA_DIR / "sessions.json")


def get_session(session_id: str) -> Optional[Dict]:
    for session in get_all_sessions():
        if session.get("id") == session_id:
            return session
    return None


def save_session(session: Dict) -> None:
    sessions = get_all_sessions()
    for i, s in enumerate(sessions):
        if s.get("id") == session["id"]:
            sessions[i] = session
            _write_json(DATA_DIR / "sessions.json", sessions)
            return
    sessions.append(session)
    _write_json(DATA_DIR / "sessions.json", sessions)


def delete_session(session_id: str) -> None:
    sessions = [s for s in get_all_sessions() if s.get("id") != session_id]
    _write_json(DATA_DIR / "sessions.json", sessions)


# --- Analyses ---

def get_all_analyses() -> List[Dict]:
    return _read_json(DATA_DIR / "analyses.json")


def get_analysis_by_id(analysis_id: str) -> Optional[Dict]:
    for a in get_all_analyses():
        if a.get("id") == analysis_id:
            return a
    return None


def get_analyses_by_user(user_id: str) -> List[Dict]:
    analyses = [a for a in get_all_analyses() if a.get("user_id") == user_id]
    return sorted(analyses, key=lambda x: x.get("created_at", ""), reverse=True)


def save_analysis(analysis: Dict) -> None:
    analyses = get_all_analyses()
    for i, a in enumerate(analyses):
        if a.get("id") == analysis["id"]:
            analyses[i] = analysis
            _write_json(DATA_DIR / "analyses.json", analyses)
            return
    analyses.append(analysis)
    _write_json(DATA_DIR / "analyses.json", analyses)


# --- Reports ---

def get_all_reports() -> List[Dict]:
    return _read_json(DATA_DIR / "reports.json")


def get_report_by_id(report_id: str) -> Optional[Dict]:
    for r in get_all_reports():
        if r.get("id") == report_id:
            return r
    return None


def get_report_by_analysis_id(analysis_id: str) -> Optional[Dict]:
    for r in get_all_reports():
        if r.get("analysis_id") == analysis_id:
            return r
    return None


def get_reports_by_user(user_id: str) -> List[Dict]:
    reports = [r for r in get_all_reports() if r.get("user_id") == user_id]
    return sorted(reports, key=lambda x: x.get("created_at", ""), reverse=True)


def save_report(report: Dict) -> None:
    reports = get_all_reports()
    for i, r in enumerate(reports):
        if r.get("id") == report["id"]:
            reports[i] = report
            _write_json(DATA_DIR / "reports.json", reports)
            return
    reports.append(report)
    _write_json(DATA_DIR / "reports.json", reports)

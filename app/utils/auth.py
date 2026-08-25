"""
Authentication utilities: password hashing and session management.
"""
import uuid
import secrets
from datetime import datetime, timezone
from typing import Optional

import bcrypt
from fastapi import Request, HTTPException

from app.config import settings
from app.utils.storage import get_session, save_session, delete_session, get_user_by_id

SESSION_COOKIE = "rl_session"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_session(user_id: str) -> str:
    session_id = secrets.token_urlsafe(32)
    session = {
        "id": session_id,
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    save_session(session)
    return session_id


def get_current_user_id(request: Request) -> Optional[str]:
    session_id = request.cookies.get(SESSION_COOKIE)
    if not session_id:
        return None
    session = get_session(session_id)
    if not session:
        return None
    return session.get("user_id")


def require_auth(request: Request) -> str:
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user_id


def invalidate_session(request: Request) -> None:
    session_id = request.cookies.get(SESSION_COOKIE)
    if session_id:
        delete_session(session_id)

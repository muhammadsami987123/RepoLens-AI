"""
Authentication API routes.
"""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, Request, Depends

from app.models.user import UserCreate, UserLogin, UserPublic
from app.utils.auth import (
    hash_password, verify_password, create_session,
    get_current_user_id, invalidate_session, SESSION_COOKIE,
)
from app.utils.storage import get_user_by_email, save_user, get_user_by_id
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup")
async def signup(user_data: UserCreate, response: Response):
    # Validate inputs
    if len(user_data.name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
    if "@" not in user_data.email or "." not in user_data.email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    # Check if email already registered
    if get_user_by_email(user_data.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create user
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "name": user_data.name.strip(),
        "email": user_data.email.lower().strip(),
        "hashed_password": hash_password(user_data.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "analyses_count": 0,
    }
    save_user(user)

    # Create session
    session_id = create_session(user_id)
    response.set_cookie(
        key=SESSION_COOKIE,
        value=session_id,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.session_max_age,
    )

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
    }


@router.post("/login")
async def login(credentials: UserLogin, response: Response):
    user = get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    session_id = create_session(user["id"])
    response.set_cookie(
        key=SESSION_COOKIE,
        value=session_id,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.session_max_age,
    )

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
        "analyses_count": user.get("analyses_count", 0),
    }


@router.post("/logout")
async def logout(request: Request, response: Response):
    invalidate_session(request)
    response.delete_cookie(SESSION_COOKIE)
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_me(request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
        "analyses_count": user.get("analyses_count", 0),
    }

"""
Analysis API routes.
"""
import uuid
import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks

from app.models.analysis import AnalysisCreate
from app.utils.auth import get_current_user_id
from app.utils.storage import save_analysis, get_analysis_by_id, get_analyses_by_user, get_user_by_id, save_user
from app.services.github_service import validate_github_url
from app.services.repository_analyzer import run_analysis

router = APIRouter(prefix="/api/analyze", tags=["analysis"])


@router.post("")
async def start_analysis(
    data: AnalysisCreate,
    request: Request,
    background_tasks: BackgroundTasks,
):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Validate URL
    is_valid, owner, repo = validate_github_url(data.repository_url)
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL. Expected format: https://github.com/owner/repository"
        )

    # Create analysis record
    analysis_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    analysis = {
        "id": analysis_id,
        "user_id": user_id,
        "repository_url": data.repository_url,
        "owner": owner,
        "repository": repo,
        "depth": data.depth,
        "status": "pending",
        "stage": "queued",
        "progress": 0,
        "message": "Analysis queued...",
        "created_at": now,
        "completed_at": None,
        "health_score": None,
        "technology_stack": [],
        "languages": {},
        "total_files": 0,
        "total_issues": 0,
        "completeness_category": "",
        "report_id": None,
        "error": None,
    }
    save_analysis(analysis)

    # Increment user's analysis count
    user = get_user_by_id(user_id)
    if user:
        user["analyses_count"] = user.get("analyses_count", 0) + 1
        save_user(user)

    # Run analysis in background
    background_tasks.add_task(
        run_analysis,
        analysis_id=analysis_id,
        user_id=user_id,
        repository_url=data.repository_url,
        depth=data.depth,
    )

    return {
        "analysis_id": analysis_id,
        "status": "pending",
        "message": "Analysis started",
    }


@router.get("/{analysis_id}")
async def get_analysis(analysis_id: str, request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    analysis = get_analysis_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if analysis.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return analysis


@router.get("/{analysis_id}/status")
async def get_analysis_status(analysis_id: str, request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    analysis = get_analysis_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if analysis.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "id": analysis["id"],
        "status": analysis.get("status", "unknown"),
        "stage": analysis.get("stage", ""),
        "progress": analysis.get("progress", 0),
        "message": analysis.get("message", ""),
        "report_id": analysis.get("report_id"),
        "error": analysis.get("error"),
    }


@router.get("")
async def list_analyses(request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    analyses = get_analyses_by_user(user_id)
    return {"analyses": analyses, "total": len(analyses)}

"""
Reports API routes.
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse, JSONResponse
import json

from app.utils.auth import get_current_user_id
from app.utils.storage import get_report_by_id, get_reports_by_user, get_report_by_analysis_id

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("")
async def list_reports(request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    reports = get_reports_by_user(user_id)
    # Return summary list (not full content)
    summary = [
        {
            "id": r["id"],
            "owner": r.get("owner", ""),
            "repository": r.get("repository", ""),
            "repository_url": r.get("repository_url", ""),
            "created_at": r.get("created_at", ""),
            "health_score": r.get("health_score", {}),
            "analysis_id": r.get("analysis_id", ""),
        }
        for r in reports
    ]
    return {"reports": summary, "total": len(summary)}


@router.get("/{report_id}")
async def get_report(report_id: str, request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return report


@router.get("/{report_id}/markdown")
async def get_report_markdown(report_id: str, request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    markdown = report.get("markdown_report", "")
    repo_name = f"{report.get('owner', 'repo')}-{report.get('repository', 'analysis')}"
    return PlainTextResponse(
        content=markdown,
        headers={
            "Content-Disposition": f"attachment; filename={repo_name}-analysis.md",
            "Content-Type": "text/markdown; charset=utf-8",
        },
    )


@router.get("/{report_id}/json")
async def get_report_json(report_id: str, request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    repo_name = f"{report.get('owner', 'repo')}-{report.get('repository', 'analysis')}"
    return JSONResponse(
        content=report,
        headers={
            "Content-Disposition": f"attachment; filename={repo_name}-analysis.json",
        },
    )


@router.post("/contact")
async def contact(request: Request):
    """Handle contact form submissions."""
    return {"message": "Message received. Thank you for contacting us."}

"""
HTML page routes — serves Jinja2 templates.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR
from app.utils.auth import get_current_user_id
from app.utils.storage import get_user_by_id, get_analysis_by_id, get_report_by_id

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _get_user(request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        return None
    return get_user_by_id(user_id)


# Public pages
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = _get_user(request)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    user = _get_user(request)
    return templates.TemplateResponse("about.html", {"request": request, "user": user})


@router.get("/how-it-works", response_class=HTMLResponse)
async def how_it_works(request: Request):
    user = _get_user(request)
    return templates.TemplateResponse("how-it-works.html", {"request": request, "user": user})


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    user = _get_user(request)
    return templates.TemplateResponse("contact.html", {"request": request, "user": user})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = _get_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "user": None})


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    user = _get_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("signup.html", {"request": request, "user": None})


# Protected pages
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse(url="/login?next=/dashboard", status_code=302)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


@router.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse(url="/login?next=/analysis", status_code=302)
    return templates.TemplateResponse("analysis.html", {"request": request, "user": user})


@router.get("/analysis/{analysis_id}", response_class=HTMLResponse)
async def analysis_result(analysis_id: str, request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse(url=f"/login?next=/analysis/{analysis_id}", status_code=302)
    analysis = get_analysis_by_id(analysis_id)
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "user": user, "analysis_id": analysis_id, "analysis": analysis}
    )


@router.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse(url="/login?next=/reports", status_code=302)
    return templates.TemplateResponse("reports.html", {"request": request, "user": user})


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse(url="/login?next=/settings", status_code=302)
    return templates.TemplateResponse("settings.html", {"request": request, "user": user})

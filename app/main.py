"""
RepoLens AI — FastAPI application entry point.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings, STATIC_DIR
from app.routes import auth, analysis, reports, pages

app = FastAPI(
    title="RepoLens AI",
    description="AI-powered GitHub repository intelligence platform",
    version="1.0.0",
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
)

# Static files
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Routers
app.include_router(auth.router)
app.include_router(analysis.router)
app.include_router(reports.router)
app.include_router(pages.router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/api/contact")
async def contact_form(request: Request):
    return {"message": "Thank you for your message. We'll get back to you soon."}


@app.exception_handler(404)
async def not_found(request: Request, exc):
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
    from app.config import TEMPLATES_DIR
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    # For API routes return JSON, for page routes return HTML
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return HTMLResponse(
        content="<h1>404 — Page Not Found</h1><a href='/'>Go Home</a>",
        status_code=404,
    )


@app.exception_handler(500)
async def server_error(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."},
    )

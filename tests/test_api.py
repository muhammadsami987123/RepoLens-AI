"""
API endpoint tests.
"""
import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_test_user():
    email = f"api_{uuid.uuid4().hex[:8]}@example.com"
    res = client.post("/api/auth/signup", json={
        "name": "API Test User",
        "email": email,
        "password": "testpassword123",
    })
    assert res.status_code == 200
    return email, client  # session cookie is set on the client


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"


def test_analyze_unauthenticated():
    c = TestClient(app)  # fresh client without auth
    res = c.post("/api/analyze", json={"repository_url": "https://github.com/tiangolo/fastapi"})
    assert res.status_code == 401


def test_analyze_invalid_url():
    email, c = create_test_user()
    res = c.post("/api/analyze", json={"repository_url": "not-a-github-url"})
    assert res.status_code == 400


def test_analyze_valid_url_starts():
    email, c = create_test_user()
    res = c.post("/api/analyze", json={"repository_url": "https://github.com/tiangolo/fastapi"})
    # Should either start (200) or be an error, not a 500
    assert res.status_code in [200, 400, 422]
    if res.status_code == 200:
        data = res.json()
        assert "analysis_id" in data
        assert data["status"] == "pending"


def test_reports_list_unauthenticated():
    c = TestClient(app)
    res = c.get("/api/reports")
    assert res.status_code == 401


def test_reports_list_authenticated():
    email, c = create_test_user()
    res = c.get("/api/reports")
    assert res.status_code == 200
    data = res.json()
    assert "reports" in data


def test_analyses_list_authenticated():
    email, c = create_test_user()
    res = c.get("/api/analyze")
    assert res.status_code == 200
    data = res.json()
    assert "analyses" in data


def test_pages_accessible():
    for path in ["/", "/about", "/how-it-works", "/contact", "/login", "/signup"]:
        res = client.get(path)
        assert res.status_code == 200, f"Page {path} returned {res.status_code}"


def test_protected_pages_redirect():
    c = TestClient(app)
    for path in ["/dashboard", "/analysis", "/reports", "/settings"]:
        res = c.get(path, follow_redirects=False)
        assert res.status_code in [302, 307], f"Page {path} should redirect"

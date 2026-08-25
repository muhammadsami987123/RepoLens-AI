"""
Authentication tests.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup_success():
    import uuid
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    res = client.post("/api/auth/signup", json={
        "name": "Test User",
        "email": email,
        "password": "testpassword123",
    })
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == email
    assert "id" in data


def test_signup_duplicate_email():
    import uuid
    email = f"dup_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/api/auth/signup", json={"name":"A","email":email,"password":"pass1234"})
    res = client.post("/api/auth/signup", json={"name":"B","email":email,"password":"pass1234"})
    assert res.status_code == 409


def test_signup_weak_password():
    res = client.post("/api/auth/signup", json={
        "name": "Test",
        "email": "weak@example.com",
        "password": "short",
    })
    assert res.status_code == 400


def test_login_success():
    import uuid
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/api/auth/signup", json={"name":"Login Test","email":email,"password":"strongpass123"})
    res = client.post("/api/auth/login", json={"email": email, "password": "strongpass123"})
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == email


def test_login_wrong_password():
    import uuid
    email = f"wp_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/api/auth/signup", json={"name":"WP","email":email,"password":"correctpass"})
    res = client.post("/api/auth/login", json={"email": email, "password": "wrongpass"})
    assert res.status_code == 401


def test_me_unauthenticated():
    res = client.get("/api/auth/me")
    assert res.status_code == 401


def test_protected_route_redirect():
    # Without auth, dashboard should redirect to login
    res = client.get("/dashboard", follow_redirects=False)
    assert res.status_code == 302
    assert "/login" in res.headers.get("location", "")

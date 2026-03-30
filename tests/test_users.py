"""
Tests for User endpoints:
  POST /users/         - create user
  GET  /users/         - get all users
  GET  /users/{id}     - get user by ID
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core import db

client = TestClient(app)


def setup_function():
    """Clear in-memory store before each test."""
    db.users.clear()
    db.courses.clear()
    db.enrollments.clear()


# ---------------------------------------------------------------------------
# POST /users/
# ---------------------------------------------------------------------------

def test_create_student_user_success():
    payload = {"name": "Alice", "email": "alice@example.com", "role": "student"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["role"] == "student"
    assert "id" in data


def test_create_admin_user_success():
    payload = {"name": "Bob Admin", "email": "bob@example.com", "role": "admin"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["role"] == "admin"


def test_create_user_invalid_email():
    payload = {"name": "Alice", "email": "not-an-email", "role": "student"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 422


def test_create_user_empty_name():
    payload = {"name": "   ", "email": "alice@example.com", "role": "student"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 422


def test_create_user_invalid_role():
    payload = {"name": "Alice", "email": "alice@example.com", "role": "superuser"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 422


def test_create_user_missing_fields():
    response = client.post("/users/", json={"name": "Alice"})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /users/
# ---------------------------------------------------------------------------

def test_get_all_users_empty():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_get_all_users_returns_created_users():
    client.post("/users/", json={"name": "Alice", "email": "alice@example.com", "role": "student"})
    client.post("/users/", json={"name": "Bob", "email": "bob@example.com", "role": "admin"})
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


# ---------------------------------------------------------------------------
# GET /users/{id}
# ---------------------------------------------------------------------------

def test_get_user_by_id_success():
    create_resp = client.post("/users/", json={"name": "Alice", "email": "alice@example.com", "role": "student"})
    user_id = create_resp.json()["data"]["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Alice"


def test_get_user_by_id_not_found():
    response = client.get("/users/9999")
    assert response.status_code == 404

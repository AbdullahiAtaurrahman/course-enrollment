"""
Tests for Course endpoints:
  GET    /courses/       - public: get all courses
  GET    /courses/{id}   - public: get course by ID
  POST   /courses/       - admin only: create course
  PATCH  /courses/{id}   - admin only: update course
  DELETE /courses/{id}   - admin only: delete course
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
# Helpers
# ---------------------------------------------------------------------------

def create_admin():
    resp = client.post("/users/", json={"name": "Admin User", "email": "admin@example.com", "role": "admin"})
    return int(resp.json()["data"]["id"])


def create_student():
    resp = client.post("/users/", json={"name": "Student User", "email": "student@example.com", "role": "student"})
    return int(resp.json()["data"]["id"])


def create_course(admin_id: int, title: str = "Math 101", code: str = "MTH101"):
    resp = client.post(
        "/courses/",
        json={"title": title, "code": code},
        params={"user_id": admin_id},
    )
    return resp


# ---------------------------------------------------------------------------
# GET /courses/  — public access
# ---------------------------------------------------------------------------

def test_get_all_courses_public_empty():
    response = client.get("/courses/")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_get_all_courses_public_with_data():
    admin_id = create_admin()
    create_course(admin_id)
    response = client.get("/courses/")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


# ---------------------------------------------------------------------------
# GET /courses/{id}  — public access
# ---------------------------------------------------------------------------

def test_get_course_by_id_public():
    admin_id = create_admin()
    course_resp = create_course(admin_id)
    course_id = course_resp.json()["data"]["id"]
    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["data"]["code"] == "MTH101"


def test_get_course_by_id_not_found():
    response = client.get("/courses/9999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /courses/  — admin only
# ---------------------------------------------------------------------------

def test_create_course_admin_success():
    admin_id = create_admin()
    response = create_course(admin_id)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["title"] == "Math 101"
    assert data["code"] == "MTH101"


def test_create_course_student_forbidden():
    student_id = create_student()
    response = client.post(
        "/courses/",
        json={"title": "Math 101", "code": "MTH101"},
        params={"user_id": student_id},
    )
    assert response.status_code == 403


def test_create_course_empty_title():
    admin_id = create_admin()
    response = client.post(
        "/courses/",
        json={"title": "   ", "code": "MTH101"},
        params={"user_id": admin_id},
    )
    assert response.status_code == 400


def test_create_course_empty_code():
    admin_id = create_admin()
    response = client.post(
        "/courses/",
        json={"title": "Math 101", "code": "   "},
        params={"user_id": admin_id},
    )
    assert response.status_code == 400


def test_create_course_duplicate_code():
    admin_id = create_admin()
    create_course(admin_id, code="MTH101")
    response = client.post(
        "/courses/",
        json={"title": "Another Math", "code": "MTH101"},
        params={"user_id": admin_id},
    )
    assert response.status_code == 400


def test_create_course_invalid_user_not_found():
    response = client.post(
        "/courses/",
        json={"title": "Math 101", "code": "MTH101"},
        params={"user_id": 9999},
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /courses/{id}  — admin only
# ---------------------------------------------------------------------------

def test_update_course_admin_success():
    admin_id = create_admin()
    course_resp = create_course(admin_id)
    course_id = course_resp.json()["data"]["id"]
    response = client.patch(
        f"/courses/{course_id}",
        json={"title": "Updated Math"},
        params={"user_id": admin_id},
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Updated Math"


def test_update_course_student_forbidden():
    admin_id = create_admin()
    student_id = create_student()
    course_resp = create_course(admin_id)
    course_id = course_resp.json()["data"]["id"]
    response = client.patch(
        f"/courses/{course_id}",
        json={"title": "Hacked"},
        params={"user_id": student_id},
    )
    assert response.status_code == 403


def test_update_course_not_found():
    admin_id = create_admin()
    response = client.patch(
        "/courses/9999",
        json={"title": "Nope"},
        params={"user_id": admin_id},
    )
    assert response.status_code == 404


def test_update_course_empty_title():
    admin_id = create_admin()
    course_resp = create_course(admin_id)
    course_id = course_resp.json()["data"]["id"]
    response = client.patch(
        f"/courses/{course_id}",
        json={"title": "   "},
        params={"user_id": admin_id},
    )
    assert response.status_code == 400


def test_update_course_duplicate_code():
    admin_id = create_admin()
    create_course(admin_id, title="Course A", code="AAA")
    course_b = create_course(admin_id, title="Course B", code="BBB")
    course_b_id = course_b.json()["data"]["id"]
    response = client.patch(
        f"/courses/{course_b_id}",
        json={"code": "AAA"},
        params={"user_id": admin_id},
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /courses/{id}  — admin only
# ---------------------------------------------------------------------------

def test_delete_course_admin_success():
    admin_id = create_admin()
    course_resp = create_course(admin_id)
    course_id = course_resp.json()["data"]["id"]
    response = client.delete(f"/courses/{course_id}", params={"user_id": admin_id})
    assert response.status_code == 200
    # Confirm gone
    get_resp = client.get(f"/courses/{course_id}")
    assert get_resp.status_code == 404


def test_delete_course_student_forbidden():
    admin_id = create_admin()
    student_id = create_student()
    course_resp = create_course(admin_id)
    course_id = course_resp.json()["data"]["id"]
    response = client.delete(f"/courses/{course_id}", params={"user_id": student_id})
    assert response.status_code == 403


def test_delete_course_not_found():
    admin_id = create_admin()
    response = client.delete("/courses/9999", params={"user_id": admin_id})
    assert response.status_code == 404

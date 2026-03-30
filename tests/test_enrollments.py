"""
Tests for Enrollment endpoints:

Student-only:
  POST   /enrollments/enroll                  - enroll in course
  DELETE /enrollments/deregister              - deregister from course
  GET    /enrollments/student/{user_id}       - get own enrollments

Admin-only:
  GET    /enrollments/                        - get all enrollments
  GET    /enrollments/course/{course_id}      - get enrollments by course
  DELETE /enrollments/force-deregister        - force deregister a student
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
    resp = client.post("/users/", json={"name": "Admin", "email": "admin@example.com", "role": "admin"})
    return int(resp.json()["data"]["id"])


def create_student(email="student@example.com"):
    resp = client.post("/users/", json={"name": "Student", "email": email, "role": "student"})
    return int(resp.json()["data"]["id"])


def create_course(admin_id: int, code: str = "CS101"):
    resp = client.post(
        "/courses/",
        json={"title": "Intro to CS", "code": code},
        params={"user_id": admin_id},
    )
    return resp.json()["data"]["id"]


def enroll(student_id: int, course_id: int):
    return client.post(
        "/enrollments/enroll",
        params={"user_id": student_id, "course_id": course_id},
    )


# ---------------------------------------------------------------------------
# POST /enrollments/enroll  — student only
# ---------------------------------------------------------------------------

def test_enroll_student_success():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    response = enroll(student_id, course_id)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == student_id
    assert data["course_id"] == course_id


def test_enroll_duplicate_fails():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    enroll(student_id, course_id)
    response = enroll(student_id, course_id)
    assert response.status_code == 400


def test_enroll_nonexistent_student():
    admin_id = create_admin()
    course_id = create_course(admin_id)
    response = client.post("/enrollments/enroll", params={"user_id": 9999, "course_id": course_id})
    # user_id 9999 doesn't exist → dependency returns 404
    assert response.status_code == 404


def test_enroll_nonexistent_course():
    student_id = create_student()
    response = client.post("/enrollments/enroll", params={"user_id": student_id, "course_id": 9999})
    assert response.status_code == 404


def test_enroll_admin_forbidden():
    admin_id = create_admin()
    course_id = create_course(admin_id)
    response = client.post(
        "/enrollments/enroll",
        params={"user_id": admin_id, "course_id": course_id},
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# DELETE /enrollments/deregister  — student only
# ---------------------------------------------------------------------------

def test_deregister_student_success():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    enroll(student_id, course_id)
    response = client.delete(
        "/enrollments/deregister",
        params={"user_id": student_id, "course_id": course_id},
    )
    assert response.status_code == 200


def test_deregister_not_enrolled():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    response = client.delete(
        "/enrollments/deregister",
        params={"user_id": student_id, "course_id": course_id},
    )
    assert response.status_code == 404


def test_deregister_admin_forbidden():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    enroll(student_id, course_id)
    response = client.delete(
        "/enrollments/deregister",
        params={"user_id": admin_id, "course_id": course_id},
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# GET /enrollments/student/{user_id}  — student only
# ---------------------------------------------------------------------------

def test_get_student_enrollments_success():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    enroll(student_id, course_id)
    response = client.get(f"/enrollments/student/{student_id}", params={"user_id": student_id})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == student_id


def test_get_student_enrollments_empty():
    student_id = create_student()
    response = client.get(f"/enrollments/student/{student_id}", params={"user_id": student_id})
    assert response.status_code == 200
    assert response.json() == []


def test_get_student_enrollments_admin_forbidden():
    admin_id = create_admin()
    student_id = create_student()
    response = client.get(f"/enrollments/student/{student_id}", params={"user_id": admin_id})
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# GET /enrollments/  — admin only
# ---------------------------------------------------------------------------

def test_admin_get_all_enrollments_success():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    enroll(student_id, course_id)
    response = client.get("/enrollments/", params={"user_id": admin_id})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_admin_get_all_enrollments_student_forbidden():
    student_id = create_student()
    response = client.get("/enrollments/", params={"user_id": student_id})
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# GET /enrollments/course/{course_id}  — admin only
# ---------------------------------------------------------------------------

def test_admin_get_course_enrollments_success():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    enroll(student_id, course_id)
    response = client.get(f"/enrollments/course/{course_id}", params={"user_id": admin_id})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["course_id"] == course_id


def test_admin_get_course_enrollments_student_forbidden():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    response = client.get(f"/enrollments/course/{course_id}", params={"user_id": student_id})
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# DELETE /enrollments/force-deregister  — admin only
# ---------------------------------------------------------------------------

def test_admin_force_deregister_success():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    enroll(student_id, course_id)
    response = client.delete(
        "/enrollments/force-deregister",
        params={"user_id": admin_id, "student_id": student_id, "course_id": course_id},
    )
    assert response.status_code == 200
    # Confirm enrollment is gone
    all_resp = client.get("/enrollments/", params={"user_id": admin_id})
    assert len(all_resp.json()) == 0


def test_admin_force_deregister_not_enrolled():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    response = client.delete(
        "/enrollments/force-deregister",
        params={"user_id": admin_id, "student_id": student_id, "course_id": course_id},
    )
    assert response.status_code == 404


def test_admin_force_deregister_student_forbidden():
    admin_id = create_admin()
    student_id = create_student()
    course_id = create_course(admin_id)
    enroll(student_id, course_id)
    response = client.delete(
        "/enrollments/force-deregister",
        params={"user_id": student_id, "student_id": student_id, "course_id": course_id},
    )
    assert response.status_code == 403

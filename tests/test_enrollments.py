import pytest

@pytest.fixture
def setup_data(client):
    # create student
    r1 = client.post("/users/", json={"name": "Alice", "email": "alice@test.com", "role": "student"})
    student_id = r1.json()["id"]
    
    # create admin
    r2 = client.post("/users/", json={"name": "Bob", "email": "bob@test.com", "role": "admin"})
    admin_id = r2.json()["id"]
    
    # create course
    headers = {"x-user-role": "admin"}
    r3 = client.post("/courses/", json={"title": "Math 101", "code": "MTH101"}, headers=headers)
    course_id = r3.json()["id"]
    
    return {"student_id": student_id, "admin_id": admin_id, "course_id": course_id}

def test_enroll_student_success(client, setup_data):
    # Only student can enroll
    headers = {"x-user-role": "student"}
    payload = {"user_id": setup_data["student_id"], "course_id": setup_data["course_id"]}
    response = client.post("/enrollments/", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["user_id"] == setup_data["student_id"]

def test_enroll_admin_forbidden(client, setup_data):
    headers = {"x-user-role": "admin"}
    payload = {"user_id": setup_data["admin_id"], "course_id": setup_data["course_id"]}
    response = client.post("/enrollments/", json=payload, headers=headers)
    assert response.status_code == 403

def test_enroll_duplicate(client, setup_data):
    headers = {"x-user-role": "student"}
    payload = {"user_id": setup_data["student_id"], "course_id": setup_data["course_id"]}
    client.post("/enrollments/", json=payload, headers=headers)
    response = client.post("/enrollments/", json=payload, headers=headers)
    assert response.status_code == 400
    assert "already enrolled" in response.json()["detail"].lower()

def test_deregister_student(client, setup_data):
    headers = {"x-user-role": "student"}
    payload = {"user_id": setup_data["student_id"], "course_id": setup_data["course_id"]}
    res = client.post("/enrollments/", json=payload, headers=headers)
    enroll_id = res.json()["id"]
    
    dereg_headers = {"x-user-role": "student", "x-user-id": str(setup_data["student_id"])}
    del_response = client.delete(f"/enrollments/{enroll_id}", headers=dereg_headers)
    assert del_response.status_code == 204

def test_get_student_enrollments(client, setup_data):
    headers = {"x-user-role": "student"}
    payload = {"user_id": setup_data["student_id"], "course_id": setup_data["course_id"]}
    client.post("/enrollments/", json=payload, headers=headers)
    
    response = client.get(f"/enrollments/students/{setup_data['student_id']}", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_admin_get_all_enrollments(client, setup_data):
    # Enroll student
    s_headers = {"x-user-role": "student"}
    payload = {"user_id": setup_data["student_id"], "course_id": setup_data["course_id"]}
    client.post("/enrollments/", json=payload, headers=s_headers)
    
    # Admin gets all
    a_headers = {"x-user-role": "admin"}
    response = client.get("/enrollments/", headers=a_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    
def test_admin_force_deregister(client, setup_data):
    # Enroll student
    s_headers = {"x-user-role": "student"}
    payload = {"user_id": setup_data["student_id"], "course_id": setup_data["course_id"]}
    res = client.post("/enrollments/", json=payload, headers=s_headers)
    enroll_id = res.json()["id"]
    
    # Admin forces deregister
    a_headers = {"x-user-role": "admin"}
    del_response = client.delete(f"/enrollments/{enroll_id}/force", headers=a_headers)
    assert del_response.status_code == 204

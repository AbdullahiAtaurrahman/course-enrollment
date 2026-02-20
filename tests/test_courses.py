def test_list_courses_empty(client):
    response = client.get("/courses/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_course_as_admin(client):
    headers = {"x-user-role": "admin"}
    response = client.post("/courses/", json={"title": "Math 101", "code": "MTH101"}, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Math 101"

def test_create_course_as_student_forbidden(client):
    headers = {"x-user-role": "student"}
    response = client.post("/courses/", json={"title": "Math 101", "code": "MTH101"}, headers=headers)
    assert response.status_code == 403

def test_create_course_missing_role(client):
    response = client.post("/courses/", json={"title": "Math 101", "code": "MTH101"})
    assert response.status_code == 422 # missing header

def test_create_course_duplicate_code(client):
    headers = {"x-user-role": "admin"}
    client.post("/courses/", json={"title": "Math 101", "code": "MTH101"}, headers=headers)
    response = client.post("/courses/", json={"title": "Advanced Math", "code": "MTH101"}, headers=headers)
    assert response.status_code == 400
    assert "unique" in response.json()["detail"].lower()

def test_update_course(client):
    headers = {"x-user-role": "admin"}
    res = client.post("/courses/", json={"title": "Math 101", "code": "MTH101"}, headers=headers)
    course_id = res.json()["id"]
    
    response = client.put(f"/courses/{course_id}", json={"title": "Math 102", "code": "MTH102"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Math 102"
    
def test_delete_course(client):
    headers = {"x-user-role": "admin"}
    res = client.post("/courses/", json={"title": "Math 101", "code": "MTH101"}, headers=headers)
    course_id = res.json()["id"]
    
    response = client.delete(f"/courses/{course_id}", headers=headers)
    assert response.status_code == 204
    
    response2 = client.get(f"/courses/{course_id}")
    assert response2.status_code == 404

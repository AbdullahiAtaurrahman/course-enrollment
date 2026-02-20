def test_create_user(client):
    response = client.post("/users/", json={"name": "Alice", "email": "alice@test.com", "role": "student"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data

def test_create_user_invalid_role(client):
    response = client.post("/users/", json={"name": "Bob", "email": "bob@test.com", "role": "hacker"})
    assert response.status_code == 422 # Pydantic validation error

def test_list_users(client):
    client.post("/users/", json={"name": "Alice", "email": "alice@test.com", "role": "student"})
    client.post("/users/", json={"name": "Bob", "email": "bob@test.com", "role": "admin"})
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_user(client):
    res = client.post("/users/", json={"name": "Alice", "email": "alice@test.com", "role": "student"})
    user_id = res.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

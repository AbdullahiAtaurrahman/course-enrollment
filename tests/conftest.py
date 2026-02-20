import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import users_db, courses_db, enrollments_db

@pytest.fixture(scope="function")
def client():
    # Clear DB before each test
    users_db.clear()
    courses_db.clear()
    enrollments_db.clear()
    return TestClient(app)

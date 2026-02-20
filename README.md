# Course Enrollment System

A RESTful API built with FastAPI that manages a course enrollment system with role-based interactions. The system uses in-memory data storage and has robust pydantic validation.

## Entities
- User (id, name, email, role: student or admin)
- Course (id, title, code)
- Enrollment (id, user_id, course_id)

## Prerequisites
- Python 3.8+
- `fastapi`
- `uvicorn`
- `pytest`
- `httpx` (for testing)

## Setup and Install
```bash
# Navigate to project director
cd course_enrollment_project

# Create virtual environment (optional but recommended)
python -m venv venv
# Activate virtual environment
# On Windows: venv\Scripts\activate
# On Unix: source venv/bin/activate

# Install requirements
pip install fastapi uvicorn pydantic pytest httpx
```

## How to Run the API
Run the following command to start the Uvicorn server:
```bash
uvicorn app.main:app --reload
```
The interactive API docs will be available at: http://127.0.0.1:8000/docs

### Note on Authentication
Authentication is simulated for the purpose of demonstrating role-based access. 
Provide roles (`student` or `admin`) via the `x-user-role` HTTP header when calling protected endpoints.
Provide the user ID (`x-user-id`) via headers when deregistering yourself from a course to prove ownership.

## How to run the tests
Tests are written with `pytest` and use standard `httpx` testing clients. 
Ensure you are in the `course_enrollment_project` root directory:
```bash
pytest tests/ -v
```

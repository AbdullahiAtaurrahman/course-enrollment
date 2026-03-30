# course-enrollment

A RESTful API for managing course enrollments, built with FastAPI.

## Features

- **User Management**: Create and view users. Supports two roles: `student` and `admin`. Validates name (non-empty) and email (format).
- **Course Management**: Admins can create, update, and delete courses. Any user can view courses. Validates non-empty titles and unique course codes.
- **Enrollment Management**: Students can enroll and deregister from courses. Admins can view all enrollments, filter by course, and force-deregister students.

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd course-enrollment
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi "uvicorn[standard]" pytest httpx email-validator
   ```

## Running the API

```bash
uvicorn app.main:app --reload
```

- API base URL: `http://127.0.0.1:8000`
- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`
- The `--reload` flag auto-restarts the server on code changes.

## Running the Tests

```bash
pytest tests/ -v
```

Run all tests from the project root directory. To run a specific file:

```bash
pytest tests/test_users.py -v
pytest tests/test_courses.py -v
pytest tests/test_enrollments.py -v
```

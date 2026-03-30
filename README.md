# course_enrollment_p
An aid designed to keep track of students who enroll in certain courses

## Features
- **User Management**: Create and view users. Supports two roles: `student` and `admin`. Includes validation for names and emails.
- **Course Management**: Admins can manage courses (Create, Update, Delete) with validation strictly on non-empty titles and unique course codes. Any user can view courses.
- **Enrollment Management**: Students can freely enroll and deregister themselves from courses. Admins can view all enrollments or enforce deregistration.

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd course_enrollment_p
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS and Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   Ensure you have FastAPI and Uvicorn installed. If you have a `requirements.txt` file, run `pip install -r requirements.txt`. Otherwise, install the packages directly:
   ```bash
   pip install fastapi "uvicorn[standard]"
   ```

## Starting the FastAPI Server

To start the FastAPI server, use `uvicorn` to run the main application file (`app/main.py`):

```bash
uvicorn app.main:app --reload
```

- The server will be accessible at: `http://127.0.0.1:8000`
- You can access the interactive API documentation (Swagger UI) at: `http://127.0.0.1:8000/docs`
- The `--reload` flag is used for local development to automatically restart the server when code changes are detected.

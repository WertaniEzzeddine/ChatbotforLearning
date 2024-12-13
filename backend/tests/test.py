import time
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import User, Course
import pylint.lint

# Constants
MAX_RESPONSE_TIME = 1  # seconds
MIN_PYLINT_SCORE = 8  # Minimum acceptable pylint score

# Use TestClient for API functional tests
client = TestClient(app)

# Fixtures for database session
@pytest.fixture(scope="module")
def test_db():
    """
    Provides a test database session for the duration of the module.
    """
    db = SessionLocal()
    yield db
    db.close()

# Unit Tests
def test_user_creation(test_db: Session):
    """
    Tests the creation of a user in the database.
    """
    user = User(full_name="Test User", email="test@example.com", password="password123")
    test_db.add(user)
    test_db.commit()
    fetched_user = test_db.query(User).filter(User.email == "test@example.com").first()
    assert fetched_user is not None
    assert fetched_user.email == "test@example.com"
    assert fetched_user.full_name == "Test User"
    assert fetched_user.password == "password123"

def test_user_course_relationship(test_db: Session):
    """
    Tests the relationship between a user and their courses.
    """
    user = User(full_name="Test User", email="user_with_courses@example.com", password="password123")
    test_db.add(user)
    test_db.commit()

    course = Course(name="User's Course", user_id=user.id, summary="Test Summary", exam="Test Exam", exam_correction="Test Correction")
    test_db.add(course)
    test_db.commit()

    fetched_user = test_db.query(User).filter(User.email == "user_with_courses@example.com").first()
    assert fetched_user is not None
    assert len(fetched_user.courses) == 1
    assert fetched_user.courses[0].name == "User's Course"

# Functional Tests
def test_user_registration():
    """
    Tests user registration via the API.
    """
    response = client.post(
        "/register",
        json={"full_name": "Test User", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert "id" in response.json()

def test_user_login():
    """
    Tests user login via the API.
    """
    response = client.post(
        "/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# Integration Tests
def test_course_creation_api(test_db: Session):
    """
    Tests course creation via the API.
    """
    user = test_db.query(User).filter(User.email == "test@example.com").first()
    user_id = user.id

    response = client.post(
        "/courses",
        json={
            "name": "Test Course",
            "user_id": user_id,
            "summary": "Summary",
            "exam": "Exam",
            "exam_correction": "Correction",
            "conversation": {}
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Course"

# Performance Tests
def test_api_performance():
    """
    Tests the API's performance for the /courses endpoint.
    """
    start_time = time.time()
    response = client.get("/courses")
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < MAX_RESPONSE_TIME

# Code Quality Tests
def test_code_quality():
    """
    Tests the code quality using pylint.
    """
    try:
        results = pylint.lint.Run(["main.py", "models.py", "schemas.py", "database.py"], do_exit=False)
        assert results.linter.stats["global_note"] >= MIN_PYLINT_SCORE
    except Exception as e:
        pytest.fail(f"Code quality check failed: {e}")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Zehcnas200@localhost/testing"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
client = TestClient(app)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
@pytest.fixture(scope="function", autouse=True)
def transactional_test():
    connection = engine.connect()
    transaction = connection.begin()    
    session = TestingSessionLocal(bind=connection)
    yield session
    transaction.rollback()
    connection.close()

def test_system_login_and_course_upload():
    # Step 1: Register a user
    register_payload = {
        "full_name": "Test User",
        "email": "testuser2022@example.com",
        "password": "password123"
    }
    register_response = client.post("/register", json=register_payload)
    assert register_response.status_code == 200

    # Step 2: Login
    login_payload = {
        "email": "testuser2022@example.com",
        "password": "password123"
    }
    login_response = client.post("/login", json=login_payload)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    assert access_token is not None

    # Step 3: Upload a course
    files = {
        "file": ("test_course.pdf", b"%PDF-1.4 test content", "application/pdf")
    }
    course_payload = {
        "name": "Test Course",
        "user_id": login_response.json()["user"]["id"]
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    upload_response = client.post("/upload_course/", data=course_payload, files=files, headers=headers)
    assert upload_response.status_code == 200
    assert upload_response.json()["message"] == "Course uploaded successfully!"

    # Step 4: Retrieve uploaded courses
    courses_response = client.get("/courses/{course_payload.user_id}", headers=headers)
    assert courses_response.status_code == 200
    assert len(courses_response.json()["courses"]) > 0

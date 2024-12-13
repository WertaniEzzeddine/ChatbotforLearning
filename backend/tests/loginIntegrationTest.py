import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os
load_dotenv()
# MySQL Connection URL
DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = DATABASE_URL
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
def test_login_user():
    payload = {
        
        "email": "johndoee@example.com",
        "password": "123"
    }
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == 'Login successful'
    
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from main import app
from db.dependencies import get_db
from db.db import init_db
from db.base import Base
from db.db import engine  

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use in-memory database for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the `get_db` dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the tables
Base.metadata.create_all(bind=engine)

# Test client
client = TestClient(app)

# Test data
TEST_USER = {
    "name": "Test",
    "last_name": "Test",
    "username": "testuser",
    "password": "ThisIsPassword1",
    "email": "testuser@testuser.com"
}

TEST_LOGIN = {
    "email": "testuser@testuser.com",
    "password": "ThisIsPassword1"
}

NOT_REGISTERED_LOGIN = {
    "email": "notregistered@testuser.com",
    "password": "notregistered12"
}

# Fixture to clear the database before each test
@pytest.fixture(autouse=True)
def clear_db():
    # Clear all tables before each test
    db = TestingSessionLocal()
    # Drop all tables and recreate them (reset the DB state)
    Base.metadata.drop_all(bind=engine)  # Drop tables
    Base.metadata.create_all(bind=engine)  # Recreate tables
    db.close()

@pytest.fixture
def setup_test_data():
    # Setup test data if needed
    db = TestingSessionLocal()
    yield
    db.close()

def test_register_user(setup_test_data):
    response = client.post("/api/register", json=TEST_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == TEST_USER["email"]

def test_register_existing_user(setup_test_data):
    client.post("/api/register", json=TEST_USER)  # First registration
    response = client.post("/api/register", json=TEST_USER)  # Second registration
    assert response.status_code == 400
    assert response.json()["detail"] == "Email is already in use"

def test_login_user(setup_test_data):
    client.post("/api/register", json=TEST_USER)  # Register the user
    response = client.post("/api/login", json=TEST_LOGIN)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_user(setup_test_data):
    response = client.post("/api/login", json=NOT_REGISTERED_LOGIN)  # No user registered
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_forgot_password(setup_test_data):
    client.post("/api/register", json=TEST_USER)  # Register the user
    response = client.post("/forgot-password", json={"email": TEST_USER["email"]})
    assert response.status_code == 200
    assert response.json()["message"] == "New password has been sent to your email."

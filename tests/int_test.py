import pytest
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app # import app and init_db from your project
from db.db import init_db
from db.db import Base
from db.dependencies import get_db
from sqlalchemy.orm import Session
from db.user import User  # Import your user model


# Setup a test database for the integration tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use SQLite in-memory database or a test-specific file

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Initialize the database for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db  # Override the dependency to use the test DB

def flush_database(db: Session):
    db.query(User).delete()  # Delete all users (or you could delete other entities too)
    db.commit()

# Then call this function before each test that requires a fresh database
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    db = next(get_db())  # Get the test database session
    flush_database(db)  # Flush the database before each test
    yield db  # Run the test
    flush_database(db)  # Flush the database after each test (if needed)

# Initialize the database schema
def init_test_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)

client = TestClient(app)  # Create the test client

# Pytest fixture to handle database session for each test
@pytest.fixture(scope="function", autouse=True)
def db_session():
    # Setup the database session
    db = TestingSessionLocal()
    try:
        # Initialize the database schema before each test if not already done
        init_test_db()  # Create tables if they don't exist yet
        yield db
        # Rollback the session to ensure the database is flushed after each test
        db.rollback()
    finally:
        db.close()

    
def test_register_user_email_taken():
    client.post("/api/register", json={
        "name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "john.doe@example.com",
        "password": "password123"
    })
    
    response = client.post("/api/register", json={
        "name": "Jane",
        "last_name": "Smith",
        "username": "janesmith",
        "email": "john.doe@example.com",  # Same email as the first user
        "password": "password456"
    })
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email is already in use"

def test_user_login():
    # Register a user first
    client.post("/api/register", json={
        "name": "Jane",
        "last_name": "Smith",
        "username": "janesmith",
        "email": "jane.smith@example.com",
        "password": "password123"
    })
    
    # Login with the newly created user
    response = client.post("/api/login", json={
        "email": "jane.smith@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_user_login_invalid_credentials():
    response = client.post("/api/login", json={
        "email": "jane.smith@example.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_forgot_password():
    # Register a user
    client.post("/api/register", json={
        "name": "Alice",
        "last_name": "Wonderland",
        "username": "alicewonder",
        "email": "alice@example.com",
        "password": "securepass"
    })
    
    response = client.post("/forgot-password", json={
        "email": "alice@example.com"
    })
    
    assert response.status_code == 200
    assert response.json()["message"] == "New password has been sent to your email."

import time

def test_create_task():
    # Create a unique email and username for each test
    unique_email = f"bob.builder+{int(time.time())}@example.com"
    unique_username = f"bobbuilder_{int(time.time())}"

    # Register a user with unique email and username
    register_response = client.post("/api/register", json={
        "name": "Bob",
        "last_name": "Builder",
        "username": unique_username,
        "email": unique_email,
        "password": "builderpass"
    })
    assert register_response.status_code == 200  # Ensure registration was successful

    # Log in and get the access token
    login_response = client.post("/api/login", json={
        "email": unique_email,
        "password": "builderpass"
    })
    assert login_response.status_code == 200  # Ensure login was successful
    access_token = login_response.json().get("access_token")
    assert access_token, "No access token returned"

    # Assuming we have a team with ID 1 (or replace it with a valid team ID)
    team_assigned_id = 1  # Replace with a valid team ID

    # Create a task with the access token
    response = client.post("/api/create/task", json={
        "title": "Build a house",
        "status_task": "In Progress",
        "email_creator": unique_email,
        "description": "Build a new house in the neighborhood",
        "email_assigned": unique_email,  # Ensure this is populated
        "team_assigned": team_assigned_id  # Pass team ID instead of team name
    }, headers={"Authorization": f"Bearer {access_token}"})

    # Check if the task creation was successful
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def test_create_team():
    # Register users and login
    client.post("/api/register", json={
        "name": "Charlie",
        "last_name": "Brown",
        "username": "charlieb",
        "email": "charlie.brown@example.com",
        "password": "charliepass"
    })
    
    login_response = client.post("/api/login", json={
        "email": "charlie.brown@example.com",
        "password": "charliepass"
    })
    access_token = login_response.json()["access_token"]
    
    # Create a team
    response = client.post("/api/create-team", json={
        "teamName": "Super Team",
        "members": ["charlie.brown@example.com"]
    }, headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert response.json() == "Team has been created successfully."

def test_get_teams_for_user():
    # Register users and create a team
    client.post("/api/register", json={
        "name": "Dave",
        "last_name": "Johnson",
        "username": "davejohnson",
        "email": "dave.johnson@example.com",
        "password": "davepass"
    })
    
    login_response = client.post("/api/login", json={
        "email": "dave.johnson@example.com",
        "password": "davepass"
    })
    access_token = login_response.json()["access_token"]
    
    # Create a team and add Dave
    client.post("/api/create-team", json={
        "teamName": "Awesome Team",
        "members": ["dave.johnson@example.com"]
    }, headers={"Authorization": f"Bearer {access_token}"})
    
    # Fetch teams for the user
    response = client.post("/api/getTeamsForMembers", json={
        "email_user": "dave.johnson@example.com"
    }, headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert len(response.json()) > 0  # Ensure the user has teams

def test_update_team_members():
    # Register users and create a team
    client.post("/api/register", json={
        "name": "Eve",
        "last_name": "Miller",
        "username": "evemiller",
        "email": "eve.miller@example.com",
        "password": "evemillerpass"
    })
    
    client.post("/api/register", json={
        "name": "Frank",
        "last_name": "King",
        "username": "frankking",
        "email": "frank.king@example.com",
        "password": "frankkingpass"
    })
    
    login_response = client.post("/api/login", json={
        "email": "eve.miller@example.com",
        "password": "evemillerpass"
    })
    access_token = login_response.json()["access_token"]
    
    # Create a team
    client.post("/api/create-team", json={
        "teamName": "Project A",
        "members": ["eve.miller@example.com"]
    }, headers={"Authorization": f"Bearer {access_token}"})
    
    # Update team members
    response = client.put("/api/teams/update/members", json={
        "team_id": 1,
        "team_name": "Project A Updated",
        "members": ["eve.miller@example.com", "frank.king@example.com"]
    }, headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Team updated successfully"

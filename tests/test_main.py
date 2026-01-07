import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.models.identity import Identity

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_identity(client):
    identity_data = {
        "username": "testuser",
        "employee_id": "EMP001",
        "primary_email": "test@example.com",
        "business_role": "developer",
        "first_name": "Test",
        "last_name": "User",
        "display_name": "Test User"  # Added required field
    }
    headers = {"X-User-Role": "hr"}
    response = client.post("/api/v1/identity/", json=identity_data, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 201
    data = response.json()
    assert data["employee_id"] == "EMP001"
    assert data["primary_email"] == "test@example.com"
    assert data["business_role"] == "developer"
    assert "entitlements" in data

def test_get_identity(client):
    # First create an identity
    identity_data = {
        "username": "testuser2",
        "employee_id": "EMP002",
        "primary_email": "test2@example.com",
        "business_role": "manager",
        "first_name": "Test",
        "last_name": "Manager"
    }
    headers = {"X-User-Role": "hr"}
    create_response = client.post("/api/v1/identity/", json=identity_data, headers=headers)
    identity_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/identity/{identity_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == "EMP002"

def test_get_identities_by_role(client):
    headers = {"X-User-Role": "hr"}
    response = client.get("/api/v1/identity/role/developer", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_identity(client):
    # Create identity first
    identity_data = {
        "username": "testuser3",
        "employee_id": "EMP003",
        "primary_email": "test3@example.com",
        "business_role": "developer",
        "first_name": "Test",
        "last_name": "Developer"
    }
    headers = {"X-User-Role": "hr"}
    create_response = client.post("/api/v1/identity/", json=identity_data, headers=headers)
    identity_id = create_response.json()["id"]
    
    # Update it
    update_data = {"business_role": "manager"}
    response = client.put(f"/api/v1/identity/{identity_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["business_role"] == "manager"

def test_get_nonexistent_identity(client):
    headers = {"X-User-Role": "hr"}
    response = client.get("/api/v1/identity/999", headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_slack_service():
    from app.service.slack import SlackService
    
    service = SlackService()
    # Test with mock data since we don't have real Slack tokens
    result = await service.create_user_account("test@example.com")
    assert "user_id" in result
    assert "status" in result
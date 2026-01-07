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
        "employee_id": "EMP001",
        "email": "test@example.com",
        "business_role": "developer"
    }
    response = client.post("/api/v1/identity/", json=identity_data)
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == "EMP001"
    assert data["email"] == "test@example.com"
    assert data["business_role"] == "developer"
    assert "entitlements" in data

def test_get_identity(client):
    # First create an identity
    identity_data = {
        "employee_id": "EMP002",
        "email": "test2@example.com",
        "business_role": "manager"
    }
    create_response = client.post("/api/v1/identity/", json=identity_data)
    identity_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/identity/{identity_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == "EMP002"

def test_get_identities_by_role(client):
    response = client.get("/api/v1/identity/role/developer")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_identity(client):
    # Create identity first
    identity_data = {
        "employee_id": "EMP003",
        "email": "test3@example.com",
        "business_role": "developer"
    }
    create_response = client.post("/api/v1/identity/", json=identity_data)
    identity_id = create_response.json()["id"]
    
    # Update it
    update_data = {"business_role": "manager"}
    response = client.put(f"/api/v1/identity/{identity_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["business_role"] == "manager"

def test_get_nonexistent_identity(client):
    response = client.get("/api/v1/identity/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_slack_service():
    from app.service.slack import SlackService
    
    service = SlackService()
    # Test with mock data since we don't have real Slack tokens
    result = await service.create_user_account("test@example.com")
    assert "user_id" in result
    assert "status" in result
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.identity import IdentityService
from app.schemas.identity import Identity, IdentityCreate, IdentityUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=Identity, summary="Create New Identity", status_code=201)
async def create_identity(
    identity: IdentityCreate,
    db: Session = Depends(get_db)
):
    """
    **Create New User Identity**
    
    Creates a new user identity in the IGA system with automatic role-based provisioning.
    
    **Business Process:**
    1. Validates user information and business role
    2. Maps business role to appropriate entitlements
    3. Provisions user to target applications (Slack, etc.)
    4. Returns complete identity record with assigned entitlements
    
    **Supported Business Roles:**
    - `developer`: Development team access with code repositories and dev channels
    - `manager`: Management access with team oversight and admin permissions
    - `hr`: Human resources access with employee management capabilities
    
    **Automatic Provisioning:**
    - Slack channel assignments based on role
    - Permission sets aligned with business requirements
    - Audit trail creation for compliance
    """
    service = IdentityService(db)
    return await service.create_identity(identity)

@router.get("/{identity_id}", response_model=Identity, summary="Retrieve Identity Details")
def get_identity(identity_id: int, db: Session = Depends(get_db)):
    """
    **Retrieve User Identity Information**
    
    Fetches complete identity details including entitlements and provisioning status.
    
    **Returns:**
    - Complete user profile information
    - Current business role assignment
    - Active entitlements and permissions
    - Target application provisioning status
    - Identity creation and modification timestamps
    
    **Use Cases:**
    - User profile verification
    - Access review and audit
    - Troubleshooting provisioning issues
    - Compliance reporting
    """
    service = IdentityService(db)
    identity = service.get_identity(identity_id)
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identity

@router.get("/role/{role}", response_model=List[Identity])
def get_identities_by_role(role: str, db: Session = Depends(get_db)):
    service = IdentityService(db)
    return service.get_identities_by_role(role)

@router.put("/{identity_id}", response_model=Identity)
async def update_identity(
    identity_id: int,
    update_data: IdentityUpdate,
    db: Session = Depends(get_db)
):
    service = IdentityService(db)
    identity = await service.update_identity(identity_id, update_data)
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identity
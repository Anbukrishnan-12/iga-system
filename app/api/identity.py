from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import AuthService
from app.service.identity import IdentityService
from app.schemas.identity import Identity, IdentityCreate, IdentityUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=Identity, summary="Create New Identity", status_code=201)
async def create_identity(
    identity: IdentityCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(AuthService.verify_user_access)
):
    """
    **Create New User Identity**
    
    Creates a new user identity in the IGA system with automatic role-based provisioning.
    **Available to all authenticated users.**
    
    **Required Header:**
    - `X-User-Role`: Your business role (developer, tester, manager, hr, etc.)
    
    **Business Process:**
    1. Validates user information and business role
    2. Maps business role to appropriate entitlements
    3. Provisions user to target applications (Slack, etc.)
    4. Returns complete identity record with assigned entitlements
    
    **Supported Business Roles:**
    - `developer`, `tester`, `manager`, `hr`, `designer`, `analyst`
    - `devops`, `sales`, `marketing`, `support`, `intern`, `contractor`
    """
    try:
        service = IdentityService(db)
        return await service.create_identity(identity)
    except Exception as e:
        import logging
        logging.error(f"Error creating identity: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{identity_id}", response_model=Identity, summary="Retrieve Identity Details")
def get_identity(
    identity_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Retrieve User Identity Information** (HR Only)
    
    Fetches complete identity details including entitlements and provisioning status.
    **Restricted to HR personnel only.**
    
    **Required Header:**
    - `X-User-Role`: Must be "hr"
    
    **Returns:**
    - Complete user profile information
    - Current business role assignment
    - Active entitlements and permissions
    - Target application provisioning status
    - Identity creation and modification timestamps
    """
    service = IdentityService(db)
    identity = service.get_identity(identity_id)
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identity

@router.get("/role/{role}", response_model=List[Identity], summary="Get Identities by Role")
def get_identities_by_role(
    role: str, 
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Get All Identities by Business Role** (HR Only)
    
    Retrieves all users with a specific business role.
    **Restricted to HR personnel only.**
    
    **Required Header:**
    - `X-User-Role`: Must be "hr"
    """
    service = IdentityService(db)
    return service.get_identities_by_role(role)

@router.get("/list/all", response_model=List[Identity], summary="Get All Identities")
def get_all_identities(
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Get All Identities** (HR Only)
    
    Retrieves all users in the system.
    **Restricted to HR personnel only.**
    
    **Required Header:**
    - `X-User-Role`: Must be "hr"
    """
    service = IdentityService(db)
    return service.get_all_identities()

@router.put("/{identity_id}", response_model=Identity, summary="Update Identity")
async def update_identity(
    identity_id: int,
    update_data: IdentityUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Update User Identity** (HR Only)
    
    Updates user identity information and re-provisions access if needed.
    **Restricted to HR personnel only.**
    
    **Required Header:**
    - `X-User-Role`: Must be "hr"
    """
    service = IdentityService(db)
    identity = await service.update_identity(identity_id, update_data)
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identity
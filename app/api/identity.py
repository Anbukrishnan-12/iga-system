from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.identity import IdentityService
from app.schemas.identity import Identity, IdentityCreate, IdentityUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=Identity)
async def create_identity(
    identity: IdentityCreate,
    db: Session = Depends(get_db)
):
    service = IdentityService(db)
    return await service.create_identity(identity)

@router.get("/{identity_id}", response_model=Identity)
def get_identity(identity_id: int, db: Session = Depends(get_db)):
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
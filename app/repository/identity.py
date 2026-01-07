from sqlalchemy.orm import Session
from app.models.identity import Identity, TargetApplication
from app.schemas.identity import IdentityCreate, IdentityUpdate
from typing import Optional, List

class IdentityRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, identity: IdentityCreate) -> Identity:
        db_identity = Identity(**identity.model_dump())
        self.db.add(db_identity)
        self.db.commit()
        self.db.refresh(db_identity)
        return db_identity
    
    def get_by_id(self, identity_id: int) -> Optional[Identity]:
        return self.db.query(Identity).filter(Identity.id == identity_id).first()
    
    def get_by_email(self, email: str) -> Optional[Identity]:
        return self.db.query(Identity).filter(Identity.primary_email == email).first()
    
    def get_by_business_role(self, role: str) -> List[Identity]:
        return self.db.query(Identity).filter(Identity.business_role == role).all()
    
    def get_all(self) -> List[Identity]:
        return self.db.query(Identity).all()
    
    def update(self, identity_id: int, update_data: IdentityUpdate) -> Optional[Identity]:
        identity = self.get_by_id(identity_id)
        if identity:
            for field, value in update_data.model_dump(exclude_unset=True).items():
                setattr(identity, field, value)
            self.db.commit()
            self.db.refresh(identity)
        return identity
    
    def delete(self, identity_id: int) -> bool:
        identity = self.get_by_id(identity_id)
        if identity:
            self.db.delete(identity)
            self.db.commit()
            return True
        return False
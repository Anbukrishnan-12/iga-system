from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Identity(Base):
    __tablename__ = "identities"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    business_role = Column(String, index=True)
    entitlements = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TargetApplication(Base):
    __tablename__ = "target_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    protocol = Column(String)  # SCIM, REST, etc.
    auth_type = Column(String)  # OAuth, API Key, etc.
    base_url = Column(String)
    config = Column(JSON)
    is_active = Column(Boolean, default=True)
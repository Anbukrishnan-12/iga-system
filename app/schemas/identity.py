from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class IdentityBase(BaseModel):
    employee_id: str
    email: EmailStr
    business_role: str
    entitlements: Optional[Dict[str, Any]] = {}

class IdentityCreate(IdentityBase):
    pass

class IdentityUpdate(BaseModel):
    business_role: Optional[str] = None
    entitlements: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class Identity(IdentityBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class SlackUserRequest(BaseModel):
    email: str
    channels: Optional[list[str]] = []
    
class SlackUserResponse(BaseModel):
    user_id: str
    email: str
    status: str
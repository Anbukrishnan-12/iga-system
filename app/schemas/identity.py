from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime, date

class IdentityBase(BaseModel):
    # Primary identifiers
    username: Optional[str] = None
    employee_id: str
    external_id: Optional[str] = None
    
    # Basic Identity Information
    first_name: str
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    display_name: str
    
    # Contact Information
    primary_email: EmailStr
    secondary_email: Optional[EmailStr] = None
    mobile_phone: Optional[str] = None
    work_phone: Optional[str] = None
    
    # Employment Information
    employment_type: Optional[str] = "Employee"
    employment_status: Optional[str] = "ACTIVE"
    hire_date: Optional[date] = None
    termination_date: Optional[date] = None
    last_working_day: Optional[date] = None
    
    # Job Information - simplified
    department: Optional[str] = None
    location: Optional[str] = None
    
    # Business Role & Entitlements
    business_role: str
    entitlements: Optional[Dict[str, Any]] = {}

class IdentityCreate(IdentityBase):
    pass

class IdentityUpdate(BaseModel):
    # Basic Identity Information
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    display_name: Optional[str] = None
    
    # Contact Information
    primary_email: Optional[EmailStr] = None
    secondary_email: Optional[EmailStr] = None
    mobile_phone: Optional[str] = None
    work_phone: Optional[str] = None
    
    # Employment Information
    employment_type: Optional[str] = None
    employment_status: Optional[str] = None
    hire_date: Optional[date] = None
    termination_date: Optional[date] = None
    last_working_day: Optional[date] = None
    
    # Job Information - simplified
    department: Optional[str] = None
    location: Optional[str] = None
    
    # Business Role & Entitlements
    business_role: Optional[str] = None
    entitlements: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class Identity(IdentityBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    last_modified_by: str

class SlackUserRequest(BaseModel):
    email: str
    channels: Optional[list[str]] = []
    
class SlackUserResponse(BaseModel):
    user_id: str
    email: str
    status: str
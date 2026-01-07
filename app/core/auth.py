from fastapi import HTTPException, Header
from typing import Optional

class AuthService:
    @staticmethod
    def verify_hr_access(current_user_role: Optional[str] = Header(None, alias="X-User-Role")):
        """Verify if current user has HR privileges"""
        if not current_user_role:
            raise HTTPException(status_code=401, detail="User role header required")
        
        if current_user_role.lower() != "hr":
            raise HTTPException(
                status_code=403, 
                detail="Access denied. Only HR personnel can perform this operation."
            )
        return True
    
    @staticmethod
    def verify_user_access(current_user_role: Optional[str] = Header(None, alias="X-User-Role")):
        """Verify if user can create accounts (all roles allowed)"""
        if not current_user_role:
            raise HTTPException(status_code=401, detail="User role header required")
        
        allowed_roles = ["developer", "tester", "manager", "hr", "designer", "analyst", 
                        "devops", "sales", "marketing", "support", "intern", "contractor"]
        
        if current_user_role.lower() not in allowed_roles:
            raise HTTPException(status_code=403, detail="Invalid user role")
        
        return current_user_role.lower()
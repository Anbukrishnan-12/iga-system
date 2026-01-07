from fastapi import APIRouter, Depends
from app.core.database import engine, Base
from app.core.auth import AuthService
from app.models.identity import Identity, TargetApplication
from app.models.employee import Employee, EmployeeDocument, EmployeeSkill, EmployeeLeave, EmployeePerformance, Department

router = APIRouter()

@router.post("/init-db", summary="Initialize Database")
def initialize_database(_: bool = Depends(AuthService.verify_hr_access)):
    """
    **Initialize Database Tables** (HR Only)
    
    Creates all necessary database tables for the IGA system.
    **Restricted to HR personnel only.**
    
    **Required Header:**
    - `X-User-Role`: Must be "hr"
    """
    try:
        Base.metadata.create_all(bind=engine)
        return {
            "message": "Database initialized successfully",
            "tables_created": [
                "identities",
                "target_applications", 
                "employees",
                "employee_documents",
                "employee_skills",
                "employee_leaves",
                "employee_performance",
                "departments"
            ]
        }
    except Exception as e:
        return {"error": f"Database initialization failed: {str(e)}"}

@router.get("/db-status", summary="Database Status")
def database_status(_: bool = Depends(AuthService.verify_hr_access)):
    """
    **Check Database Status** (HR Only)
    
    Returns current database connection status.
    **Restricted to HR personnel only.**
    """
    try:
        # Test database connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return {
                "status": "connected",
                "message": "Database connection successful"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }
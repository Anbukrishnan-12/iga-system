from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import AuthService
from app.repository.employee import EmployeeRepository
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate, EmployeeSkill, EmployeeSkillCreate, EmployeeLeave, EmployeeLeaveCreate
from typing import List

router = APIRouter()

@router.post("/", response_model=Employee, summary="Create Employee Record")
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(AuthService.verify_user_access)
):
    """
    **Create New Employee Record**
    
    Creates comprehensive employee record in the database.
    **Available to all authenticated users.**
    
    **Required Header:**
    - `X-User-Role`: Your business role
    """
    repo = EmployeeRepository(db)
    return repo.create_employee(employee)

@router.get("/", response_model=List[Employee], summary="Get All Employees")
def get_all_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Get All Employee Records** (HR Only)
    
    Retrieves paginated list of all active employees.
    **Restricted to HR personnel only.**
    """
    try:
        repo = EmployeeRepository(db)
        return repo.get_all_employees(skip=skip, limit=limit)
    except Exception as e:
        # If employee table doesn't exist, return empty list
        return []

@router.get("/{employee_id}", response_model=Employee, summary="Get Employee by ID")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Get Employee Details** (HR Only)
    
    Retrieves complete employee information by ID.
    **Restricted to HR personnel only.**
    """
    repo = EmployeeRepository(db)
    employee = repo.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.get("/department/{department}", response_model=List[Employee], summary="Get Employees by Department")
def get_employees_by_department(
    department: str,
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Get Employees by Department** (HR Only)
    
    Retrieves all employees in a specific department.
    **Restricted to HR personnel only.**
    """
    repo = EmployeeRepository(db)
    return repo.get_employees_by_department(department)

@router.put("/{employee_id}", response_model=Employee, summary="Update Employee")
def update_employee(
    employee_id: int,
    update_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Update Employee Information** (HR Only)
    
    Updates employee details and information.
    **Restricted to HR personnel only.**
    """
    repo = EmployeeRepository(db)
    employee = repo.update_employee(employee_id, update_data)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.delete("/{employee_id}", summary="Deactivate Employee")
def deactivate_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Deactivate Employee** (HR Only)
    
    Deactivates employee record (soft delete).
    **Restricted to HR personnel only.**
    """
    repo = EmployeeRepository(db)
    success = repo.deactivate_employee(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deactivated successfully"}

@router.post("/{employee_id}/skills", response_model=EmployeeSkill, summary="Add Employee Skill")
def add_employee_skill(
    employee_id: int,
    skill_data: EmployeeSkillCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Add Employee Skill** (HR Only)
    
    Adds a new skill to employee profile.
    **Restricted to HR personnel only.**
    """
    skill_data.employee_id = employee_id
    repo = EmployeeRepository(db)
    return repo.add_employee_skill(skill_data)

@router.post("/{employee_id}/leave", response_model=EmployeeLeave, summary="Create Leave Request")
def create_leave_request(
    employee_id: int,
    leave_data: EmployeeLeaveCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(AuthService.verify_user_access)
):
    """
    **Create Leave Request**
    
    Creates a new leave request for employee.
    **Available to all authenticated users.**
    """
    leave_data.employee_id = employee_id
    repo = EmployeeRepository(db)
    return repo.create_leave_request(leave_data)
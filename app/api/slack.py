from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import AuthService
from app.service.slack import SlackService
from app.schemas.identity import (
    SlackUserRequest, 
    SlackUserResponse, 
    SlackCreateUserRequest,
    SlackUserSearchResponse,
    SlackDeleteResponse
)

router = APIRouter()

@router.post("/provision", response_model=SlackUserResponse, summary="Provision User to Slack")
async def provision_slack_user(request: SlackUserRequest):
    """
    **Provision User to Slack Workspace**
    
    Creates or retrieves user in Slack and assigns to specified channels.
    
    **Process:**
    1. Check if user exists in Slack by email
    2. If user doesn't exist, create new user with provided details
    3. Assign user to specified channels based on requirements
    4. Return user details and provisioning status
    
    **Request Fields:**
    - `email`: User's email address (required)
    - `first_name`: User's first name (required for new users)
    - `last_name`: User's last name (optional)
    - `channels`: List of Slack channels to assign user to
    
    **Response Status:**
    - `existing`: User already exists in Slack
    - `created`: New user created successfully
    - `failed`: User creation or provisioning failed
    """
    service = SlackService()
    result = await service.create_user_account(
        request.email, 
        request.first_name, 
        request.last_name, 
        request.channels
    )
    
    if result["status"] == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "Slack provisioning failed"))
    
    return SlackUserResponse(**result)

@router.get("/user/{email}")
async def get_slack_user(email: str):
    service = SlackService()
    user = await service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@router.post("/create-user", response_model=SlackUserResponse, summary="Create New Slack User")
async def create_new_slack_user(request: SlackCreateUserRequest):
    """
    **Create New User in Slack**
    
    Creates a brand new user in Slack workspace without checking if user already exists.
    
    **Use Cases:**
    - Force create new user account
    - Bulk user creation scenarios
    - When you're sure user doesn't exist
    
    **Request Fields:**
    - `email`: User's email address (required)
    - `first_name`: User's first name (required)
    - `last_name`: User's last name (optional)
    """
    service = SlackService()
    result = await service.create_new_user_only(
        request.email, 
        request.first_name, 
        request.last_name
    )
    
    if result["status"] == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "User creation failed"))
    
    return SlackUserResponse(**result)

@router.get("/search/{user_id}", response_model=SlackUserSearchResponse, summary="Search User by ID")
async def search_slack_user(
    user_id: str,
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Search User by Slack User ID** (HR Only)
    
    Retrieves detailed user information from Slack workspace using user ID.
    **Restricted to HR personnel only.**
    
    **Required Header:**
    - `X-User-Role`: Must be "hr"
    """
    service = SlackService()
    user = await service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found in Slack")
    
    return SlackUserSearchResponse(
        user_id=user.get("id"),
        email=user.get("profile", {}).get("email"),
        name=user.get("real_name"),
        status="found",
        is_active=not user.get("deleted", False),
        profile=user.get("profile", {})
    )

@router.delete("/delete/{user_id}", response_model=SlackDeleteResponse, summary="Delete Slack User")
async def delete_slack_user(
    user_id: str,
    _: bool = Depends(AuthService.verify_hr_access)
):
    """
    **Delete User from Slack Workspace** (HR Only)
    
    Removes or deactivates user from Slack workspace permanently.
    **Restricted to HR personnel only.**
    
    **Required Header:**
    - `X-User-Role`: Must be "hr"
    
    **Warning:** This action may be irreversible depending on Slack configuration.
    """
    service = SlackService()
    result = await service.delete_user(user_id)
    
    if result["status"] == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "User deletion failed"))
    
    message = "User deleted successfully" if result["status"] == "deleted" else "User deactivated successfully"
    
    return SlackDeleteResponse(
        user_id=user_id,
        status=result["status"],
        message=message
    )
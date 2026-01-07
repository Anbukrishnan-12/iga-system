from fastapi import APIRouter, HTTPException
from app.service.slack import SlackService
from app.schemas.identity import SlackUserRequest, SlackUserResponse

router = APIRouter()

@router.post("/provision", response_model=SlackUserResponse)
async def provision_slack_user(request: SlackUserRequest):
    service = SlackService()
    result = await service.create_user_account(request.email, request.channels)
    
    if result["status"] == "not_found":
        raise HTTPException(status_code=404, detail="User not found in Slack")
    
    return SlackUserResponse(**result)

@router.get("/user/{email}")
async def get_slack_user(email: str):
    service = SlackService()
    user = await service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
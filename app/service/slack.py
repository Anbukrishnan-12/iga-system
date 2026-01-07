import httpx
from app.core.config import settings
from typing import Dict, Any, Optional

class SlackService:
    def __init__(self):
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {settings.slack_bot_token}",
            "Content-Type": "application/json"
        }
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users.lookupByEmail",
                headers=self.headers,
                params={"email": email}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("user") if data.get("ok") else None
            return None
    
    async def invite_user_to_channel(self, user_id: str, channel_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/conversations.invite",
                headers=self.headers,
                json={"channel": channel_id, "users": user_id}
            )
            return response.status_code == 200 and response.json().get("ok", False)
    
    async def create_user_account(self, email: str, channels: list = None) -> Dict[str, Any]:
        # In real implementation, this would use Slack's SCIM API
        # For demo purposes, we'll simulate the response
        user = await self.get_user_by_email(email)
        if user:
            result = {
                "user_id": user["id"],
                "email": email,
                "status": "existing"
            }
            
            if channels:
                for channel in channels:
                    await self.invite_user_to_channel(user["id"], channel)
            
            return result
        
        return {
            "user_id": None,
            "email": email,
            "status": "not_found"
        }
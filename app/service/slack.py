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
    
    async def create_slack_user(self, email: str, first_name: str, last_name: str = None) -> Dict[str, Any]:
        """Create new user in Slack workspace"""
        async with httpx.AsyncClient() as client:
            user_data = {
                "email": email,
                "name": {
                    "given_name": first_name,
                    "family_name": last_name or ""
                },
                "userName": email.split('@')[0],
                "active": True
            }
            
            response = await client.post(
                f"{self.base_url}/scim/v1/Users",
                headers=self.headers,
                json=user_data
            )
            
            if response.status_code == 201:
                return response.json()
            return None
    
    async def get_or_create_user(self, email: str, first_name: str, last_name: str = None) -> Dict[str, Any]:
        """Get existing user or create new one"""
        # First try to get existing user
        user = await self.get_user_by_email(email)
        
        if user:
            return {
                "user_id": user["id"],
                "email": email,
                "status": "existing",
                "name": user.get("real_name", "")
            }
        
        # If user doesn't exist, create new one
        new_user = await self.create_slack_user(email, first_name, last_name)
        
        if new_user:
            return {
                "user_id": new_user.get("id"),
                "email": email,
                "status": "created",
                "name": f"{first_name} {last_name or ''}".strip()
            }
        
        return {
            "user_id": None,
            "email": email,
            "status": "failed",
            "error": "Could not create user in Slack"
        }
    async def create_user_account(self, email: str, first_name: str, last_name: str = None, channels: list = None) -> Dict[str, Any]:
        """Main method for user provisioning with channel assignment"""
        # Get or create user
        result = await self.get_or_create_user(email, first_name, last_name)
        
        # If user exists or was created successfully, assign to channels
        if result["user_id"] and channels:
            for channel in channels:
                await self.invite_user_to_channel(result["user_id"], channel)
            result["channels_assigned"] = channels
        
        return result
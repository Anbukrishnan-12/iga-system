import httpx
from app.core.config import settings
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

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
        try:
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
        except Exception as e:
            logger.error(f"Error in get_or_create_user: {str(e)}")
            return {
                "user_id": None,
                "email": email,
                "status": "error",
                "error": str(e)
            }
    async def create_user_account(self, email: str, first_name: str, last_name: str = None, channels: list = None) -> Dict[str, Any]:
        """Main method for user provisioning with channel assignment"""
        # If no Slack token configured, return mock response
        if not settings.slack_bot_token:
            return {
                "user_id": "mock_user_id",
                "email": email,
                "status": "mocked",
                "name": f"{first_name} {last_name or ''}".strip(),
                "channels_assigned": channels or []
            }
        
        # Get or create user
        result = await self.get_or_create_user(email, first_name, last_name)
        
        # If user exists or was created successfully, assign to channels
        if result["user_id"] and channels:
            for channel in channels:
                await self.invite_user_to_channel(result["user_id"], channel)
            result["channels_assigned"] = channels
        
        return result
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user details by Slack user ID"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users.info",
                headers=self.headers,
                params={"user": user_id}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("user") if data.get("ok") else None
            return None
    
    async def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete/deactivate user from Slack workspace"""
        async with httpx.AsyncClient() as client:
            # First try SCIM API for deletion
            response = await client.delete(
                f"{self.base_url}/scim/v1/Users/{user_id}",
                headers=self.headers
            )
            
            if response.status_code == 204:
                return {"status": "deleted", "user_id": user_id}
            
            # If SCIM fails, try deactivating user
            response = await client.post(
                f"{self.base_url}/admin.users.setInactive",
                headers=self.headers,
                json={"user": user_id}
            )
            
            if response.status_code == 200 and response.json().get("ok"):
                return {"status": "deactivated", "user_id": user_id}
            
            return {"status": "failed", "user_id": user_id, "error": "Could not delete user"}
    
    async def create_new_user_only(self, email: str, first_name: str, last_name: str = None) -> Dict[str, Any]:
        """Create new user without checking if exists"""
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
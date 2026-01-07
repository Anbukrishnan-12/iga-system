from sqlalchemy.orm import Session
from app.repository.identity import IdentityRepository
from app.schemas.identity import IdentityCreate, IdentityUpdate, Identity
from app.service.slack import SlackService
from typing import List, Optional, Dict, Any

class IdentityService:
    def __init__(self, db: Session):
        self.repository = IdentityRepository(db)
        self.slack_service = SlackService()
    
    async def create_identity(self, identity_data: IdentityCreate) -> Identity:
        # Apply business role mapping
        entitlements = self._map_business_role_to_entitlements(identity_data.business_role)
        identity_data.entitlements = entitlements
        
        # Create identity
        identity = self.repository.create(identity_data)
        
        # Provision to target applications
        await self._provision_to_targets(identity)
        
        return identity
    
    def get_identity(self, identity_id: int) -> Optional[Identity]:
        return self.repository.get_by_id(identity_id)
    
    def get_identities_by_role(self, role: str) -> List[Identity]:
        return self.repository.get_by_business_role(role)
    
    async def update_identity(self, identity_id: int, update_data: IdentityUpdate) -> Optional[Identity]:
        identity = self.repository.update(identity_id, update_data)
        if identity and update_data.business_role:
            # Re-provision if business role changed
            await self._provision_to_targets(identity)
        return identity
    
    def _map_business_role_to_entitlements(self, business_role: str) -> Dict[str, Any]:
        """Map business roles to entitlements"""
        role_mappings = {
            "developer": {
                "slack": {"channels": ["#dev-team", "#general", "#tech-updates"]},
                "permissions": ["read", "write", "code_access"]
            },
            "tester": {
                "slack": {"channels": ["#qa-team", "#general", "#bug-reports"]},
                "permissions": ["read", "write", "test_access"]
            },
            "manager": {
                "slack": {"channels": ["#management", "#general", "#leadership"]},
                "permissions": ["read", "write", "admin", "team_management"]
            },
            "hr": {
                "slack": {"channels": ["#hr", "#general", "#announcements"]},
                "permissions": ["read", "write", "user_management", "employee_data"]
            },
            "designer": {
                "slack": {"channels": ["#design-team", "#general", "#creative"]},
                "permissions": ["read", "write", "design_tools"]
            },
            "analyst": {
                "slack": {"channels": ["#analytics", "#general", "#data-insights"]},
                "permissions": ["read", "write", "data_access", "reports"]
            },
            "devops": {
                "slack": {"channels": ["#devops", "#general", "#infrastructure", "#alerts"]},
                "permissions": ["read", "write", "admin", "infrastructure_access"]
            },
            "sales": {
                "slack": {"channels": ["#sales", "#general", "#customer-updates"]},
                "permissions": ["read", "write", "crm_access"]
            },
            "marketing": {
                "slack": {"channels": ["#marketing", "#general", "#campaigns"]},
                "permissions": ["read", "write", "marketing_tools"]
            },
            "support": {
                "slack": {"channels": ["#support", "#general", "#customer-issues"]},
                "permissions": ["read", "write", "support_tools"]
            },
            "intern": {
                "slack": {"channels": ["#general", "#interns"]},
                "permissions": ["read"]
            },
            "contractor": {
                "slack": {"channels": ["#general", "#contractors"]},
                "permissions": ["read", "limited_write"]
            }
        }
        # Return default entitlements for unknown roles
        return role_mappings.get(business_role.lower(), {
            "slack": {"channels": ["#general"]},
            "permissions": ["read"]
        })
    
    async def _provision_to_targets(self, identity: Identity):
        """Provision identity to target applications"""
        entitlements = identity.entitlements or {}
        
        # Provision to Slack
        if "slack" in entitlements:
            slack_config = entitlements["slack"]
            channels = slack_config.get("channels", [])
            await self.slack_service.create_user_account(
                identity.primary_email, 
                identity.first_name, 
                identity.last_name, 
                channels
            )
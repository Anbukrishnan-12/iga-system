<<<<<<< HEAD
# IGA System - Identity Governance & Administration

A minimal FastAPI-based Identity Governance & Administration system with Slack integration.

## Features

- **Identity Management**: Create, read, update identities with business role mapping
- **Business Role Mapping**: Automatic entitlement assignment based on roles
- **Slack Integration**: Provision users to Slack channels based on entitlements
- **Target Application Support**: Extensible framework for multiple target applications
- **CRUD Operations**: Full REST API for identity management

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Configure environment variables in `.env`:
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
```

3. Initialize database:
```bash
python init_db.py
```

4. Run the application:
```bash
python -m app.main
```

## API Endpoints

- `POST /api/v1/identity/` - Create identity
- `GET /api/v1/identity/{id}` - Get identity by ID
- `GET /api/v1/identity/role/{role}` - Get identities by business role
- `PUT /api/v1/identity/{id}` - Update identity
- `POST /api/v1/slack/provision` - Provision Slack user
- `GET /api/v1/slack/user/{email}` - Get Slack user info

## Testing

```bash
pytest tests/
```

## Business Role Mappings

- **developer**: Access to #dev-team, #general channels
- **manager**: Access to #management, #general channels with admin permissions
- **hr**: Access to #hr, #general channels with user management permissions
=======
"# iga-system" 
>>>>>>> 830a5ffb3433f0f1035532a1baa3b0dc6f1821bc

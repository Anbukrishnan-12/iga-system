from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api.identity import router as identity_router
from app.api.slack import router as slack_router
from app.api.employee import router as employee_router
from app.api.database import router as database_router

app = FastAPI(
    title="IGA System - Identity Governance & Administration",
    description="""
    ## Enterprise Identity Management Platform
    
    **IGA System** provides comprehensive identity governance and administration capabilities for modern enterprises.
    
    ### Key Features
    - **Identity Lifecycle Management**: Complete CRUD operations for user identities
    - **Role-Based Access Control**: Automated entitlement provisioning based on business roles
    - **Multi-Application Integration**: Seamless provisioning to target applications
    - **Slack Integration**: Direct user provisioning to Slack channels
    - **Audit & Compliance**: Full audit trail for identity operations
    
    ### Business Roles Supported
    - **Developer**: Access to development channels and resources
    - **Manager**: Administrative access with team management capabilities  
    - **HR**: User management permissions and HR-specific channels
    
    ### API Standards
    - RESTful API design following OpenAPI 3.0 specifications
    - JSON request/response format
    - HTTP status codes for proper error handling
    - Comprehensive input validation
    
    ### Support
    For technical support or business inquiries, contact our enterprise support team.
    """,
    version="1.0.0",
    contact={
        "name": "IGA System Support",
        "email": "support@igasystem.com",
        "url": "https://igasystem.com/support"
    },
    license_info={
        "name": "Enterprise License",
        "url": "https://igasystem.com/license"
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Identity Management",
            "description": "Core identity lifecycle operations including create, read, update, and delete functionalities."
        },
        {
            "name": "Slack Integration", 
            "description": "Slack workspace integration for automated user provisioning and channel management."
        },
        {
            "name": "Employee Management",
            "description": "Complete employee lifecycle management including personal information, skills, and leave management."
        },
        {
            "name": "Database Administration",
            "description": "Database initialization and management endpoints for system administrators."
        },
        {
            "name": "System Health",
            "description": "System monitoring and health check endpoints for operational visibility."
        }
    ]
)

app.include_router(identity_router, prefix="/api/v1/identity", tags=["Identity Management"])
app.include_router(slack_router, prefix="/api/v1/slack", tags=["Slack Integration"])
app.include_router(employee_router, prefix="/api/v1/employee", tags=["Employee Management"])
app.include_router(database_router, prefix="/api/v1/admin", tags=["Database Administration"])

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IGA System - Identity Governance & Administration</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; }
        .header h1 { font-size: 3rem; margin-bottom: 0.5rem; }
        .header p { font-size: 1.2rem; opacity: 0.9; }
        .nav { background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 1rem 0; }
        .nav-links { display: flex; gap: 2rem; list-style: none; }
        .nav-links a { text-decoration: none; color: #333; font-weight: 500; padding: 0.5rem 1rem; border-radius: 5px; transition: all 0.3s; }
        .nav-links a:hover { background: #667eea; color: white; }
        .hero { padding: 4rem 0; background: #f8f9fa; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 3rem; }
        .feature { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .feature h3 { color: #667eea; margin-bottom: 1rem; }
        .cta { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 0; text-align: center; }
        .btn { display: inline-block; background: white; color: #667eea; padding: 1rem 2rem; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 0.5rem; transition: all 0.3s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .footer { background: #343a40; color: white; padding: 2rem 0; text-align: center; }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1>IGA System</h1>
            <p>Identity Governance & Administration Platform</p>
        </div>
    </header>
    <nav class="nav">
        <div class="container">
            <ul class="nav-links">
                <li><a href="/docs">API Documentation</a></li>
                <li><a href="/health">Health Check</a></li>
            </ul>
        </div>
    </nav>
    <section class="hero">
        <div class="container">
            <h2>Enterprise Identity Management Made Simple</h2>
            <p>Streamline user provisioning, role management, and application access with our comprehensive IGA solution.</p>
            <div class="features">
                <div class="feature">
                    <h3>🔐 Identity Management</h3>
                    <p>Complete CRUD operations for user identities with automated business role mapping and entitlement assignment.</p>
                </div>
                <div class="feature">
                    <h3>🎯 Role-Based Access</h3>
                    <p>Automatic entitlement provisioning based on business roles - developer, manager, HR with appropriate permissions.</p>
                </div>
                <div class="feature">
                    <h3>💬 Slack Integration</h3>
                    <p>Seamless user provisioning to Slack channels based on role entitlements and organizational structure.</p>
                </div>
                <div class="feature">
                    <h3>🔌 Extensible Framework</h3>
                    <p>Built-in support for multiple target applications with SCIM, REST APIs, and custom connectors.</p>
                </div>
            </div>
        </div>
    </section>
    <section class="cta">
        <div class="container">
            <h2>Get Started with IGA System</h2>
            <p>Explore our comprehensive API documentation and start managing identities today</p>
            <a href="/docs" class="btn">API Documentation</a>
            <a href="/health" class="btn">System Status</a>
        </div>
    </section>
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 IGA System. Enterprise Identity Governance & Administration Platform.</p>
        </div>
    </footer>
</body>
</html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/health", tags=["System Health"], summary="System Health Check")
async def health_check():
    """
    **System Health Check Endpoint**
    
    Returns the current operational status of the IGA System including:
    - Service availability status
    - System version information
    - Service identification
    
    This endpoint is used by:
    - Load balancers for health monitoring
    - CI/CD pipelines for deployment verification
    - Monitoring systems for uptime tracking
    - Operations teams for system diagnostics
    
    **Response Format:**
    - `status`: Current system status (healthy/unhealthy)
    - `service`: Service name identifier
    - `version`: Current deployed version
    """
    return {"status": "healthy", "service": "IGA System", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8090))
    uvicorn.run(app, host="0.0.0.0", port=port)
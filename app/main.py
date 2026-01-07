from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api.identity import router as identity_router
from app.api.slack import router as slack_router

app = FastAPI(
    title="IGA System - Identity Governance & Administration",
    description="Enterprise Identity Management Platform with Slack Integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(identity_router, prefix="/api/v1/identity", tags=["Identity Management"])
app.include_router(slack_router, prefix="/api/v1/slack", tags=["Slack Integration"])

@app.get("/", response_class=HTMLResponse)
async def homepage():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "IGA System", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8090))
    uvicorn.run(app, host="0.0.0.0", port=port)
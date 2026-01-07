from fastapi import FastAPI
from app.core.config import settings
from app.api.identity import router as identity_router
from app.api.slack import router as slack_router

app = FastAPI(title="IGA System", version="1.0.0")

app.include_router(identity_router, prefix="/api/v1/identity", tags=["identity"])
app.include_router(slack_router, prefix="/api/v1/slack", tags=["slack"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8090))
    uvicorn.run(app, host="0.0.0.0", port=port)
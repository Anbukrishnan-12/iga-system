#!/usr/bin/env python3
"""
Production startup script with database initialization
"""
import os
import uvicorn
from sqlalchemy import create_engine, inspect

# Initialize database on startup
def init_db_if_needed():
    """Initialize database if tables don't exist"""
    try:
        from app.core.database import engine, Base
        from app.models.identity import Identity, TargetApplication
        
        # Check if tables exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        if 'identities' not in existing_tables:
            print("🔧 Initializing database tables...")
            Base.metadata.create_all(bind=engine)
            print("✅ Database initialized successfully!")
        else:
            print("✅ Database tables already exist")
            
    except Exception as e:
        print(f"⚠️ Database initialization warning: {str(e)}")
        # Continue anyway - let the app handle it

if __name__ == "__main__":
    print("🚀 Starting IGA System Production Server...")
    
    # Initialize database
    init_db_if_needed()
    
    # Start server
    port = int(os.environ.get("PORT", 8090))
    print(f"🌐 Server starting on port {port}")
    
    from app.main import app
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
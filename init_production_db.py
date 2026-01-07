#!/usr/bin/env python3
"""
Production database initialization script
Run this on Railway to create tables
"""
import os
import sys
from sqlalchemy import create_engine, text

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import Base, engine
from app.models.identity import Identity, TargetApplication

def init_production_db():
    """Initialize production database"""
    try:
        print("Creating database tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully!")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection test passed!")
            
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    init_production_db()
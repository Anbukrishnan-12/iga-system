#!/usr/bin/env python3
"""
Run the IGA system locally for testing
"""
import uvicorn
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting IGA System locally...")
    print("API will be available at: http://localhost:8090")
    print("API Documentation: http://localhost:8090/docs")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8090,
        reload=True,
        log_level="info"
    )
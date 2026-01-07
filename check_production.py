#!/usr/bin/env python3
"""
Quick production server health check
"""
import requests
import json
import time

def check_production_server():
    base_url = "https://iga-system-production-c44b.up.railway.app"
    
    print("Checking production server status...")
    
    # 1. Health check
    try:
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("Health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"Health check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"Health check: ERROR - {str(e)}")
        return False
    
    # 2. API docs check
    try:
        print("\n2. Testing API docs...")
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("API docs: ACCESSIBLE")
        else:
            print(f"API docs: Status {response.status_code}")
    except Exception as e:
        print(f"API docs: ERROR - {str(e)}")
    
    # 3. Test identity creation
    try:
        print("\n3. Testing identity creation...")
        headers = {
            "accept": "application/json",
            "X-User-Role": "hr",
            "Content-Type": "application/json"
        }
        
        data = {
            "username": "testuser",
            "employee_id": "TEST001",
            "external_id": "string",
            "first_name": "Test",
            "last_name": "User",
            "middle_name": "string",
            "display_name": "Test User",
            "primary_email": "test@example.com",
            "secondary_email": "test2@example.com",
            "mobile_phone": "string",
            "work_phone": "string",
            "employment_type": "Employee",
            "employment_status": "ACTIVE",
            "hire_date": "2026-01-07",
            "termination_date": "2026-01-07",
            "last_working_day": "2026-01-07",
            "department": "string",
            "location": "string",
            "business_role": "developer",
            "entitlements": {}
        }
        
        response = requests.post(f"{base_url}/api/v1/identity/", 
                               headers=headers, json=data, timeout=15)
        
        if response.status_code == 201:
            print("Identity creation: SUCCESS!")
            result = response.json()
            print(f"   Created ID: {result.get('id')}")
            print(f"   Business Role: {result.get('business_role')}")
            print(f"   Entitlements: {len(result.get('entitlements', {}))}")
            return True
        else:
            print(f"Identity creation: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Identity creation: ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    print("Production Server Status Check")
    print("=" * 50)
    
    success = check_production_server()
    
    print("\n" + "=" * 50)
    if success:
        print("PRODUCTION SERVER IS READY!")
        print("All tests passed - Boss kita demo kaami!")
    else:
        print("Production server has issues")
        print("Use local server for demo: http://localhost:8090/docs")
    
    print("\nProduction URLs:")
    print("   Health: https://iga-system-production-c44b.up.railway.app/health")
    print("   API Docs: https://iga-system-production-c44b.up.railway.app/docs")
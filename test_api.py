#!/usr/bin/env python3
"""
Quick test script to debug the identity creation API
"""
import requests
import json

def test_create_identity():
    url = "http://localhost:8090/api/v1/identity/"
    
    headers = {
        "Content-Type": "application/json",
        "X-User-Role": "developer"
    }
    
    data = {
        "username": "anbu",
        "employee_id": "001",
        "external_id": "01",
        "first_name": "anbu",
        "last_name": "krishna",
        "middle_name": "string",
        "display_name": "krishna",
        "primary_email": "user@example.com",
        "secondary_email": "user@example.com",
        "mobile_phone": "string",
        "work_phone": "string",
        "employment_type": "Employee",
        "employment_status": "ACTIVE",
        "hire_date": "2026-01-07",
        "termination_date": "2026-01-07",
        "last_working_day": "2026-01-07",
        "department": "string",
        "location": "string",
        "business_role": "developer",  # Changed from "string" to "developer"
        "entitlements": {}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Identity created successfully!")
            return response.json()
        else:
            print("❌ Failed to create identity")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running on localhost:8090")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Testing Identity Creation API...")
    test_create_identity()
import requests
import json

# Test the exact same request you're making
url = "https://iga-system-production-c44b.up.railway.app/api/v1/identity/"

headers = {
    "accept": "application/json",
    "X-User-Role": "hr",
    "Content-Type": "application/json"
}

# Exact same data as your request
data = {
    "username": "anbu",
    "employee_id": "01",
    "external_id": "string",
    "first_name": "anbu",
    "last_name": "krishna",
    "middle_name": "string",
    "display_name": "anbu",
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

print("Testing API with correct data...")
print(f"URL: {url}")
print(f"Headers: {headers}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 201:
        print("✅ SUCCESS! Identity created!")
        result = response.json()
        print(f"Created ID: {result.get('id')}")
        print(f"Business Role: {result.get('business_role')}")
        print(f"Entitlements: {result.get('entitlements')}")
    else:
        print("❌ FAILED!")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
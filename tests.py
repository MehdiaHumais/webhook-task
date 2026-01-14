import requests
import json

BASE_URL = "http://127.0.0.1:8000/webhook"
SECRET = "my-secret-key"

def run_test(name, payload, signature, expected_status):
    print(f"--- Running Test: {name} ---")
    headers = {
        "Content-Type": "application/json",
        "X-Signature": signature
    }
    
    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == expected_status:
            print("✅ PASS\n")
        else:
            print(f"❌ FAIL (Expected {expected_status})\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

# 1. Test Success (Fixed: changed 'data' to 'payload')
run_test(
    name="Valid Request",
    payload={"event_id": "evt_001", "payload": "New User Signup"}, 
    signature=SECRET,
    expected_status=201
)

# 2. Test Idempotency (Fixed: changed 'data' to 'payload')
run_test(
    name="Idempotency Check (Duplicate)",
    payload={"event_id": "evt_001", "payload": "New User Signup"},
    signature=SECRET,
    expected_status=200
)

# 3. Test Security (Invalid Key)
run_test(
    name="Invalid Signature",
    payload={"event_id": "evt_002", "payload": "Hacking Attempt"},
    signature="wrong-key",
    expected_status=401
)
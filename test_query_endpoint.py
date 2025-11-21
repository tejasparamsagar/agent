"""
Test the /query endpoint with proper authentication.
"""
import requests
import os
import json

API_URL = "http://localhost:5000"
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "htcodehub-2024")

print("=" * 60)
print("Testing /query Endpoint")
print("=" * 60)
print()

# Test query
test_query = {
    "question": "What programs do you offer?",  # Note: /query uses "question", /api/chat uses "query"
    "dataset_name": "htcodehub"
}

print(f"Question: {test_query['question']}")
print(f"AUTH_TOKEN: {AUTH_TOKEN[:10]}...")
print()

try:
    response = requests.post(
        f"{API_URL}/query",
        json=test_query,
        headers={
            "X-API-Key": AUTH_TOKEN,
            "Content-Type": "application/json"
        },
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print()
    
    try:
        data = response.json()
        print("Response JSON:")
        print(json.dumps(data, indent=2))
    except:
        print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        print()
        print("[OK] Query successful!")
        if 'answer' in data:
            print(f"Answer: {data['answer'][:200]}...")
    else:
        print()
        print(f"[ERROR] Query failed with status {response.status_code}")
        
except Exception as e:
    print(f"[ERROR] Request failed: {e}")
    import traceback
    traceback.print_exc()


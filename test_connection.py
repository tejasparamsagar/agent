"""
Quick test script to verify RAG API is working and can be reached.
"""
import requests
import json

API_URL = "http://localhost:5000"

print("=" * 60)
print("Testing RAG API Connection")
print("=" * 60)

# Test 1: Health Check
print("\n1. Health Check...")
try:
    response = requests.get(f"{API_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Status: {data.get('status')}")
        print(f"   ✅ RAG Initialized: {data.get('rag_initialized')}")
        if not data.get('rag_initialized'):
            print("   ⚠️  RAG not initialized - check Flask console")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Cannot connect: {e}")
    print("   Make sure Flask is running: python app.py")
    exit(1)

# Test 2: Chat Endpoint
print("\n2. Chat Endpoint Test...")
try:
    response = requests.post(
        f"{API_URL}/api/chat",
        json={"query": "What programs do you offer?"},
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get('answer', '')
        print(f"   ✅ Status: 200")
        print(f"   ✅ Answer: {answer[:100]}...")
        
        if 'not sure' in answer.lower() or 'don\'t have' in answer.lower():
            print("\n   ⚠️  RAG doesn't have data yet")
            print("   Run: python ingest_data.py")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: CORS (simulate browser request)
print("\n3. CORS Test...")
try:
    response = requests.options(
        f"{API_URL}/api/chat",
        headers={"Origin": "http://localhost:8000"}
    )
    cors_header = response.headers.get("Access-Control-Allow-Origin")
    if cors_header:
        print(f"   ✅ CORS configured: {cors_header}")
    else:
        print("   ⚠️  CORS header not found")
except Exception as e:
    print(f"   ⚠️  CORS test failed: {e}")

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print("If all tests pass, your Laravel chat widget should work!")
print("\nNext: Update Laravel .env with RAG_API_URL=http://localhost:5000")


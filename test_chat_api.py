"""
Test the /api/chat endpoint to see what it returns.
"""
import requests
import json

API_URL = "http://localhost:5000"

test_queries = [
    "What programs do you offer?",
    "What is HT Code Hub?",
    "How can I contact you?",
]

print("=" * 60)
print("Testing RAG API Chat Endpoint")
print("=" * 60)
print()

for query in test_queries:
    print(f"Query: {query}")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{API_URL}/api/chat",
            json={"query": query},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', 'No answer field')
            print(f"Answer: {answer[:200]}..." if len(answer) > 200 else f"Answer: {answer}")
        else:
            print(f"Error: {response.text}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()

print("=" * 60)


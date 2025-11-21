"""
Example usage of the Flask RAG API
Run this after starting the Flask server
"""
import requests
import json

API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{API_URL}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_chat(query):
    """Test chat endpoint."""
    response = requests.post(
        f"{API_URL}/api/chat",
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )
    print(f"Query: {query}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("Flask RAG API Test")
    print("=" * 50)
    print()
    
    # Test health
    test_health()
    
    # Test chat
    test_chat("What is this document about?")
    test_chat("Summarize the main points.")


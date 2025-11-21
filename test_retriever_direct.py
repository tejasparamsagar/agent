"""
Test the retriever directly to see what error occurs.
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment
from dotenv import load_dotenv
load_dotenv()

from config import Config
from rag.vectorstore import VectorStore
from rag.retriever import Retriever

print("=" * 60)
print("Testing Retriever Directly")
print("=" * 60)
print()

# Check config
print(f"GROQ_API_KEY set: {bool(Config.GROQ_API_KEY)}")
if Config.GROQ_API_KEY:
    print(f"GROQ_API_KEY: {Config.GROQ_API_KEY[:10]}...{Config.GROQ_API_KEY[-4:]}")
print()

# Initialize components
print("Initializing VectorStore...")
try:
    vectorstore = VectorStore()
    print("[OK] VectorStore initialized")
except Exception as e:
    print(f"[ERROR] VectorStore failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("Initializing Retriever...")
try:
    retriever = Retriever()
    print("[OK] Retriever initialized")
except Exception as e:
    print(f"[ERROR] Retriever failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("Testing query...")
print()

test_query = "What programs do you offer?"

try:
    result = retriever.query("htcodehub", test_query)
    print(f"[OK] Query successful")
    print(f"Answer: {result.get('answer', 'No answer')[:200]}...")
    print(f"Sources: {len(result.get('sources', []))} sources found")
except Exception as e:
    print(f"[ERROR] Query failed: {e}")
    import traceback
    traceback.print_exc()


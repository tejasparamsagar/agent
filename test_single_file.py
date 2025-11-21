"""
Test loading a single file to debug the 500 error.
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app import load_document, chunk_documents

# Test with one file
test_file = Path("data/htcodehub_about.txt")

print("=" * 60)
print("Testing Single File Load")
print("=" * 60)
print()

if not test_file.exists():
    print(f"[ERROR] File not found: {test_file}")
    sys.exit(1)

print(f"Testing file: {test_file}")
print()

try:
    print("1. Loading document...")
    documents = load_document(test_file)
    print(f"   [OK] Loaded {len(documents)} document(s)")
    
    if documents:
        preview = documents[0].page_content[:100].replace('\n', ' ')
        print(f"   First document preview: {preview}...")
    
    print()
    print("2. Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"   [OK] Created {len(chunks)} chunks")
    
    if chunks:
        preview = chunks[0].page_content[:100].replace('\n', ' ')
        print(f"   First chunk preview: {preview}...")
    
    print()
    print("[SUCCESS] File processing works! The issue might be with file upload or vector store.")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("This is the actual error causing the 500 response.")


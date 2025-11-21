"""
Check if GROQ_API_KEY is set and dependencies are installed.
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("Groq Setup Check")
print("=" * 60)
print()

# Check GROQ_API_KEY
groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    print(f"[OK] GROQ_API_KEY is set: {groq_key[:10]}...{groq_key[-4:]}")
else:
    print("[ERROR] GROQ_API_KEY is NOT set")
    print()
    print("To set it:")
    print("  1. Get your key from: https://console.groq.com/keys")
    print("  2. Add to .env file: GROQ_API_KEY=your_key_here")
    print("  3. Or set in PowerShell: $env:GROQ_API_KEY='your_key_here'")
    print()

# Try to load from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print(f"[OK] Found GROQ_API_KEY in .env file: {groq_key[:10]}...{groq_key[-4:]}")
    else:
        print("[ERROR] GROQ_API_KEY not found in .env file")
except ImportError:
    print("[WARN] python-dotenv not installed (optional)")
except Exception as e:
    print(f"[WARN] Error loading .env: {e}")

print()

# Check dependencies
print("Checking dependencies...")
print()

dependencies = {
    "langchain-groq": "langchain_groq",
    "transformers": "transformers",
    "sentence-transformers": "sentence_transformers",
    "langchain-community": "langchain_community",
}

missing = []
for package_name, import_name in dependencies.items():
    try:
        __import__(import_name)
        print(f"[OK] {package_name} installed")
    except ImportError:
        print(f"[ERROR] {package_name} NOT installed")
        missing.append(package_name)

print()

if missing:
    print("[WARN] Missing dependencies. Install with:")
    print(f"   pip install {' '.join(missing)}")
    print()
else:
    print("[OK] All dependencies installed")
    print()

# Test imports
print("Testing imports...")
print()

try:
    from langchain_groq import ChatGroq
    print("[OK] ChatGroq import successful")
except Exception as e:
    print(f"[ERROR] ChatGroq import failed: {e}")

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("[OK] HuggingFaceEmbeddings import successful")
except Exception as e:
    print(f"[ERROR] HuggingFaceEmbeddings import failed: {e}")

print()
print("=" * 60)

if not groq_key:
    print()
    print("🔧 ACTION REQUIRED:")
    print("   1. Get your Groq API key from: https://console.groq.com/keys")
    print("   2. Add it to your .env file or set as environment variable")
    print("   3. Restart Flask app")
    sys.exit(1)

if missing:
    print()
    print("🔧 ACTION REQUIRED:")
    print(f"   Install missing packages: pip install {' '.join(missing)}")
    sys.exit(1)

print()
print("[OK] Setup looks good! Your Flask app should initialize correctly.")
print("   If it still fails, check Flask console for detailed error messages.")


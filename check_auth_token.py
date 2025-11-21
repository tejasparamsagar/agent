"""
Quick script to check what AUTH_TOKEN Flask is using.
"""
import os
import sys

# Try to load from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import config
sys.path.insert(0, os.path.dirname(__file__))
from config import Config

print("=" * 60)
print("AUTH_TOKEN Check")
print("=" * 60)
print()

# Check environment variable
env_token = os.getenv("AUTH_TOKEN")
if env_token:
    print(f"✅ AUTH_TOKEN from environment: {env_token}")
else:
    print("⚠️  AUTH_TOKEN not set in environment variables")

print()

# Check config (what Flask is actually using)
config_token = Config.AUTH_TOKEN
print(f"📋 AUTH_TOKEN Flask is using: {config_token}")
print()

if config_token == "default-token-change-in-production":
    print("⚠️  Using default token!")
    print("   Set a custom token for security:")
    print()
    print("   PowerShell:")
    print('     $env:AUTH_TOKEN="your-secure-token-here"')
    print()
    print("   Or create .env file with:")
    print("     AUTH_TOKEN=your-secure-token-here")
else:
    print("✅ Using custom token")

print()
print("=" * 60)
print("To use this token in ingestion script:")
print("=" * 60)
print(f'  $env:AUTH_TOKEN="{config_token}"')
print("  python ingest_data.py")


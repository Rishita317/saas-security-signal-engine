"""
Test OpenAI API Setup
Quick verification that OpenAI API key is working correctly
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment
load_dotenv()

print("=" * 70)
print("🧪 Testing OpenAI API Setup")
print("=" * 70 + "\n")

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found in .env file")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...{api_key[-4:]}")
print(f"   Key length: {len(api_key)} characters")

# Test OpenAI connection
print("\n🔍 Testing OpenAI API connection...")
try:
    client = OpenAI(api_key=api_key)

    # Simple test request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'API working' if you can read this."}
        ],
        max_tokens=10,
        temperature=0
    )

    result = response.choices[0].message.content
    print(f"✅ OpenAI API Response: {result}")
    print(f"   Model: {response.model}")
    print(f"   Tokens used: {response.usage.total_tokens}")

    print("\n" + "=" * 70)
    print("✅ OpenAI API Setup VERIFIED!")
    print("=" * 70)

except Exception as e:
    print(f"\n❌ OpenAI API Error: {e}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. API key not activated")
    print("3. No credits/quota remaining")
    print("4. Network connection issue")
    exit(1)

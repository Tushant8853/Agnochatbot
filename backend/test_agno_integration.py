#!/usr/bin/env python3
"""
Test script to verify Agno integration works alongside existing system.
This script tests both the existing system and the new Agno endpoints.
"""

import asyncio
import requests
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "agno_test_user",
    "email": "agno_test@example.com",
    "password": "testpass123"
}

async def test_existing_system():
    """Test that the existing system still works."""
    print("🧪 Testing existing system...")
    
    # Test signup
    signup_response = requests.post(
        f"{BASE_URL}/auth/signup",
        json=TEST_USER
    )
    
    if signup_response.status_code == 200:
        print("✅ Signup works")
        token_data = signup_response.json()
        token = token_data["access_token"]
    else:
        print(f"❌ Signup failed: {signup_response.text}")
        return None
    
    # Test login
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
    )
    
    if login_response.status_code == 200:
        print("✅ Login works")
    else:
        print(f"❌ Login failed: {login_response.text}")
        return None
    
    # Test existing chat endpoint
    chat_response = requests.post(
        f"{BASE_URL}/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "message": "Hello, this is a test of the existing system",
            "use_memory": True
        }
    )
    
    if chat_response.status_code == 200:
        print("✅ Existing chat endpoint works")
        chat_data = chat_response.json()
        print(f"   Response: {chat_data['message'][:100]}...")
    else:
        print(f"❌ Existing chat failed: {chat_response.text}")
        return None
    
    return token

async def test_agno_system(token):
    """Test the new Agno system."""
    print("\n🤖 Testing Agno system...")
    
    # Test Agno chat endpoint
    agno_chat_response = requests.post(
        f"{BASE_URL}/agno/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "message": "Hello, this is a test of the Agno system. Can you tell me about yourself?",
            "use_memory": True
        }
    )
    
    if agno_chat_response.status_code == 200:
        print("✅ Agno chat endpoint works")
        agno_data = agno_chat_response.json()
        print(f"   Success: {agno_data['success']}")
        if agno_data.get('message'):
            print(f"   Response: {agno_data['message'][:100]}...")
        if agno_data.get('agno_metadata'):
            print(f"   Metadata: {agno_data['agno_metadata']}")
    else:
        print(f"❌ Agno chat failed: {agno_chat_response.text}")
        return False
    
    # Test Agno memories endpoint
    memories_response = requests.get(
        f"{BASE_URL}/agno/memories",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if memories_response.status_code == 200:
        print("✅ Agno memories endpoint works")
        memories_data = memories_response.json()
        print(f"   Memory count: {memories_data.get('count', 0)}")
    else:
        print(f"❌ Agno memories failed: {memories_response.text}")
        return False
    
    # Test adding Agno memory
    add_memory_response = requests.post(
        f"{BASE_URL}/agno/memories",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "Test user likes to test new AI systems",
            "memory_type": "preference"
        }
    )
    
    if add_memory_response.status_code == 200:
        print("✅ Agno add memory endpoint works")
        memory_data = add_memory_response.json()
        print(f"   Success: {memory_data['success']}")
    else:
        print(f"❌ Agno add memory failed: {add_memory_response.text}")
        return False
    
    return True

async def main():
    """Run all tests."""
    print("🚀 Starting Agno Integration Test")
    print("=" * 50)
    
    # Test existing system
    token = await test_existing_system()
    if not token:
        print("❌ Existing system test failed. Stopping.")
        return
    
    # Test Agno system
    agno_success = await test_agno_system(token)
    
    print("\n" + "=" * 50)
    if agno_success:
        print("🎉 All tests passed! Agno integration successful.")
        print("\n📋 Summary:")
        print("   ✅ Existing login/signup still works")
        print("   ✅ Existing chat endpoint still works")
        print("   ✅ New Agno chat endpoint works")
        print("   ✅ New Agno memories endpoints work")
        print("\n🔗 Available endpoints:")
        print("   - POST /chat (existing)")
        print("   - POST /agno/chat (new)")
        print("   - GET /agno/memories (new)")
        print("   - POST /agno/memories (new)")
        print("   - DELETE /agno/agent (new)")
    else:
        print("❌ Some Agno tests failed. Check the logs above.")

if __name__ == "__main__":
    asyncio.run(main()) 
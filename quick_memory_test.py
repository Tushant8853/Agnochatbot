#!/usr/bin/env python3
"""
Quick test to verify memory isolation fixes are working.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_memory_isolation():
    print("🧪 Testing Memory Isolation Fixes...")
    print("=" * 50)
    
    # Test 1: Sign up two users
    print("\n1. Creating two test users...")
    
    user1_data = {
        "email": f"testuser1_{int(time.time())}@example.com",
        "password": "testpass123",
        "name": "Test User 1"
    }
    
    user2_data = {
        "email": f"testuser2_{int(time.time())}@example.com", 
        "password": "testpass123",
        "name": "Test User 2"
    }
    
    # Sign up user 1
    response = requests.post(f"{BASE_URL}/auth/signup", json=user1_data)
    if response.status_code == 200:
        user1_token = response.json()["access_token"]
        # Get user ID from auth/me endpoint
        headers1 = {"Authorization": f"Bearer {user1_token}"}
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers1)
        if me_response.status_code == 200:
            user1_id = me_response.json()["user_id"]
            print(f"✅ User 1 created: {user1_id}")
        else:
            print(f"❌ Failed to get user 1 ID: {me_response.text}")
            return
    else:
        print(f"❌ Failed to create user 1: {response.text}")
        return
    
    # Sign up user 2
    response = requests.post(f"{BASE_URL}/auth/signup", json=user2_data)
    if response.status_code == 200:
        user2_token = response.json()["access_token"]
        # Get user ID from auth/me endpoint
        headers2 = {"Authorization": f"Bearer {user2_token}"}
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers2)
        if me_response.status_code == 200:
            user2_id = me_response.json()["user_id"]
            print(f"✅ User 2 created: {user2_id}")
        else:
            print(f"❌ Failed to get user 2 ID: {me_response.text}")
            return
    else:
        print(f"❌ Failed to create user 2: {response.text}")
        return
    
    # Test 2: User 1 chats and stores personal info
    print(f"\n2. User 1 ({user1_id}) storing personal information...")
    
    chat_messages = [
        "My name is Alice Johnson and I live in New York.",
        "I work as a software engineer at Google.",
        "My favorite color is blue and I love pizza."
    ]
    
    for message in chat_messages:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": message, "user_id": user1_id, "session_id": "test_session_1"},
            headers=headers1
        )
        if response.status_code == 200:
            print(f"✅ User 1 chat: {message[:30]}...")
        else:
            print(f"❌ User 1 chat failed: {response.text}")
    
    # Test 3: User 2 chats and stores different personal info
    print(f"\n3. User 2 ({user2_id}) storing different personal information...")
    
    chat_messages2 = [
        "My name is Bob Smith and I live in Los Angeles.",
        "I work as a teacher at UCLA.",
        "My favorite color is red and I love sushi."
    ]
    
    for message in chat_messages2:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": message, "user_id": user2_id, "session_id": "test_session_2"},
            headers=headers2
        )
        if response.status_code == 200:
            print(f"✅ User 2 chat: {message[:30]}...")
        else:
            print(f"❌ User 2 chat failed: {response.text}")
    
    # Test 4: User 1 searches for their own information
    print(f"\n4. User 1 searching for their own information...")
    
    search_queries = ["Alice", "New York", "Google", "blue", "pizza"]
    
    for query in search_queries:
        response = requests.post(
            f"{BASE_URL}/memory/search?user_id={user1_id}&query={query}",
            headers=headers1
        )
        if response.status_code == 200:
            result = response.json()["results"]
            print(f"✅ User 1 search '{query}': {result[:100]}...")
        else:
            print(f"❌ User 1 search failed: {response.text}")
    
    # Test 5: User 2 searches for their own information
    print(f"\n5. User 2 searching for their own information...")
    
    search_queries2 = ["Bob", "Los Angeles", "UCLA", "red", "sushi"]
    
    for query in search_queries2:
        response = requests.post(
            f"{BASE_URL}/memory/search?user_id={user2_id}&query={query}",
            headers=headers2
        )
        if response.status_code == 200:
            result = response.json()["results"]
            print(f"✅ User 2 search '{query}': {result[:100]}...")
        else:
            print(f"❌ User 2 search failed: {response.text}")
    
    # Test 6: Cross-contamination test - User 1 searches for User 2's info
    print(f"\n6. Testing cross-contamination - User 1 searching for User 2's info...")
    
    cross_queries = ["Bob", "Los Angeles", "UCLA", "red", "sushi"]
    
    for query in cross_queries:
        response = requests.post(
            f"{BASE_URL}/memory/search?user_id={user1_id}&query={query}",
            headers=headers1
        )
        if response.status_code == 200:
            result = response.json()["results"]
            if "Bob" in result or "Los Angeles" in result or "UCLA" in result:
                print(f"❌ CROSS-CONTAMINATION DETECTED! User 1 found User 2's info for '{query}': {result[:100]}...")
            else:
                print(f"✅ User 1 correctly did NOT find User 2's info for '{query}': {result[:100]}...")
        else:
            print(f"❌ Cross-contamination test failed: {response.text}")
    
    # Test 7: Cross-contamination test - User 2 searches for User 1's info
    print(f"\n7. Testing cross-contamination - User 2 searching for User 1's info...")
    
    cross_queries2 = ["Alice", "New York", "Google", "blue", "pizza"]
    
    for query in cross_queries2:
        response = requests.post(
            f"{BASE_URL}/memory/search?user_id={user2_id}&query={query}",
            headers=headers2
        )
        if response.status_code == 200:
            result = response.json()["results"]
            if "Alice" in result or "New York" in result or "Google" in result:
                print(f"❌ CROSS-CONTAMINATION DETECTED! User 2 found User 1's info for '{query}': {result[:100]}...")
            else:
                print(f"✅ User 2 correctly did NOT find User 1's info for '{query}': {result[:100]}...")
        else:
            print(f"❌ Cross-contamination test failed: {response.text}")
    
    print(f"\n" + "=" * 50)
    print("🎯 Memory Isolation Test Complete!")
    print("If you see 'CROSS-CONTAMINATION DETECTED' messages above, the fixes are not working.")
    print("If you only see ✅ messages for cross-contamination tests, the fixes are working!")

if __name__ == "__main__":
    test_memory_isolation() 
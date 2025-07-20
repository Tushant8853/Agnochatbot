#!/usr/bin/env python3
"""
Simple Memory Isolation Test for AgnoChat Bot
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"

def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def test_memory_isolation():
    """Test memory isolation between two users"""
    
    log("🚀 Starting Simple Memory Isolation Test")
    
    # Create User 1
    log("Creating User 1...")
    user1_data = {
        "email": "alice_test@example.com",
        "password": "testpass123",
        "first_name": "Alice",
        "last_name": "Johnson"
    }
    
    response = requests.post(f"{BASE_URL}{API_PREFIX}/auth/signup", json=user1_data)
    if response.status_code != 200:
        log(f"❌ Failed to create User 1: {response.text}")
        return
    
    user1_token = response.json()["access_token"]
    log("✅ User 1 created")
    
    # Get User 1 ID
    headers = {"Authorization": f"Bearer {user1_token}"}
    response = requests.get(f"{BASE_URL}{API_PREFIX}/auth/me", headers=headers)
    user1_id = response.json()["user_id"]
    log(f"User 1 ID: {user1_id}")
    
    # Create User 2
    log("Creating User 2...")
    user2_data = {
        "email": "bob_test@example.com",
        "password": "testpass456",
        "first_name": "Bob",
        "last_name": "Smith"
    }
    
    response = requests.post(f"{BASE_URL}{API_PREFIX}/auth/signup", json=user2_data)
    if response.status_code != 200:
        log(f"❌ Failed to create User 2: {response.text}")
        return
    
    user2_token = response.json()["access_token"]
    log("✅ User 2 created")
    
    # Get User 2 ID
    headers = {"Authorization": f"Bearer {user2_token}"}
    response = requests.get(f"{BASE_URL}{API_PREFIX}/auth/me", headers=headers)
    user2_id = response.json()["user_id"]
    log(f"User 2 ID: {user2_id}")
    
    # Send personal information to User 1
    log("Sending personal info to User 1...")
    chat_data = {
        "message": "Hello! My name is Alice Johnson. I live in Seattle. I work as a data scientist. I love hiking and coffee.",
        "user_id": user1_id,
        "session_id": "test_session_1"
    }
    
    headers = {"Authorization": f"Bearer {user1_token}"}
    response = requests.post(f"{BASE_URL}{API_PREFIX}/chat", json=chat_data, headers=headers)
    if response.status_code == 200:
        log("✅ User 1 chat message sent")
    else:
        log(f"❌ Failed to send User 1 chat: {response.text}")
    
    # Send personal information to User 2
    log("Sending personal info to User 2...")
    chat_data = {
        "message": "Hi! My name is Bob Smith. I live in Austin. I work as a software engineer. I love BBQ and football.",
        "user_id": user2_id,
        "session_id": "test_session_2"
    }
    
    headers = {"Authorization": f"Bearer {user2_token}"}
    response = requests.post(f"{BASE_URL}{API_PREFIX}/chat", json=chat_data, headers=headers)
    if response.status_code == 200:
        log("✅ User 2 chat message sent")
    else:
        log(f"❌ Failed to send User 2 chat: {response.text}")
    
    # Wait for memory processing
    log("Waiting for memory processing...")
    time.sleep(5)
    
    # Debug memory for both users
    log("Debugging User 1 memory...")
    response = requests.get(f"{BASE_URL}{API_PREFIX}/memory/debug/{user1_id}", headers={"Authorization": f"Bearer {user1_token}"})
    if response.status_code == 200:
        debug1 = response.json()
        log("✅ User 1 memory debug retrieved")
    else:
        log(f"❌ Failed to debug User 1 memory: {response.text}")
        debug1 = {}
    
    log("Debugging User 2 memory...")
    response = requests.get(f"{BASE_URL}{API_PREFIX}/memory/debug/{user2_id}", headers={"Authorization": f"Bearer {user2_token}"})
    if response.status_code == 200:
        debug2 = response.json()
        log("✅ User 2 memory debug retrieved")
    else:
        log(f"❌ Failed to debug User 2 memory: {response.text}")
        debug2 = {}
    
    # Test search functionality
    log("Testing User 1 search for Alice...")
    response = requests.post(f"{BASE_URL}{API_PREFIX}/memory/search?user_id={user1_id}&query=Alice%20Johnson", headers={"Authorization": f"Bearer {user1_token}"})
    if response.status_code == 200:
        search1_alice = response.json()
        log("✅ User 1 search for Alice completed")
    else:
        log(f"❌ Failed User 1 search for Alice: {response.text}")
        search1_alice = {}
    
    log("Testing User 1 search for Bob...")
    response = requests.post(f"{BASE_URL}{API_PREFIX}/memory/search?user_id={user1_id}&query=Bob%20Smith", headers={"Authorization": f"Bearer {user1_token}"})
    if response.status_code == 200:
        search1_bob = response.json()
        log("✅ User 1 search for Bob completed")
    else:
        log(f"❌ Failed User 1 search for Bob: {response.text}")
        search1_bob = {}
    
    log("Testing User 2 search for Alice...")
    response = requests.post(f"{BASE_URL}{API_PREFIX}/memory/search?user_id={user2_id}&query=Alice%20Johnson", headers={"Authorization": f"Bearer {user2_token}"})
    if response.status_code == 200:
        search2_alice = response.json()
        log("✅ User 2 search for Alice completed")
    else:
        log(f"❌ Failed User 2 search for Alice: {response.text}")
        search2_alice = {}
    
    log("Testing User 2 search for Bob...")
    response = requests.post(f"{BASE_URL}{API_PREFIX}/memory/search?user_id={user2_id}&query=Bob%20Smith", headers={"Authorization": f"Bearer {user2_token}"})
    if response.status_code == 200:
        search2_bob = response.json()
        log("✅ User 2 search for Bob completed")
    else:
        log(f"❌ Failed User 2 search for Bob: {response.text}")
        search2_bob = {}
    
    # Analyze results
    log("\n📊 ANALYZING RESULTS:")
    log("=" * 50)
    
    # Check for memory contamination
    contamination_found = False
    
    if debug1 and "debug_result" in debug1:
        debug_text = debug1["debug_result"].lower()
        if "bob smith" in debug_text or "austin" in debug_text or "bbq" in debug_text:
            log("❌ CRITICAL: User 1's memory contains Bob's information!")
            contamination_found = True
        else:
            log("✅ User 1's memory appears isolated")
    
    if debug2 and "debug_result" in debug2:
        debug_text = debug2["debug_result"].lower()
        if "alice johnson" in debug_text or "seattle" in debug_text or "hiking" in debug_text:
            log("❌ CRITICAL: User 2's memory contains Alice's information!")
            contamination_found = True
        else:
            log("✅ User 2's memory appears isolated")
    
    # Check search results
    if search1_bob and "results" in search1_bob:
        if "bob smith" in search1_bob["results"].lower():
            log("❌ CRITICAL: User 1 can search and find Bob's information!")
            contamination_found = True
        else:
            log("✅ User 1 search is properly isolated")
    
    if search2_alice and "results" in search2_alice:
        if "alice johnson" in search2_alice["results"].lower():
            log("❌ CRITICAL: User 2 can search and find Alice's information!")
            contamination_found = True
        else:
            log("✅ User 2 search is properly isolated")
    
    if not contamination_found:
        log("🎉 SUCCESS: Memory isolation appears to be working correctly!")
    else:
        log("🚨 FAILURE: Memory isolation issues detected!")
    
    # Print detailed results
    log("\n📋 DETAILED RESULTS:")
    log("=" * 50)
    
    if debug1 and "debug_result" in debug1:
        log(f"User 1 Debug (first 300 chars): {debug1['debug_result'][:300]}...")
    
    if debug2 and "debug_result" in debug2:
        log(f"User 2 Debug (first 300 chars): {debug2['debug_result'][:300]}...")
    
    if search1_alice and "results" in search1_alice:
        log(f"User 1 Search Alice: {search1_alice['results'][:150]}...")
    
    if search1_bob and "results" in search1_bob:
        log(f"User 1 Search Bob: {search1_bob['results'][:150]}...")
    
    if search2_alice and "results" in search2_alice:
        log(f"User 2 Search Alice: {search2_alice['results'][:150]}...")
    
    if search2_bob and "results" in search2_bob:
        log(f"User 2 Search Bob: {search2_bob['results'][:150]}...")

if __name__ == "__main__":
    test_memory_isolation() 
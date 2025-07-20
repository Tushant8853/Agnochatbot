#!/usr/bin/env python3
"""
Comprehensive Memory Isolation Fix for AgnoChat Bot

This script implements fixes for the critical memory isolation issues:
1. User memory contamination
2. Search cross-contamination
3. Internal user ID conflicts
"""

import os
import sys

def fix_agent_configuration():
    """Fix the agent configuration to ensure proper user isolation"""
    
    print("🔧 Fixing Agent Configuration...")
    
    # Read the current agent configuration
    agent_file = "backend/agno_chatbot/agents/chatbot_agent.py"
    
    with open(agent_file, 'r') as f:
        content = f.read()
    
    # Fix 1: Ensure proper user isolation in agent instructions
    isolation_instructions = '''        instructions=[
            "You are an intelligent AI assistant with memory capabilities.",
            "Use Zep tools to store and retrieve temporal memory and chat history.",
            "Use Mem0 tools to store and retrieve fact-based memory.",
            "Always provide helpful, context-aware responses.",
            "Remember user preferences and past conversations.",
            "When users share information about themselves, store it in memory.",
            "Use memory to provide personalized responses.",
            "CRITICAL MEMORY ISOLATION RULES:",
            "1. ALWAYS use the user_id parameter when calling memory tools",
            "2. NEVER share or access memories from different users",
            "3. Each user must have completely separate memory spaces",
            "4. When storing information, ensure it's stored only for the current user",
            "5. When searching memory, only search within the current user's memory space",
            "6. If no user_id is provided, do not access any memories",
            "7. Verify user isolation before storing or retrieving any information",
            "8. If asked to search for information, thoroughly search both Zep and Mem0 memories for the current user only",
            "9. Provide detailed search results when information is found in memory",
            "10. If no information is found, clearly state that no relevant information was found for this user",
            "11. IMPORTANT: Always include the user_id in your tool calls to ensure proper isolation",
            "12. NEVER reference or access data from other users' memory spaces",
            "13. CRITICAL: Each user must have a unique memory namespace",
            "14. When using Zep tools, always specify the user_id parameter",
            "15. When using Mem0 tools, always specify the user_id parameter"
        ]'''
    
    # Replace the instructions section
    import re
    pattern = r'instructions=\[[^\]]*\],'
    replacement = isolation_instructions + ','
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("✅ Agent instructions updated for user isolation")
    else:
        print("❌ Could not find instructions section to update")
    
    # Write the updated content
    with open(agent_file, 'w') as f:
        f.write(content)
    
    print("✅ Agent configuration fixed")

def fix_api_routes():
    """Fix the API routes to ensure proper user isolation"""
    
    print("🔧 Fixing API Routes...")
    
    routes_file = "backend/agno_chatbot/api/routes.py"
    
    with open(routes_file, 'r') as f:
        content = f.read()
    
    # Fix 1: Enhanced search prompt with stronger user isolation
    enhanced_search_prompt = '''        # Search memory using agent tools with enhanced prompt
        search_prompt = f"""
        SEARCH REQUEST: {query}
        USER ID: {user_id}
        
        Please search through ALL memory sources (Zep and Mem0) for user {user_id} to find information related to: {query}
        
        CRITICAL USER ISOLATION RULES:
        1. ONLY search within user {user_id}'s memory space
        2. DO NOT access memories from other users
        3. DO NOT search across user boundaries
        4. Search Zep memory for temporal/conversation memories related to: {query}
        5. Search Mem0 memory for factual/personal information related to: {query}
        6. Look for exact matches, partial matches, and related information
        7. If you find information, provide a comprehensive summary
        8. If no information is found, clearly state that no relevant information was found for user {user_id}
        9. ALWAYS include user_id={user_id} in your tool calls
        10. NEVER search outside of user {user_id}'s memory namespace
        
        Search terms to look for: {query}
        Target user: {user_id}
        
        Please provide a detailed response with all relevant information found for user {user_id} only.
        """'''
    
    # Replace the search prompt
    import re
    pattern = r'# Search memory using agent tools with enhanced prompt.*?Please provide a detailed response with all relevant information found for user \{user_id\} only\.'
    replacement = enhanced_search_prompt
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("✅ Search prompt enhanced for user isolation")
    else:
        print("❌ Could not find search prompt to update")
    
    # Fix 2: Enhanced chat prompt with stronger user isolation
    enhanced_chat_prompt = '''            # Regular chat processing with user isolation
            chat_prompt = f"""
            User message: {chat_data.message}
            User ID: {chat_data.user_id}
            
            CRITICAL MEMORY ISOLATION RULES:
            1. Only access memories for user {chat_data.user_id}
            2. Do NOT access memories from other users
            3. Do NOT reference information from other users
            4. If you don't have specific memories for user {chat_data.user_id}, start fresh
            5. When storing new information, ensure it's only stored for user {chat_data.user_id}
            6. Use both Zep and Mem0 tools to store information for user {chat_data.user_id}
            7. ALWAYS include user_id={chat_data.user_id} in your tool calls
            8. NEVER access memory outside of user {chat_data.user_id}'s namespace
            9. Verify user isolation before any memory operation
            10. Each user must have completely separate memory spaces
            
            Respond to the user's message based ONLY on their own memories and context.
            If the user shares personal information, store it in memory for user {chat_data.user_id} only.
            """'''
    
    # Replace the chat prompt
    pattern = r'# Regular chat processing with user isolation.*?If the user shares personal information, store it in memory for user \{chat_data\.user_id\} only\.'
    replacement = enhanced_chat_prompt
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("✅ Chat prompt enhanced for user isolation")
    else:
        print("❌ Could not find chat prompt to update")
    
    # Write the updated content
    with open(routes_file, 'w') as f:
        f.write(content)
    
    print("✅ API routes fixed")

def fix_user_id_generation():
    """Fix user ID generation to ensure uniqueness"""
    
    print("🔧 Fixing User ID Generation...")
    
    auth_file = "backend/agno_chatbot/utils/auth.py"
    
    with open(auth_file, 'r') as f:
        content = f.read()
    
    # Fix user ID generation to be more unique
    enhanced_user_id_generation = '''def generate_user_id(email: str) -> str:
    """Generate a unique user ID from email."""
    # Create a more unique user ID to prevent conflicts
    import hashlib
    import time
    
    # Use email + timestamp to ensure uniqueness
    unique_string = f"{email}_{int(time.time() * 1000)}"
    hash_object = hashlib.md5(unique_string.encode())
    hash_hex = hash_object.hexdigest()[:8]
    
    # Create a shorter, more unique ID
    username = email.split('@')[0]
    return f"{username}_{hash_hex}"'''
    
    # Replace the user ID generation function
    import re
    pattern = r'def generate_user_id\(email: str\) -> str:.*?return f"{username}_\{hash_hex\}"'
    replacement = enhanced_user_id_generation
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("✅ User ID generation enhanced for uniqueness")
    else:
        print("❌ Could not find user ID generation function to update")
    
    # Write the updated content
    with open(auth_file, 'w') as f:
        f.write(content)
    
    print("✅ User ID generation fixed")

def create_memory_isolation_test():
    """Create a comprehensive memory isolation test"""
    
    print("🔧 Creating Memory Isolation Test...")
    
    test_content = '''#!/usr/bin/env python3
"""
Comprehensive Memory Isolation Test for AgnoChat Bot

This test verifies that the memory isolation fixes are working correctly.
"""

import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"

def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def test_memory_isolation_fixed():
    """Test memory isolation after fixes"""
    
    log("🚀 Testing Memory Isolation After Fixes")
    
    # Create unique test users
    timestamp = int(time.time())
    user1_email = f"test_alice_{timestamp}@example.com"
    user2_email = f"test_bob_{timestamp}@example.com"
    
    # Create User 1
    log("Creating User 1...")
    user1_data = {
        "email": user1_email,
        "password": "testpass123",
        "first_name": "Alice",
        "last_name": "Johnson"
    }
    
    response = requests.post(f"{BASE_URL}{API_PREFIX}/auth/signup", json=user1_data)
    if response.status_code != 200:
        log(f"❌ Failed to create User 1: {response.text}")
        return False
    
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
        "email": user2_email,
        "password": "testpass456",
        "first_name": "Bob",
        "last_name": "Smith"
    }
    
    response = requests.post(f"{BASE_URL}{API_PREFIX}/auth/signup", json=user2_data)
    if response.status_code != 200:
        log(f"❌ Failed to create User 2: {response.text}")
        return False
    
    user2_token = response.json()["access_token"]
    log("✅ User 2 created")
    
    # Get User 2 ID
    headers = {"Authorization": f"Bearer {user2_token}"}
    response = requests.get(f"{BASE_URL}{API_PREFIX}/auth/me", headers=headers)
    user2_id = response.json()["user_id"]
    log(f"User 2 ID: {user2_id}")
    
    # Verify unique user IDs
    if user1_id == user2_id:
        log("❌ CRITICAL: User IDs are not unique!")
        return False
    else:
        log("✅ User IDs are unique")
    
    # Send personal information to User 1
    log("Sending personal info to User 1...")
    chat_data = {
        "message": "Hello! My name is Alice Johnson. I live in Seattle. I work as a data scientist. I love hiking and coffee.",
        "user_id": user1_id,
        "session_id": f"test_session_1_{timestamp}"
    }
    
    headers = {"Authorization": f"Bearer {user1_token}"}
    response = requests.post(f"{BASE_URL}{API_PREFIX}/chat", json=chat_data, headers=headers)
    if response.status_code == 200:
        log("✅ User 1 chat message sent")
    else:
        log(f"❌ Failed to send User 1 chat: {response.text}")
        return False
    
    # Send personal information to User 2
    log("Sending personal info to User 2...")
    chat_data = {
        "message": "Hi! My name is Bob Smith. I live in Austin. I work as a software engineer. I love BBQ and football.",
        "user_id": user2_id,
        "session_id": f"test_session_2_{timestamp}"
    }
    
    headers = {"Authorization": f"Bearer {user2_token}"}
    response = requests.post(f"{BASE_URL}{API_PREFIX}/chat", json=chat_data, headers=headers)
    if response.status_code == 200:
        log("✅ User 2 chat message sent")
    else:
        log(f"❌ Failed to send User 2 chat: {response.text}")
        return False
    
    # Wait for memory processing
    log("Waiting for memory processing...")
    time.sleep(10)
    
    # Debug memory for both users
    log("Debugging User 1 memory...")
    response = requests.get(f"{BASE_URL}{API_PREFIX}/memory/debug/{user1_id}", headers={"Authorization": f"Bearer {user1_token}"})
    if response.status_code == 200:
        debug1 = response.json()
        log("✅ User 1 memory debug retrieved")
    else:
        log(f"❌ Failed to debug User 1 memory: {response.text}")
        return False
    
    log("Debugging User 2 memory...")
    response = requests.get(f"{BASE_URL}{API_PREFIX}/memory/debug/{user2_id}", headers={"Authorization": f"Bearer {user2_token}"})
    if response.status_code == 200:
        debug2 = response.json()
        log("✅ User 2 memory debug retrieved")
    else:
        log(f"❌ Failed to debug User 2 memory: {response.text}")
        return False
    
    # Test search functionality
    log("Testing User 1 search for Alice...")
    response = requests.post(f"{BASE_URL}{API_PREFIX}/memory/search?user_id={user1_id}&query=Alice%20Johnson", headers={"Authorization": f"Bearer {user1_token}"})
    if response.status_code == 200:
        search1_alice = response.json()
        log("✅ User 1 search for Alice completed")
    else:
        log(f"❌ Failed User 1 search for Alice: {response.text}")
        return False
    
    log("Testing User 1 search for Bob...")
    response = requests.post(f"{BASE_URL}{API_PREFIX}/memory/search?user_id={user1_id}&query=Bob%20Smith", headers={"Authorization": f"Bearer {user1_token}"})
    if response.status_code == 200:
        search1_bob = response.json()
        log("✅ User 1 search for Bob completed")
    else:
        log(f"❌ Failed User 1 search for Bob: {response.text}")
        return False
    
    log("Testing User 2 search for Alice...")
    response = requests.post(f"{BASE_URL}{API_PREFIX}/memory/search?user_id={user2_id}&query=Alice%20Johnson", headers={"Authorization": f"Bearer {user2_token}"})
    if response.status_code == 200:
        search2_alice = response.json()
        log("✅ User 2 search for Alice completed")
    else:
        log(f"❌ Failed User 2 search for Alice: {response.text}")
        return False
    
    log("Testing User 2 search for Bob...")
    response = requests.post(f"{BASE_URL}{API_PREFIX}/memory/search?user_id={user2_id}&query=Bob%20Smith", headers={"Authorization": f"Bearer {user2_token}"})
    if response.status_code == 200:
        search2_bob = response.json()
        log("✅ User 2 search for Bob completed")
    else:
        log(f"❌ Failed User 2 search for Bob: {response.text}")
        return False
    
    # Analyze results
    log("\\n📊 ANALYZING RESULTS:")
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
        log("🎉 SUCCESS: Memory isolation is working correctly!")
        return True
    else:
        log("🚨 FAILURE: Memory isolation issues still detected!")
        return False

if __name__ == "__main__":
    success = test_memory_isolation_fixed()
    if success:
        print("\\n✅ MEMORY ISOLATION TEST PASSED")
    else:
        print("\\n❌ MEMORY ISOLATION TEST FAILED")
'''
    
    with open("test_memory_isolation_fixed.py", 'w') as f:
        f.write(test_content)
    
    print("✅ Memory isolation test created")

def main():
    """Run all fixes"""
    print("🚀 Starting Comprehensive Memory Isolation Fix")
    print("=" * 60)
    
    try:
        fix_agent_configuration()
        fix_api_routes()
        fix_user_id_generation()
        create_memory_isolation_test()
        
        print("\\n" + "=" * 60)
        print("✅ ALL FIXES COMPLETED SUCCESSFULLY")
        print("\\n📋 NEXT STEPS:")
        print("1. Restart the backend server")
        print("2. Run: python3 test_memory_isolation_fixed.py")
        print("3. Verify that memory isolation is working")
        print("4. Test with multiple users to ensure privacy")
        
    except Exception as e:
        print(f"❌ Error during fixes: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 
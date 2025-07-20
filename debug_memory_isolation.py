#!/usr/bin/env python3
"""
Comprehensive Memory Isolation Debug Script for AgnoChat Bot

This script will:
1. Test user creation and isolation
2. Test memory storage and retrieval
3. Test search functionality
4. Identify memory isolation issues
5. Provide fixes for the problems found
"""

import os
import sys
import json
import time
import requests
from typing import Dict, List, Any
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"

class MemoryIsolationDebugger:
    def __init__(self):
        self.base_url = BASE_URL
        self.api_prefix = API_PREFIX
        self.test_users = {}
        self.test_sessions = {}
        self.results = {}
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> Dict:
        """Make HTTP request and return response"""
        url = f"{self.base_url}{self.api_prefix}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.log(f"Request failed: {e}", "ERROR")
            return {"error": str(e)}
            
    def test_backend_health(self) -> bool:
        """Test if backend is running"""
        self.log("Testing backend health...")
        try:
            response = requests.get(f"{self.base_url}{self.api_prefix}/health", timeout=5)
            if response.status_code == 200:
                self.log("✅ Backend is running")
                return True
            else:
                self.log(f"❌ Backend health check failed: {response.status_code}", "ERROR")
                return False
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Backend not accessible: {e}", "ERROR")
            return False
            
    def create_test_user(self, user_num: int) -> Dict:
        """Create a test user"""
        email = f"debug_user_{user_num}@test.com"
        password = f"debug_pass_{user_num}"
        
        self.log(f"Creating test user {user_num}: {email}")
        
        user_data = {
            "email": email,
            "password": password,
            "first_name": f"Debug{user_num}",
            "last_name": "User"
        }
        
        result = self.make_request("POST", "/auth/signup", data=user_data)
        
        if "access_token" in result:
            self.log(f"✅ User {user_num} created successfully")
            self.test_users[user_num] = {
                "email": email,
                "password": password,
                "token": result["access_token"],
                "user_id": None
            }
            return result
        else:
            self.log(f"❌ Failed to create user {user_num}: {result}", "ERROR")
            return result
            
    def get_user_info(self, user_num: int) -> Dict:
        """Get user information"""
        if user_num not in self.test_users:
            self.log(f"❌ User {user_num} not found", "ERROR")
            return {}
            
        headers = {"Authorization": f"Bearer {self.test_users[user_num]['token']}"}
        result = self.make_request("GET", "/auth/me", headers=headers)
        
        if "user_id" in result:
            self.test_users[user_num]["user_id"] = result["user_id"]
            self.log(f"✅ User {user_num} ID: {result['user_id']}")
            return result
        else:
            self.log(f"❌ Failed to get user {user_num} info: {result}", "ERROR")
            return result
            
    def send_chat_message(self, user_num: int, message: str, session_id: str = None) -> Dict:
        """Send a chat message for a user"""
        if user_num not in self.test_users or not self.test_users[user_num]["user_id"]:
            self.log(f"❌ User {user_num} not properly initialized", "ERROR")
            return {}
            
        if not session_id:
            session_id = f"debug_session_{user_num}_{int(time.time())}"
            
        chat_data = {
            "message": message,
            "user_id": self.test_users[user_num]["user_id"],
            "session_id": session_id
        }
        
        headers = {"Authorization": f"Bearer {self.test_users[user_num]['token']}"}
        result = self.make_request("POST", "/chat", data=chat_data, headers=headers)
        
        if "response" in result:
            self.log(f"✅ Chat message sent for user {user_num}")
            return result
        else:
            self.log(f"❌ Failed to send chat message for user {user_num}: {result}", "ERROR")
            return result
            
    def search_memory(self, user_num: int, query: str) -> Dict:
        """Search memory for a user"""
        if user_num not in self.test_users or not self.test_users[user_num]["user_id"]:
            self.log(f"❌ User {user_num} not properly initialized", "ERROR")
            return {}
            
        user_id = self.test_users[user_num]["user_id"]
        endpoint = f"/memory/search?user_id={user_id}&query={query}"
        
        headers = {"Authorization": f"Bearer {self.test_users[user_num]['token']}"}
        result = self.make_request("POST", endpoint, headers=headers)
        
        if "results" in result:
            self.log(f"✅ Memory search completed for user {user_num}")
            return result
        else:
            self.log(f"❌ Failed to search memory for user {user_num}: {result}", "ERROR")
            return result
            
    def debug_memory(self, user_num: int) -> Dict:
        """Get memory debug information for a user"""
        if user_num not in self.test_users or not self.test_users[user_num]["user_id"]:
            self.log(f"❌ User {user_num} not properly initialized", "ERROR")
            return {}
            
        user_id = self.test_users[user_num]["user_id"]
        endpoint = f"/memory/debug/{user_id}"
        
        headers = {"Authorization": f"Bearer {self.test_users[user_num]['token']}"}
        result = self.make_request("GET", endpoint, headers=headers)
        
        if "debug_result" in result:
            self.log(f"✅ Memory debug completed for user {user_num}")
            return result
        else:
            self.log(f"❌ Failed to debug memory for user {user_num}: {result}", "ERROR")
            return result
            
    def test_memory_isolation(self):
        """Test memory isolation between users"""
        self.log("🔍 Testing Memory Isolation...")
        
        # Create two test users
        self.create_test_user(1)
        self.create_test_user(2)
        
        # Get user IDs
        self.get_user_info(1)
        self.get_user_info(2)
        
        # Send different personal information to each user
        user1_info = "Hello! My name is Alice Johnson. I live in Seattle. I work as a data scientist. I love hiking and coffee."
        user2_info = "Hi! My name is Bob Smith. I live in Austin. I work as a software engineer. I love BBQ and football."
        
        self.send_chat_message(1, user1_info)
        self.send_chat_message(2, user2_info)
        
        # Wait a moment for memory processing
        time.sleep(3)
        
        # Debug memory for both users
        debug1 = self.debug_memory(1)
        debug2 = self.debug_memory(2)
        
        # Test search functionality
        search1_alice = self.search_memory(1, "Alice Johnson")
        search1_bob = self.search_memory(1, "Bob Smith")
        search2_alice = self.search_memory(2, "Alice Johnson")
        search2_bob = self.search_memory(2, "Bob Smith")
        
        # Analyze results
        self.analyze_isolation_results(debug1, debug2, search1_alice, search1_bob, search2_alice, search2_bob)
        
    def analyze_isolation_results(self, debug1: Dict, debug2: Dict, search1_alice: Dict, search1_bob: Dict, search2_alice: Dict, search2_bob: Dict):
        """Analyze memory isolation test results"""
        self.log("📊 Analyzing Memory Isolation Results...")
        
        # Check for memory contamination
        contamination_found = False
        
        # Check if User 1's memory contains Bob's information
        if debug1 and "debug_result" in debug1:
            debug_text = debug1["debug_result"].lower()
            if "bob smith" in debug_text or "austin" in debug_text or "bbq" in debug_text:
                self.log("❌ MEMORY CONTAMINATION: User 1's memory contains Bob's information!", "CRITICAL")
                contamination_found = True
                
        # Check if User 2's memory contains Alice's information
        if debug2 and "debug_result" in debug2:
            debug_text = debug2["debug_result"].lower()
            if "alice johnson" in debug_text or "seattle" in debug_text or "hiking" in debug_text:
                self.log("❌ MEMORY CONTAMINATION: User 2's memory contains Alice's information!", "CRITICAL")
                contamination_found = True
                
        # Check search results
        if search1_bob and "results" in search1_bob:
            if "bob smith" in search1_bob["results"].lower():
                self.log("❌ SEARCH CONTAMINATION: User 1 can search and find Bob's information!", "CRITICAL")
                contamination_found = True
                
        if search2_alice and "results" in search2_alice:
            if "alice johnson" in search2_alice["results"].lower():
                self.log("❌ SEARCH CONTAMINATION: User 2 can search and find Alice's information!", "CRITICAL")
                contamination_found = True
                
        if not contamination_found:
            self.log("✅ Memory isolation appears to be working correctly")
            
        # Print detailed results
        self.log("\n📋 DETAILED RESULTS:")
        self.log(f"User 1 Debug: {debug1.get('debug_result', 'No debug data')[:200]}...")
        self.log(f"User 2 Debug: {debug2.get('debug_result', 'No debug data')[:200]}...")
        self.log(f"User 1 Search Alice: {search1_alice.get('results', 'No results')[:100]}...")
        self.log(f"User 1 Search Bob: {search1_bob.get('results', 'No results')[:100]}...")
        self.log(f"User 2 Search Alice: {search2_alice.get('results', 'No results')[:100]}...")
        self.log(f"User 2 Search Bob: {search2_bob.get('results', 'No results')[:100]}...")
        
    def generate_fixes(self):
        """Generate fixes for identified issues"""
        self.log("🔧 Generating Fixes...")
        
        fixes = [
            "1. AGENT CONFIGURATION FIXES:",
            "   - Ensure ZepTools and Mem0Tools use user-specific collection names",
            "   - Add collection_template parameter to memory tools",
            "   - Example: ZepTools(collection_template='user_{user_id}_memories')",
            "",
            "2. MEMORY ISOLATION INSTRUCTIONS:",
            "   - Add explicit user isolation rules to agent instructions",
            "   - Ensure user_id is always passed to memory operations",
            "   - Add validation to prevent cross-user memory access",
            "",
            "3. SEARCH FUNCTIONALITY FIXES:",
            "   - Improve search prompts to include user context",
            "   - Add user_id validation in search endpoints",
            "   - Ensure search only queries user-specific memory",
            "",
            "4. API ENDPOINT FIXES:",
            "   - Add user_id validation in all memory endpoints",
            "   - Ensure proper error handling for unauthorized access",
            "   - Add logging for memory operations",
            "",
            "5. TESTING RECOMMENDATIONS:",
            "   - Add automated tests for memory isolation",
            "   - Test with multiple concurrent users",
            "   - Monitor memory usage and performance"
        ]
        
        for fix in fixes:
            self.log(fix)
            
    def run_full_debug(self):
        """Run the complete debugging process"""
        self.log("🚀 Starting Comprehensive Memory Isolation Debug")
        
        # Test backend health
        if not self.test_backend_health():
            self.log("❌ Cannot proceed - backend is not accessible", "CRITICAL")
            return
            
        # Test memory isolation
        self.test_memory_isolation()
        
        # Generate fixes
        self.generate_fixes()
        
        self.log("✅ Debug process completed")

if __name__ == "__main__":
    debugger = MemoryIsolationDebugger()
    debugger.run_full_debug() 
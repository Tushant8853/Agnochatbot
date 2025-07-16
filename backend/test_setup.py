#!/usr/bin/env python3
"""
Test script to verify Agno Chatbot Backend setup
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from config import settings
from utils.logger import logger


async def test_configuration():
    """Test configuration loading."""
    logger.info("Testing configuration...")
    
    required_vars = [
        "database_url",
        "secret_key", 
        "gemini_api_key",
        "zep_api_key",
        "mem0_api_key"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = getattr(settings, var, None)
        if not value or value.startswith("your_"):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing or default configuration for: {', '.join(missing_vars)}")
        logger.info("Please update your .env file with proper values.")
    else:
        logger.info("Configuration looks good!")
    
    return len(missing_vars) == 0


async def test_database_connection():
    """Test database connection."""
    logger.info("Testing database connection...")
    
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        engine = create_async_engine(settings.database_url, echo=False)
        
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            await result.fetchone()
        
        await engine.dispose()
        logger.info("Database connection successful!")
        return True
        
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


async def test_imports():
    """Test that all modules can be imported."""
    logger.info("Testing module imports...")
    
    modules_to_test = [
        "auth.models",
        "auth.jwt_handler", 
        "auth.deps",
        "auth.auth_routes",
        "memory.zep_memory",
        "memory.mem0_memory",
        "memory.hybrid_memory",
        "services.gemini",
        "agno_agent.agent"
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            logger.info(f"✓ {module}")
        except ImportError as e:
            logger.error(f"✗ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0


async def main():
    """Run all tests."""
    logger.info("Running Agno Chatbot Backend setup tests...")
    
    tests = [
        ("Configuration", test_configuration),
        ("Database Connection", test_database_connection),
        ("Module Imports", test_imports)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("TEST SUMMARY")
    logger.info("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nPassed: {passed}/{len(results)}")
    
    if passed == len(results):
        logger.info("🎉 All tests passed! Your setup is ready.")
        logger.info("You can now run: python start.py")
    else:
        logger.error("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 
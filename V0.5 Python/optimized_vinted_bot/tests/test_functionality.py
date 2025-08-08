"""
Test script for the Optimized Vinted Discord Bot
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import directly with absolute paths to avoid relative import issues
import sys
sys.path.append(str(PROJECT_ROOT / "core"))
sys.path.append(str(PROJECT_ROOT / "config"))
sys.path.append(str(PROJECT_ROOT / "utils"))

from vinted_api import VintedAPIClient, VintedItem
from proxy_manager import ProxyManager, ProxyInfo
from database import DatabaseManager
from settings import settings
from logging_setup import setup_logging

async def test_vinted_api():
    """Test Vinted API client functionality"""
    print("🔄 Testing Vinted API Client...")
    
    try:
        async with VintedAPIClient() as client:
            # Test search functionality
            print("  - Testing item search...")
            items = await client.search_items(
                search_query="test",
                price_to=50,
                per_page=5
            )
            
            if items:
                print(f"  ✅ Found {len(items)} items")
                
                # Test individual item
                item = items[0]
                print(f"    Sample item: {item.title} - {item.price} {item.currency}")
                
                # Test get_latest_items with URL
                print("  - Testing get_latest_items...")
                test_url = "https://www.vinted.fr/catalog?search_text=test&price_to=50"
                latest_items = await client.get_latest_items(test_url, max_items=3)
                print(f"  ✅ Latest items: {len(latest_items)} found")
                
            else:
                print("  ⚠️ No items found (might be normal)")
                
            # Test API stats
            stats = client.get_stats()
            print(f"  ✅ API Stats: {stats['total_requests']} requests, {stats['success_rate']:.2f} success rate")
            
    except Exception as e:
        print(f"  ❌ API Test failed: {e}")
        return False
        
    return True

def test_proxy_manager():
    """Test proxy manager functionality"""
    print("🔄 Testing Proxy Manager...")
    
    try:
        # Create proxy manager without file (empty)
        proxy_manager = ProxyManager(enable_rotation=True)
        
        # Add test proxies (these won't work but will test the logic)
        proxy_manager.rotator.add_proxy("http://test1:8080", "user", "pass")
        proxy_manager.rotator.add_proxy("http://test2:8080", "user", "pass")
        
        print(f"  ✅ Added test proxies: {len(proxy_manager.rotator.proxies)}")
        
        # Test proxy selection
        proxy_info = proxy_manager.rotator.get_next_proxy()
        if proxy_info:
            print(f"  ✅ Proxy selection works: {proxy_info.url}")
        
        # Test stats
        stats = proxy_manager.get_stats()
        print(f"  ✅ Proxy stats: {stats['total']} total proxies")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Proxy Manager test failed: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("🔄 Testing Database Manager...")
    
    try:
        # Use test database
        test_db_path = "test_bot.db"
        db = DatabaseManager(test_db_path)
        
        # Test adding search config
        print("  - Testing search config...")
        success = db.add_search_config(12345, "https://test.com/search")
        print(f"  ✅ Add search config: {success}")
        
        # Test getting search config
        config = db.get_search_config(12345)
        if config:
            print(f"  ✅ Retrieved config: {config['search_url']}")
        
        # Test item tracking
        print("  - Testing item tracking...")
        test_item = VintedItem(
            id=999999,
            title="Test Item",
            price="10.00",
            currency="EUR",
            brand="Test Brand",
            size="M",
            condition="Good",
            url="https://test.com/item/999999",
            photo_url="https://test.com/photo.jpg",
            user_login="testuser",
            created_at="123456789",
            updated_at="123456789"
        )
        
        # Check if already published (should be False)
        is_published = db.is_item_published(test_item.id, 12345)
        print(f"  ✅ Item published check: {is_published}")
        
        # Mark as published
        marked = db.mark_item_published(test_item, 12345, "https://test.com/search")
        print(f"  ✅ Mark item published: {marked}")
        
        # Check again (should be True now)
        is_published = db.is_item_published(test_item.id, 12345)
        print(f"  ✅ Item published check after marking: {is_published}")
        
        # Test database stats
        stats = db.get_database_stats()
        print(f"  ✅ Database stats: {stats}")
        
        # Cleanup test database
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("  ✅ Cleaned up test database")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("🔄 Testing Configuration...")
    
    try:
        # Test settings loading
        print(f"  ✅ Discord prefix: {settings.discord.command_prefix}")
        print(f"  ✅ Proxy enabled: {settings.proxy.enabled}")
        print(f"  ✅ API base URL: {settings.vinted_api.base_url}")
        print(f"  ✅ Log level: {settings.logging.level}")
        
        # Test directories (importing from settings module directly)
        from settings import BASE_DIR, LOGS_DIR, DATA_DIR
        print(f"  ✅ Base dir exists: {BASE_DIR.exists()}")
        print(f"  ✅ Logs dir exists: {LOGS_DIR.exists()}")
        print(f"  ✅ Data dir exists: {DATA_DIR.exists()}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")
        return False

def test_logging():
    """Test logging setup"""
    print("🔄 Testing Logging Setup...")
    
    try:
        # Setup logging
        setup_logging(level="DEBUG", console_output=True)
        
        import logging
        logger = logging.getLogger("test_logger")
        
        # Test different log levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        print("  ✅ Logging setup successful")
        return True
        
    except Exception as e:
        print(f"  ❌ Logging test failed: {e}")
        return False

async def run_tests():
    """Run all tests"""
    print("🚀 Starting Vinted Bot Functionality Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Logging", test_logging),
        ("Database", test_database),
        ("Proxy Manager", test_proxy_manager),
        ("Vinted API", test_vinted_api),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The bot is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")
        
    return passed == total

def main():
    """Main test function"""
    try:
        # Run async tests
        success = asyncio.run(run_tests())
        
        if success:
            print("\n✅ Bot functionality test completed successfully!")
            print("\nNext steps:")
            print("1. Configure your Discord bot token in .env")
            print("2. Add your proxy list to config/proxy_list.txt (optional)")
            print("3. Run: python main.py")
        else:
            print("\n❌ Some tests failed. Please fix the issues before running the bot.")
            
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Fatal error during testing: {e}")

if __name__ == "__main__":
    main()

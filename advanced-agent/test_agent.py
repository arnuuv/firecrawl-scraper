#!/usr/bin/env python3
"""
Test script for the Developer Tools Research Agent

This script tests the basic functionality of the agent
without requiring an OpenAI API key or making actual API calls.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        from src.models import Company, ComparisonMatrix
        print("✅ Pydantic models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import models: {e}")
        return False
    
    try:
        from src.utils import (
            generate_quick_stats,
            display_comparison_matrix,
            filter_tools,
            sort_tools,
            save_as_json,
            save_as_markdown
        )
        print("✅ Utility functions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import utils: {e}")
        return False
    
    try:
        from src.prompts import RESEARCH_PROMPT, ANALYSIS_PROMPT
        print("✅ Prompts imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import prompts: {e}")
        return False
    
    try:
        from src.firecrawl import FirecrawlScraper
        print("✅ Firecrawl scraper imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import firecrawl: {e}")
        return False
    
    return True

def test_models():
    """Test Pydantic model creation"""
    print("\n🔍 Testing Pydantic models...")
    
    try:
        from src.models import Company
        
        # Create a test company
        test_company = Company(
            name="Test Tool",
            description="A test developer tool",
            website="https://example.com",
            pricing="Free",
            open_source=True,
            api_available=True,
            languages=["Python", "JavaScript"],
            integrations=["GitHub", "Slack"],
            tech_stack=["Docker", "AWS"],
            popularity_score=8,
            community_activity="High",
            market_position="Emerging",
            trend_status="Rising",
            recent_updates="Latest version released",
            competitive_advantages=["Easy to use", "Good documentation"],
            limitations=["Limited free tier", "No mobile SDK"],
            use_cases=["Web development", "API management"],
            target_audience="Developers",
            pricing_details="Free tier with paid plans",
            api_documentation="https://docs.example.com",
            github_url="https://github.com/example/tool",
            documentation_url="https://docs.example.com"
        )
        
        print("✅ Test company created successfully")
        print(f"   Name: {test_company.name}")
        print(f"   Languages: {test_company.languages}")
        print(f"   Trend Status: {test_company.trend_status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create test company: {e}")
        return False

def test_utils():
    """Test utility functions with mock data"""
    print("\n🔍 Testing utility functions...")
    
    try:
        from src.models import Company
        from src.utils import generate_quick_stats, filter_tools, sort_tools
        
        # Create test companies
        companies = [
            Company(
                name="Tool A",
                description="First test tool",
                website="https://toola.com",
                pricing="Free",
                open_source=True,
                api_available=True,
                languages=["Python"],
                integrations=["GitHub"],
                tech_stack=["Docker"],
                popularity_score=7,
                community_activity="Medium",
                market_position="Established",
                trend_status="Stable",
                recent_updates="Regular updates",
                competitive_advantages=["Simple"],
                limitations=["Basic features"],
                use_cases=["Development"],
                target_audience="Developers",
                pricing_details="Free",
                api_documentation="https://docs.toola.com",
                github_url="https://github.com/toola",
                documentation_url="https://docs.toola.com"
            ),
            Company(
                name="Tool B",
                description="Second test tool",
                website="https://toolb.com",
                pricing="Paid",
                open_source=False,
                api_available=True,
                languages=["JavaScript", "Python"],
                integrations=["GitHub", "Slack"],
                tech_stack=["Docker", "AWS"],
                popularity_score=9,
                community_activity="High",
                market_position="Leading",
                trend_status="Hot",
                recent_updates="Major update",
                competitive_advantages=["Advanced features"],
                limitations=["Expensive"],
                use_cases=["Enterprise"],
                target_audience="Enterprise",
                pricing_details="Paid plans",
                api_documentation="https://docs.toolb.com",
                github_url="",
                documentation_url="https://docs.toolb.com"
            )
        ]
        
        # Test quick stats
        stats = generate_quick_stats(companies)
        print("✅ Quick stats generated successfully")
        print(f"   Stats: {stats[:100]}...")
        
        # Test filtering
        free_tools = filter_tools(companies, pricing="free")
        print(f"✅ Filtering works: {len(free_tools)} free tools found")
        
        # Test sorting
        sorted_tools = sort_tools(companies, sort_by="popularity_score", reverse=True)
        print(f"✅ Sorting works: Top tool is {sorted_tools[0].name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test utilities: {e}")
        return False

def test_file_operations():
    """Test file saving operations"""
    print("\n🔍 Testing file operations...")
    
    try:
        from src.utils import save_as_json, save_as_markdown
        
        # Create test data
        test_data = {
            "companies": [],
            "analysis": "Test analysis",
            "comparison_matrix": {},
            "metadata": {
                "query": "test query",
                "timestamp": "20240101_120000"
            }
        }
        
        # Test JSON save
        json_file = save_as_json(test_data, "test")
        if os.path.exists(json_file):
            print(f"✅ JSON file saved: {json_file}")
            os.remove(json_file)  # Clean up
        else:
            print("❌ JSON file not created")
            return False
        
        # Test Markdown save
        md_file = save_as_markdown(test_data, "test")
        if os.path.exists(md_file):
            print(f"✅ Markdown file saved: {md_file}")
            os.remove(md_file)  # Clean up
        else:
            print("❌ Markdown file not created")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test file operations: {e}")
        return False

def test_environment():
    """Test environment setup"""
    print("\n🔍 Testing environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 11:
        print(f"✅ Python version {python_version.major}.{python_version.minor}.{python_version.micro} is compatible")
    else:
        print(f"❌ Python version {python_version.major}.{python_version.minor}.{python_version.micro} is too old (need 3.11+)")
        return False
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("⚠️ .env file not found (you'll need to create one with OPENAI_API_KEY)")
    
    # Check if dependencies are installed
    try:
        import firecrawl_py
        print("✅ firecrawl-py is installed")
    except ImportError:
        print("❌ firecrawl-py is not installed")
        return False
    
    try:
        import langchain_openai
        print("✅ langchain-openai is installed")
    except ImportError:
        print("❌ langchain-openai is not installed")
        return False
    
    try:
        import langgraph
        print("✅ langgraph is installed")
    except ImportError:
        print("❌ langgraph is not installed")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Developer Tools Research Agent - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("Models", test_models),
        ("Utilities", test_utils),
        ("File Operations", test_file_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The agent is ready to use.")
        print("\nNext steps:")
        print("1. Create a .env file with your OPENAI_API_KEY")
        print("2. Run: python main.py")
        print("3. Or run: python example_usage.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
#!/usr/bin/env python3
"""
Test script for AI Customer Support Agent
Run this to verify all components are working correctly
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Config: {e}")
        return False
    
    try:
        from utils.knowledge_base import KnowledgeBaseManager
        print("✅ KnowledgeBaseManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import KnowledgeBaseManager: {e}")
        return False
    
    try:
        from models.ai_agent import CustomerSupportAgent
        print("✅ CustomerSupportAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CustomerSupportAgent: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import Config
        
        # Test if required directories exist
        os.makedirs(Config.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        os.makedirs(Config.KNOWLEDGE_BASE_DIR, exist_ok=True)
        
        print("✅ Configuration directories created")
        print(f"   Chroma DB: {Config.CHROMA_PERSIST_DIRECTORY}")
        print(f"   Knowledge Base: {Config.KNOWLEDGE_BASE_DIR}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base functionality"""
    print("\n📚 Testing knowledge base...")
    
    try:
        from config import Config
        from utils.knowledge_base import KnowledgeBaseManager
        
        # Initialize knowledge base
        kb = KnowledgeBaseManager(Config.CHROMA_PERSIST_DIRECTORY)
        print("✅ Knowledge base initialized")
        
        # Test collection info
        info = kb.get_collection_info()
        print(f"   Collection info: {info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Knowledge base test failed: {e}")
        return False

def test_sample_documents():
    """Test if sample documents exist"""
    print("\n📄 Testing sample documents...")
    
    sample_files = [
        "data/knowledge_base/sample_faq.txt",
        "data/knowledge_base/product_guide.md",
        "data/knowledge_base/support_tickets.csv"
    ]
    
    all_exist = True
    for file_path in sample_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_requirements():
    """Test if required packages are installed"""
    print("\n📦 Testing required packages...")
    
    required_packages = [
        'langchain',
        'langchain_google_genai',
        'langchain_community',
        'google_generativeai',
        'chromadb',
        'streamlit',
        'python-dotenv'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            all_installed = False
    
    return all_installed

def main():
    """Run all tests"""
    print("🚀 Starting AI Customer Support Agent System Tests")
    print("=" * 60)
    
    tests = [
        ("Package Installation", test_requirements),
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Knowledge Base", test_knowledge_base),
        ("Sample Documents", test_sample_documents)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Set your Google Gemini API key in .env file")
        print("2. Run: streamlit run ui/streamlit_app.py")
        print("3. Or run: python console_app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check file permissions and paths")
        print("3. Verify your Python environment")

if __name__ == "__main__":
    main()

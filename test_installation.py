#!/usr/bin/env python3
"""Test script to verify the job application assistant installation."""

import sys
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all major modules can be imported."""
    print("🧪 Testing imports...")
    
    tests = [
        ("Core Config", "job_application_assistant.core.config"),
        ("Core LLM", "job_application_assistant.core.llm"),
        ("Core Logging", "job_application_assistant.core.logging"),
        ("Core Exceptions", "job_application_assistant.core.exceptions"),
        ("Data Models", "job_application_assistant.models.data_models"),
        ("Job Application Agent", "job_application_assistant.agents.job_application_agent"),
        ("Interview Prep Agent", "job_application_assistant.agents.interview_prep_agent"),
        ("Document Processor", "job_application_assistant.tools.document_processor"),
        ("Streamlit Helpers", "job_application_assistant.utils.streamlit_helpers"),
    ]
    
    failed = []
    
    for name, module in tests:
        try:
            __import__(module)
            print(f"✅ {name}")
        except Exception as e:
            print(f"❌ {name}: {e}")
            failed.append((name, module, e))
    
    return failed

def test_config():
    """Test configuration loading."""
    print("\n🔧 Testing configuration...")
    
    try:
        from job_application_assistant.core.config import get_settings
        settings = get_settings()
        print(f"✅ Configuration loaded")
        print(f"   - Model: {settings.primary_model_name}")
        print(f"   - Base URL: {settings.ollama_base_url}")
        print(f"   - Log Level: {settings.log_level}")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        traceback.print_exc()
        return False

def test_llm_manager():
    """Test LLM manager initialization."""
    print("\n🤖 Testing LLM Manager...")
    
    try:
        from job_application_assistant.core.llm import get_llm_manager
        llm_manager = get_llm_manager()
        print(f"✅ LLM Manager initialized")
        print(f"   - Primary Model: {llm_manager.settings.primary_model_name}")
        print(f"   - Base URL: {llm_manager.settings.ollama_base_url}")
        print(f"   - Ollama Available: {'✅ Yes' if llm_manager.settings.is_ollama_available else '❌ No'}")
        return True
    except Exception as e:
        print(f"❌ LLM Manager failed: {e}")
        traceback.print_exc()
        return False

def test_entry_points():
    """Test entry points."""
    print("\n🚀 Testing entry points...")
    
    # Test CLI entry point
    try:
        from job_application_assistant.cli.main import app
        print("✅ CLI entry point accessible")
    except Exception as e:
        print(f"❌ CLI entry point failed: {e}")
    
    # Test web entry point
    try:
        from job_application_assistant.web.app import main
        print("✅ Web entry point accessible")
    except Exception as e:
        print(f"❌ Web entry point failed: {e}")

def main():
    """Run all tests."""
    print("🎯 Job Application Assistant - Installation Test")
    print("=" * 50)
    
    # Test imports
    failed_imports = test_imports()
    
    # Test configuration
    config_ok = test_config()
    
    # Test LLM manager
    llm_ok = test_llm_manager()
    
    # Test entry points
    test_entry_points()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    if failed_imports:
        print(f"❌ {len(failed_imports)} import(s) failed:")
        for name, module, error in failed_imports:
            print(f"   - {name}: {error}")
    else:
        print("✅ All imports successful")
    
    if config_ok:
        print("✅ Configuration working")
    else:
        print("❌ Configuration issues")
    
    if llm_ok:
        print("✅ LLM Manager working")
    else:
        print("❌ LLM Manager issues")
    
    print("\n💡 Next steps:")
    print("   1. Make sure Ollama is running: ollama serve")
    print("   2. Install a model: ollama pull llama3.2")
    print("   3. Run the web app: python run_web.py")
    print("   4. Or run the CLI: python run_cli.py --help")
    
    # Return exit code
    if failed_imports or not config_ok:
        sys.exit(1)
    else:
        print("\n🎉 Installation test passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()

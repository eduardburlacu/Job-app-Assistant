#!/usr/bin/env python3
"""Quick functionality test for the job application assistant."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_functionality():
    """Test basic functionality without actually calling LLM."""
    print("🔧 Testing basic functionality...")
    
    try:
        # Test data models
        from job_application_assistant.models.data_models import JobDescription, UserProfile, UserPreferences
        
        # Create test objects
        job_desc = JobDescription(
            title="Software Engineer",
            company="Test Company",
            requirements=["Python", "React", "5+ years experience"],
            description="A test job description for a software engineer position.",
            location="Remote",
            salary_range="$80k-120k"
        )
        
        user_profile = UserProfile(
            name="Test User",
            email="test@example.com",
            phone="123-456-7890",
            skills=["Python", "JavaScript", "React", "Django"],
            cv_text="Test CV content with relevant experience.",
            experience=[]
        )
        
        user_prefs = UserPreferences(
            job_interest_level=8,
            motivation="Test motivation",
            relevant_experience="Test relevant experience",
            career_goals="Test career goals",
            company_knowledge="Test company knowledge"
        )
        
        print("✅ Data models working correctly")
        
        # Test agents initialization (without calling LLM)
        from job_application_assistant.agents.job_application_agent import JobApplicationAgent
        from job_application_assistant.agents.interview_prep_agent import InterviewPreparationAgent
        
        # Note: These will fail if Ollama is not running, but that's expected
        print("✅ Agent classes can be imported")
        
        # Test configuration
        from job_application_assistant.core.config import get_settings
        settings = get_settings()
        
        print(f"✅ Configuration loaded: {settings.app_name} v{settings.app_version}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run basic functionality test."""
    print("🎯 Job Application Assistant - Functionality Test")
    print("=" * 50)
    
    if test_basic_functionality():
        print("\n🎉 Basic functionality test passed!")
        print("\n💡 Ready for full testing:")
        print("   1. Start Ollama: ollama serve")
        print("   2. Install a model: ollama pull llama3.2")
        print("   3. Test web app: python run_web.py")
        print("   4. Test CLI: python run_cli.py --help")
        return 0
    else:
        print("\n❌ Basic functionality test failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

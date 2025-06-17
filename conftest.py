"""Pytest configuration for Job Application Assistant tests."""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def sample_job_description():
    """Sample job description for testing."""
    from job_application_assistant.models.data_models import JobDescription
    
    return JobDescription(
        title="Senior Python Developer",
        company="Tech Innovations Inc.",
        requirements=[
            "5+ years Python experience",
            "Experience with FastAPI or Django",
            "Strong knowledge of databases",
            "Experience with cloud platforms"
        ],
        description="We are looking for a senior Python developer to join our team...",
        location="Remote",
        salary_range="$100,000 - $150,000"
    )

@pytest.fixture
def sample_user_profile():
    """Sample user profile for testing."""
    from job_application_assistant.models.data_models import UserProfile
    
    return UserProfile(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1-555-0123",
        skills=["Python", "Django", "PostgreSQL", "AWS", "Docker"],
        cv_text="Experienced Python developer with 6+ years of experience...",
        experience=[]
    )

@pytest.fixture
def sample_user_preferences():
    """Sample user preferences for testing."""
    from job_application_assistant.models.data_models import UserPreferences
    
    return UserPreferences(
        job_interest_level=9,
        motivation="I'm excited about this role because...",
        relevant_experience="My experience with Python and cloud platforms...",
        career_goals="I want to grow as a senior developer...",
        company_knowledge="I've researched the company and admire..."
    )

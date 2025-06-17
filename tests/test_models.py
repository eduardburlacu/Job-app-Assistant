"""Test the data models."""

import pytest
from pydantic import ValidationError

from job_application_assistant.models.data_models import (
    JobDescription,
    UserProfile, 
    UserPreferences,
    ApplicationDocument,
    InterviewPreparation
)


class TestJobDescription:
    """Test JobDescription model."""
    
    def test_valid_job_description(self, sample_job_description):
        """Test creating a valid job description."""
        assert sample_job_description.title == "Senior Python Developer"
        assert sample_job_description.company == "Tech Innovations Inc."
        assert len(sample_job_description.requirements) == 4
    
    def test_job_description_validation(self):
        """Test job description validation."""
        with pytest.raises(ValidationError):
            JobDescription(
                title="",  # Empty title should fail
                company="Test Company",
                requirements=[],
                description="Test description"
            )


class TestUserProfile:
    """Test UserProfile model."""
    
    def test_valid_user_profile(self, sample_user_profile):
        """Test creating a valid user profile."""
        assert sample_user_profile.name == "John Doe"
        assert sample_user_profile.email == "john.doe@example.com"
        assert "Python" in sample_user_profile.skills
    
    def test_email_validation(self):
        """Test email validation."""
        with pytest.raises(ValidationError):
            UserProfile(
                name="Test User",
                email="invalid-email",  # Invalid email
                phone="+1-555-0123",
                skills=["Python"],
                cv_text="Test CV"
            )


class TestUserPreferences:
    """Test UserPreferences model."""
    
    def test_valid_user_preferences(self, sample_user_preferences):
        """Test creating valid user preferences."""
        assert sample_user_preferences.job_interest_level == 9
        assert sample_user_preferences.motivation.startswith("I'm excited")
    
    def test_interest_level_validation(self):
        """Test interest level validation."""
        with pytest.raises(ValidationError):
            UserPreferences(
                job_interest_level=11,  # Should be 1-10
                motivation="Test motivation",
                relevant_experience="Test experience",
                career_goals="Test goals",
                company_knowledge="Test knowledge"
            )


class TestApplicationDocument:
    """Test ApplicationDocument model."""
    
    def test_valid_application_document(self):
        """Test creating a valid application document."""
        doc = ApplicationDocument(
            document_type="cover_letter",
            title="Cover Letter for Senior Python Developer",
            content="Dear Hiring Manager...",
            created_at="2025-06-17T10:00:00Z"
        )
        
        assert doc.document_type == "cover_letter"
        assert doc.title == "Cover Letter for Senior Python Developer"
        assert doc.content.startswith("Dear Hiring Manager")


class TestInterviewPreparation:
    """Test InterviewPreparation model."""
    
    def test_valid_interview_preparation(self):
        """Test creating valid interview preparation."""
        prep = InterviewPreparation(
            confidence_checklist=["Python fundamentals", "System design"],
            technical_topics=["Review algorithms", "Practice coding"],
            behavioral_questions=["Tell me about yourself", "Why this company?"],
            technical_questions=["How do you optimize Python code?", "Explain decorators"]
        )
        
        assert len(prep.confidence_checklist) == 2
        assert len(prep.technical_topics) == 2
        assert len(prep.behavioral_questions) == 2
        assert len(prep.technical_questions) == 2

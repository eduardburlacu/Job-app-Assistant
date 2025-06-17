"""Data models for the Job Application Assistant."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator, EmailStr


class JobDescription(BaseModel):
    """Model for job description data."""
    
    title: str = Field(..., description="Job title", min_length=1)
    company: str = Field(..., description="Company name", min_length=1)
    description: str = Field(..., description="Full job description text")
    requirements: List[str] = Field(default_factory=list, description="Job requirements")
    skills: List[str] = Field(default_factory=list, description="Required skills")
    location: Optional[str] = Field(None, description="Job location")
    salary_range: Optional[str] = Field(None, description="Salary range")
    job_type: Optional[str] = Field(None, description="Job type (full-time, part-time, etc.)")
    url: Optional[HttpUrl] = Field(None, description="Job posting URL")
    posted_date: Optional[datetime] = Field(None, description="When the job was posted")


class UserProfile(BaseModel):
    """Model for user profile data."""
    
    name: str = Field(..., description="User's full name", min_length=1)
    email: EmailStr = Field(..., description="User's email address")
    phone: Optional[str] = Field(None, description="User's phone number")
    cv_text: str = Field(..., description="CV/Resume content as text")
    skills: List[str] = Field(default_factory=list, description="User's skills")
    experience: List[Dict[str, Any]] = Field(default_factory=list, description="Work experience")
    education: List[Dict[str, Any]] = Field(default_factory=list, description="Educational background")
    linkedin_url: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub profile URL")


class UserPreferences(BaseModel):
    """Model for user preferences about a specific job."""
    
    job_interest_level: int = Field(..., ge=1, le=10, description="Interest level (1-10)")
    motivation: str = Field(..., description="What motivates user about this job")
    relevant_experience: str = Field(..., description="Most relevant experience for this role")
    career_goals: str = Field(..., description="How this job fits career goals")
    company_knowledge: str = Field(..., description="What user knows about the company")
    concerns: Optional[str] = Field(None, description="Any concerns about the role")
    additional_info: Optional[str] = Field(None, description="Additional information to include")


class ApplicationDocument(BaseModel):
    """Model for generated application documents."""
    
    document_type: str = Field(..., description="Type of document (cover_letter, motivation_letter, etc.)")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    job_id: Optional[str] = Field(None, description="Related job ID")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class InterviewPreparation(BaseModel):
    """Model for interview preparation materials."""
    
    confidence_checklist: List[str] = Field(default_factory=list, description="Topics to be confident in")
    technical_topics: List[str] = Field(default_factory=list, description="Technical topics to study")
    behavioral_questions: List[str] = Field(default_factory=list, description="Behavioral interview questions")
    technical_questions: List[str] = Field(default_factory=list, description="Technical interview questions")
    company_research: List[str] = Field(default_factory=list, description="Company research points")
    questions_to_ask: List[str] = Field(default_factory=list, description="Questions to ask the interviewer")
    preparation_timeline: Dict[str, List[str]] = Field(default_factory=dict, description="Study timeline")


class ApplicationSession(BaseModel):
    """Model for an application session."""
    
    session_id: str = Field(..., description="Unique session identifier")
    job_description: JobDescription = Field(..., description="Job description")
    user_profile: UserProfile = Field(..., description="User profile")
    user_preferences: UserPreferences = Field(..., description="User preferences")
    generated_documents: List[ApplicationDocument] = Field(default_factory=list, description="Generated documents")
    interview_prep: Optional[InterviewPreparation] = Field(None, description="Interview preparation materials")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")
    status: str = Field(default="active", description="Session status")

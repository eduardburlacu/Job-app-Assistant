"""Job Application Agent using simplified LangChain chains."""

from typing import Dict, Any, Optional, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from job_application_assistant.core.llm import get_llm_manager
from job_application_assistant.models.data_models import JobDescription, UserProfile, UserPreferences, ApplicationDocument


class JobApplicationAgent:
    """Simplified job application agent using LangChain chains."""
    
    def __init__(self):
        """Initialize the job application agent."""
        llm_manager = get_llm_manager()
        self.llm = llm_manager.get_llm()
    
    async def analyze_job(self, job_description: JobDescription) -> str:
        """Analyze the job description."""
        analysis_prompt = ChatPromptTemplate.from_template("""
        Analyze this job description and extract key information:
        
        Job Title: {title}
        Company: {company}
        Description: {description}
        
        Please extract:
        1. Key requirements and qualifications
        2. Technical skills needed
        3. Soft skills emphasized
        4. Company culture indicators
        5. Growth opportunities mentioned
        
        Format your response as a structured analysis.
        """)
        
        chain = analysis_prompt | self.llm | StrOutputParser()
        
        return await chain.ainvoke({
            "title": job_description.title,
            "company": job_description.company,
            "description": job_description.description
        })
    
    async def generate_cover_letter(
        self,
        job_description: JobDescription,
        user_profile: UserProfile,
        user_preferences: UserPreferences
    ) -> ApplicationDocument:
        """Generate a personalized cover letter."""
        cover_letter_prompt = ChatPromptTemplate.from_template("""
        Write a compelling cover letter for this job application:
        
        Job: {job_title} at {company}
        Job Description: {job_description}
        
        Applicant Profile:
        Name: {name}
        Skills: {skills}
        Experience: {experience}
        
        User Preferences:
        Motivation: {motivation}
        Relevant Experience: {relevant_experience}
        Career Goals: {career_goals}
        Company Knowledge: {company_knowledge}
        
        Write a professional, personalized cover letter that:
        1. Shows genuine interest and understanding of the role
        2. Highlights relevant experience and skills
        3. Demonstrates knowledge of the company
        4. Connects the user's goals with the opportunity
        5. Is engaging and memorable
        
        Keep it to 3-4 paragraphs and maintain a professional tone.
        """)
        
        chain = cover_letter_prompt | self.llm | StrOutputParser()
        
        content = await chain.ainvoke({
            "job_title": job_description.title,
            "company": job_description.company,
            "job_description": job_description.description,
            "name": user_profile.name,
            "skills": ", ".join(user_profile.skills),
            "experience": str(user_profile.experience),
            "motivation": user_preferences.motivation,
            "relevant_experience": user_preferences.relevant_experience,
            "career_goals": user_preferences.career_goals,
            "company_knowledge": user_preferences.company_knowledge
        })
        
        return ApplicationDocument(
            document_type="cover_letter",
            title=f"Cover Letter - {job_description.title} at {job_description.company}",
            content=content
        )
    
    async def generate_motivation_letter(
        self,
        job_description: JobDescription,
        user_profile: UserProfile,
        user_preferences: UserPreferences
    ) -> ApplicationDocument:
        """Generate a motivation letter."""
        motivation_prompt = ChatPromptTemplate.from_template("""
        Write a detailed motivation letter for this job application:
        
        Job: {job_title} at {company}
        
        Focus on:
        1. Deep personal motivation for this specific role
        2. Alignment with career aspirations
        3. Unique value proposition
        4. Specific examples of relevant achievements
        5. Future contributions to the company
        
        User's Motivation: {motivation}
        Career Goals: {career_goals}
        Relevant Experience: {relevant_experience}
        
        Write a compelling motivation letter that goes beyond the cover letter.
        """)
        
        chain = motivation_prompt | self.llm | StrOutputParser()
        
        content = await chain.ainvoke({
            "job_title": job_description.title,
            "company": job_description.company,
            "motivation": user_preferences.motivation,
            "career_goals": user_preferences.career_goals,
            "relevant_experience": user_preferences.relevant_experience
        })
        
        return ApplicationDocument(
            document_type="motivation_letter",
            title=f"Motivation Letter - {job_description.title} at {job_description.company}",
            content=content
        )
    
    async def process_application(
        self,
        job_description: JobDescription,
        user_profile: UserProfile,
        user_preferences: UserPreferences
    ) -> Dict[str, Any]:
        """Process a complete job application."""
        try:
            # Analyze job
            analysis = await self.analyze_job(job_description)
            
            # Generate documents
            cover_letter = await self.generate_cover_letter(
                job_description, user_profile, user_preferences
            )
            
            motivation_letter = await self.generate_motivation_letter(
                job_description, user_profile, user_preferences
            )
            
            return {
                "job_description": job_description,
                "user_profile": user_profile,
                "user_preferences": user_preferences,
                "generated_documents": [cover_letter, motivation_letter],
                "analysis": analysis,
                "error": None
            }
            
        except Exception as e:
            return {
                "error": f"Error processing application: {str(e)}",
                "generated_documents": []
            }

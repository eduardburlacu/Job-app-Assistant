"""Interview Preparation Agent using simplified LangChain chains."""

from typing import Dict, Any, Optional, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from job_application_assistant.core.llm import get_llm_manager
from job_application_assistant.models.data_models import JobDescription, UserProfile, InterviewPreparation


class InterviewPreparationAgent:
    """Simplified interview preparation agent using LangChain chains."""
    
    def __init__(self):
        """Initialize the interview preparation agent."""
        llm_manager = get_llm_manager()
        self.llm = llm_manager.get_llm()
    
    async def create_confidence_checklist(
        self, 
        job_description: JobDescription, 
        user_profile: UserProfile
    ) -> List[str]:
        """Create a checklist of topics to be confident about."""
        checklist_prompt = ChatPromptTemplate.from_template("""
        Create a comprehensive confidence checklist for this interview:
        
        Job: {job_title} at {company}
        Key Requirements: {requirements}
        User Skills: {user_skills}
        
        Create a checklist of topics the candidate should be very confident discussing:
        1. Technical concepts and skills
        2. Relevant project experiences
        3. Industry knowledge
        4. Company knowledge
        5. Role-specific competencies
        
        Format as a bulleted list with clear, actionable items.
        Each item should be something concrete they can prepare for.
        Return only the list items, one per line, without bullet points.
        """)
        
        chain = checklist_prompt | self.llm | StrOutputParser()
        
        checklist_text = await chain.ainvoke({
            "job_title": job_description.title,
            "company": job_description.company,
            "requirements": ", ".join(job_description.requirements),
            "user_skills": ", ".join(user_profile.skills)
        })
        
        # Parse into list
        return [
            item.strip("- •").strip() 
            for item in checklist_text.split("\n") 
            if item.strip() and not item.strip().isdigit()
        ]
    
    async def generate_technical_questions(
        self, 
        job_description: JobDescription
    ) -> List[str]:
        """Generate technical interview questions."""
        technical_prompt = ChatPromptTemplate.from_template("""
        Generate technical interview questions for this role:
        
        Job: {job_title} at {company}
        Technical Requirements: {requirements}
        Required Skills: {skills}
        
        Create 10-15 technical questions covering:
        1. Core technical skills
        2. Problem-solving scenarios
        3. System design (if applicable)
        4. Best practices and methodologies
        5. Real-world application scenarios
        
        Mix different question types:
        - Conceptual questions
        - Practical coding/implementation questions
        - Scenario-based questions
        - Architecture/design questions
        
        Return only the questions, one per line.
        """)
        
        chain = technical_prompt | self.llm | StrOutputParser()
        
        questions_text = await chain.ainvoke({
            "job_title": job_description.title,
            "company": job_description.company,
            "requirements": ", ".join(job_description.requirements),
            "skills": ", ".join(job_description.skills)
        })
        
        # Parse into list
        return [
            item.strip("- •").strip() 
            for item in questions_text.split("\n") 
            if item.strip() and "?" in item
        ]
    
    async def generate_behavioral_questions(
        self, 
        job_description: JobDescription
    ) -> List[str]:
        """Generate behavioral interview questions."""
        behavioral_prompt = ChatPromptTemplate.from_template("""
        Generate behavioral interview questions for this role:
        
        Job: {job_title} at {company}
        Job Description: {description}
        
        Create 8-12 behavioral questions using the STAR method format:
        1. Leadership and teamwork
        2. Problem-solving and conflict resolution
        3. Communication and collaboration
        4. Adaptability and learning
        5. Initiative and innovation
        6. Time management and prioritization
        
        Focus on competencies most relevant to this specific role.
        Include both standard questions and role-specific scenarios.
        
        Format: "Tell me about a time when..." or "Describe a situation where..."
        Return only the questions, one per line.
        """)
        
        chain = behavioral_prompt | self.llm | StrOutputParser()
        
        questions_text = await chain.ainvoke({
            "job_title": job_description.title,
            "company": job_description.company,
            "description": job_description.description
        })
        
        # Parse into list
        return [
            item.strip("- •").strip() 
            for item in questions_text.split("\n") 
            if item.strip() and ("Tell me" in item or "Describe" in item or "?" in item)
        ]
    
    async def generate_questions_to_ask(
        self, 
        job_description: JobDescription
    ) -> List[str]:
        """Generate thoughtful questions to ask the interviewer."""
        questions_prompt = ChatPromptTemplate.from_template("""
        Generate thoughtful questions to ask the interviewer for this role:
        
        Job: {job_title} at {company}
        
        Create 5-8 questions that show:
        1. Genuine interest in the role and company
        2. Understanding of the business
        3. Desire to contribute and grow
        4. Professional curiosity
        
        Avoid questions about salary, benefits, or basic company information easily found online.
        
        Return only the questions, one per line.
        """)
        
        chain = questions_prompt | self.llm | StrOutputParser()
        
        questions_text = await chain.ainvoke({
            "job_title": job_description.title,
            "company": job_description.company
        })
        
        # Parse into list and filter
        questions = [
            item.strip("- •").strip() 
            for item in questions_text.split("\n") 
            if item.strip() and "?" in item
        ]
        
        # Add some default good questions if needed
        if len(questions) < 3:
            questions.extend([
                "What are the biggest challenges facing the team right now?",
                "How do you measure success in this role?",
                "What opportunities are there for professional development?",
                "Can you describe the team culture and collaboration style?",
                "What are the company's priorities for the next year?"
            ])
        
        return questions[:8]  # Limit to 8 questions
    
    async def prepare_for_interview(
        self,
        job_description: JobDescription,
        user_profile: UserProfile
    ) -> Dict[str, Any]:
        """Prepare comprehensive interview materials."""
        try:
            # Generate all preparation materials
            confidence_checklist = await self.create_confidence_checklist(
                job_description, user_profile
            )
            
            technical_questions = await self.generate_technical_questions(
                job_description
            )
            
            behavioral_questions = await self.generate_behavioral_questions(
                job_description
            )
            
            questions_to_ask = await self.generate_questions_to_ask(
                job_description
            )
            
            # Create interview preparation object
            interview_prep = InterviewPreparation(
                confidence_checklist=confidence_checklist,
                technical_questions=technical_questions,
                behavioral_questions=behavioral_questions,
                questions_to_ask=questions_to_ask,
                preparation_timeline={
                    "Week 1": ["Foundation study", "Core concepts review"],
                    "Week 2": ["Technical practice", "Mock coding sessions"],
                    "Week 3": ["Behavioral prep", "STAR method practice"],
                    "Final Days": ["Review and polish", "Interview simulation"]
                }
            )
            
            return {
                "interview_prep": interview_prep,
                "error": None
            }
            
        except Exception as e:
            return {
                "error": f"Error preparing for interview: {str(e)}",
                "interview_prep": None
            }

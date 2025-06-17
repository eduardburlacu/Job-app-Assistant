"""Streamlit web application for the Job Application Assistant."""

import asyncio
import streamlit as st
from typing import Optional
import tempfile
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Try to import required packages
try:
    from job_application_assistant.core.config import Settings
    from job_application_assistant.models.data_models import JobDescription, UserProfile, UserPreferences
    from job_application_assistant.agents.job_application_agent import JobApplicationAgent
    from job_application_assistant.agents.interview_prep_agent import InterviewPreparationAgent
    from job_application_assistant.tools.document_processor import process_cv_file, extract_job_description
    from job_application_assistant.core.llm import get_llm_manager
    from job_application_assistant.utils.streamlit_helpers import (
        StreamlitJobApplicationAgent, 
        StreamlitInterviewPreparationAgent,
        get_model_info
    )
except ImportError as e:
    st.error(f"Missing dependencies: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Job Application Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'job_description' not in st.session_state:
    st.session_state.job_description = None
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = None


def main():
    """Main application function."""
    st.title("🚀 Job Application & Interview Assistant")
    st.markdown("*Powered by Local AI Models*")
    
    # Sidebar for system info
    with st.sidebar:
        st.header("System Information")
        try:
            model_info = get_model_info()
            st.info(f"**Model:** {model_info['model']}")
            st.info(f"**Provider:** {model_info['provider']}")
        except Exception as e:
            st.error(f"Error getting model info: {e}")
    
    # Main navigation
    tab1, tab2, tab3 = st.tabs(["📝 Profile Setup", "🎯 Job Application", "🎤 Interview Prep"])
    
    with tab1:
        setup_profile_tab()
    
    with tab2:
        job_application_tab()
    
    with tab3:
        interview_prep_tab()


def setup_profile_tab():
    """Profile setup tab."""
    st.header("📝 Set Up Your Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Information")
        name = st.text_input("Full Name", value="")
        email = st.text_input("Email Address", value="")
        phone = st.text_input("Phone Number", value="")
    
    with col2:
        st.subheader("CV/Resume Upload")
        uploaded_file = st.file_uploader(
            "Upload your CV/Resume",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, Word Document, Text File"
        )
    
    st.subheader("Skills & Experience")
    skills_input = st.text_area(
        "List your key skills (one per line or comma-separated)",
        height=100
    )
    
    experience_summary = st.text_area(
        "Brief summary of your experience and background",
        height=150
    )
    
    if st.button("💾 Save Profile", type="primary"):
        if not name or not email:
            st.error("Please fill in at least your name and email.")
            return
        
        # Process CV if uploaded
        cv_text = experience_summary
        skills = []
        
        if uploaded_file:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process the file
                with st.spinner("Processing your CV..."):
                    user_profile = process_cv_file(tmp_path)
                    cv_text = user_profile.cv_text
                    skills = user_profile.skills
                
                # Clean up
                os.unlink(tmp_path)
                
                st.success("✅ CV processed successfully!")
                
            except Exception as e:
                st.error(f"Error processing CV: {e}")
        
        # Parse skills from input
        if skills_input:
            manual_skills = [
                skill.strip() 
                for skill in skills_input.replace('\n', ',').split(',') 
                if skill.strip()
            ]
            skills.extend(manual_skills)
        
        # Create user profile
        st.session_state.user_profile = UserProfile(
            name=name,
            email=email,
            phone=phone if phone else None,
            cv_text=cv_text,
            skills=list(set(skills)),  # Remove duplicates
            experience=[],
            education=[]
        )
        
        st.success("✅ Profile saved successfully!")
        st.balloons()


def job_application_tab():
    """Job application tab."""
    st.header("🎯 Create Job Application")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please set up your profile first in the Profile Setup tab.")
        return
    
    # Job Description Input
    st.subheader("Job Description")
    
    with st.expander("💡 Tips for Job URL Extraction", expanded=False):
        st.markdown("""
        **For LinkedIn Jobs:**
        - LinkedIn requires authentication, so URL extraction may be limited
        - **Recommended:** Copy the job description text and use "📝 Paste Text"
        
        **For Other Job Sites (Indeed, Glassdoor):**
        - Direct job posting URLs work best
        - Make sure the URL is publicly accessible
        
        **If URL extraction fails:**
        - Try copying the job description text instead
        - Use "✍️ Manual Entry" for complete control
        """)
    
    input_method = st.radio(
        "How would you like to provide the job description?",
        ["📝 Paste Text", "🔗 URL", "✍️ Manual Entry"]
    )
    
    job_desc = None
    
    if input_method == "📝 Paste Text":
        job_text = st.text_area(
            "Paste the complete job description here:",
            height=200
        )
        if job_text and st.button("📋 Process Job Description"):
            with st.spinner("Processing job description..."):
                try:
                    job_desc = extract_job_description(job_text)
                    st.session_state.job_description = job_desc
                    st.success("✅ Job description processed!")
                except Exception as e:
                    st.error(f"Error processing job description: {e}")
    
    elif input_method == "🔗 URL":
        job_url = st.text_input("Enter the job posting URL:")
        
        # Provide guidance for LinkedIn URLs
        if job_url and "linkedin.com" in job_url.lower():
            st.info("""
            📝 **LinkedIn URL Tips:**
            - LinkedIn requires authentication for full access
            - For best results, copy the job description text directly
            - Use the "📄 Text/Paste" option above for better extraction
            """)
        
        if job_url and st.button("🔗 Extract from URL"):
            with st.spinner("Extracting job description from URL..."):
                try:
                    job_desc = extract_job_description(job_url)
                    
                    # Check if extraction was successful
                    if hasattr(job_desc, 'title') and job_desc.title == "Unknown Position":
                        st.warning("""
                        ⚠️ **Limited extraction from this URL**
                        
                        The job information couldn't be fully extracted (likely due to authentication requirements).
                        
                        **Recommended alternatives:**
                        1. Copy the job description text and use "📄 Text/Paste" option
                        2. Or fill in the details manually using "✍️ Manual Entry"
                        """)
                        
                        # Still save what we got
                        st.session_state.job_description = job_desc
                    else:
                        st.session_state.job_description = job_desc
                        st.success("✅ Job description extracted!")
                        
                        # Show what was extracted
                        st.write("**Extracted:**")
                        st.write(f"- **Title:** {job_desc.title}")
                        st.write(f"- **Company:** {job_desc.company}")
                        if job_desc.location:
                            st.write(f"- **Location:** {job_desc.location}")
                        
                except Exception as e:
                    st.error(f"Error extracting job description: {e}")
                    st.info("💡 **Try copying the job description text instead and use the 'Text/Paste' option above.**")
    
    else:  # Manual Entry
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Job Title")
            company = st.text_input("Company Name")
            location = st.text_input("Location")
        
        with col2:
            requirements = st.text_area("Key Requirements (one per line)")
            skills = st.text_area("Required Skills (one per line)")
        
        description = st.text_area("Job Description", height=150)
        
        if st.button("💾 Save Job Information") and title and company and description:
            job_desc = JobDescription(
                title=title,
                company=company,
                description=description,
                requirements=[req.strip() for req in requirements.split('\n') if req.strip()],
                skills=[skill.strip() for skill in skills.split('\n') if skill.strip()],
                location=location if location else None
            )
            st.session_state.job_description = job_desc
            st.success("✅ Job information saved!")
    
    # User Preferences
    if st.session_state.job_description:
        st.subheader("💭 Tell Us About Your Interest")
        
        job_desc = st.session_state.job_description
        
        col1, col2 = st.columns(2)
        
        with col1:
            interest_level = st.slider(
                "Interest Level (1-10)",
                min_value=1, max_value=10, value=7
            )
            
            motivation = st.text_area(
                "What excites you most about this opportunity?",
                height=100
            )
            
            relevant_experience = st.text_area(
                "Most relevant experience for this role:",
                height=100
            )
        
        with col2:
            career_goals = st.text_area(
                "How does this role fit your career goals?",
                height=100
            )
            
            company_knowledge = st.text_area(
                f"What do you know about {job_desc.company}?",
                height=100
            )
            
            concerns = st.text_area(
                "Any concerns about the role? (optional)",
                height=80
            )
        
        if st.button("🚀 Generate Application Materials", type="primary"):
            if not all([motivation, relevant_experience, career_goals, company_knowledge]):
                st.error("Please fill in all required fields.")
                return
            
            user_prefs = UserPreferences(
                job_interest_level=interest_level,
                motivation=motivation,
                relevant_experience=relevant_experience,
                career_goals=career_goals,
                company_knowledge=company_knowledge,
                concerns=concerns if concerns else None
            )
            
            # Generate application materials
            with st.spinner("🤖 Generating your personalized application materials..."):
                try:
                    agent = StreamlitJobApplicationAgent()
                    result = agent.process_application(
                        job_description=job_desc,
                        user_profile=st.session_state.user_profile,
                        user_preferences=user_prefs
                    )
                    
                    if result.get("error"):
                        st.error(f"Error: {result['error']}")
                        return
                    
                    # Display generated documents
                    for doc in result.get("generated_documents", []):
                        st.subheader(f"📄 {doc.title}")
                        st.text_area(
                            f"{doc.document_type.replace('_', ' ').title()}",
                            value=doc.content,
                            height=300,
                            key=f"doc_{doc.document_type}"
                        )
                        
                        # Download button
                        st.download_button(
                            label=f"💾 Download {doc.document_type.replace('_', ' ').title()}",
                            data=doc.content,
                            file_name=f"{doc.document_type}_{job_desc.company}_{job_desc.title}.txt",
                            mime="text/plain"
                        )
                    
                    st.success("🎉 Application materials generated successfully!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Error generating application materials: {e}")


def interview_prep_tab():
    """Interview preparation tab."""
    st.header("🎤 Interview Preparation")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please set up your profile first in the Profile Setup tab.")
        return
    
    if not st.session_state.job_description:
        st.warning("⚠️ Please add job description first in the Job Application tab.")
        return
    
    if st.button("🎯 Generate Interview Preparation Materials", type="primary"):
        with st.spinner("🤖 Preparing your interview materials..."):
            try:
                agent = StreamlitInterviewPreparationAgent()
                result = agent.prepare_for_interview(
                    job_description=st.session_state.job_description,
                    user_profile=st.session_state.user_profile
                )
                
                if result.get("error"):
                    st.error(f"Error: {result['error']}")
                    return
                
                prep = result.get("interview_prep")
                if not prep:
                    st.error("No interview preparation materials generated.")
                    return
                
                # Display preparation materials
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🎯 Confidence Checklist")
                    st.info("Master these topics before your interview:")
                    for item in prep.confidence_checklist:
                        st.write(f"• {item}")
                    
                    st.subheader("⚙️ Technical Questions")
                    st.warning("Practice these technical questions:")
                    for q in prep.technical_questions:
                        st.write(f"• {q}")
                
                with col2:
                    st.subheader("🗣️ Behavioral Questions")
                    st.info("Use the STAR method for these questions:")
                    for q in prep.behavioral_questions:
                        st.write(f"• {q}")
                    
                    st.subheader("❓ Questions to Ask")
                    st.success("Great questions to ask the interviewer:")
                    for q in prep.questions_to_ask:
                        st.write(f"• {q}")
                
                st.success("🎉 Interview preparation complete! You've got this!")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error generating interview preparation: {e}")


if __name__ == "__main__":
    main()

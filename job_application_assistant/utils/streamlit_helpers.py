"""Streamlit helper utilities for async operations."""

import asyncio
from typing import Any, Callable, Dict
from concurrent.futures import ThreadPoolExecutor
import functools


def run_async_in_streamlit(async_func: Callable, *args, **kwargs) -> Any:
    """
    Run an async function in Streamlit environment safely.
    This avoids conflicts with Streamlit's event loop.
    """
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If there's already a running loop, use ThreadPoolExecutor
            with ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                return future.result()
        else:
            # No running loop, safe to use asyncio.run
            return asyncio.run(async_func(*args, **kwargs))
    except RuntimeError:
        # No event loop, create one
        return asyncio.run(async_func(*args, **kwargs))


class StreamlitJobApplicationAgent:
    """Synchronous wrapper for JobApplicationAgent for Streamlit."""
    
    def __init__(self):
        from job_application_assistant.agents.job_application_agent import JobApplicationAgent
        self.agent = JobApplicationAgent()
    
    def process_application(self, job_description, user_profile, user_preferences) -> Dict[str, Any]:
        """Process application synchronously for Streamlit."""
        return run_async_in_streamlit(
            self.agent.process_application,
            job_description,
            user_profile,
            user_preferences
        )


class StreamlitInterviewPreparationAgent:
    """Synchronous wrapper for InterviewPreparationAgent for Streamlit."""
    
    def __init__(self):
        from job_application_assistant.agents.interview_prep_agent import InterviewPreparationAgent
        self.agent = InterviewPreparationAgent()
    
    def prepare_for_interview(self, job_description, user_profile) -> Dict[str, Any]:
        """Prepare for interview synchronously for Streamlit."""
        return run_async_in_streamlit(
            self.agent.prepare_for_interview,
            job_description,
            user_profile
        )


def get_model_info():
    """Get information about the currently configured LLM model."""
    try:
        from job_application_assistant.core.llm import get_llm_manager
        llm_manager = get_llm_manager()
        return {
            "model": llm_manager.settings.primary_model_name,
            "base_url": llm_manager.settings.ollama_base_url,
            "is_healthy": llm_manager.settings.is_ollama_available,
            "provider": "Ollama"
        }
    except Exception as e:
        return {
            "model": "Unknown",
            "base_url": "Unknown", 
            "is_healthy": False,
            "provider": "Unknown",
            "error": str(e)
        }

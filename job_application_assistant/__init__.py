"""
Job Application Assistant

An AI-powered assistant for job applications and interview preparation.
Uses local LLMs via Ollama for privacy and cost-effectiveness.
"""

__version__ = "1.0.0"
__author__ = "Eduard Burlacu"
__email__ = "eduardburlacu5@gmail.com"
__description__ = "AI-powered job application and interview preparation assistant"

from typing import Optional

from .core.config import Settings
from .core.exceptions import JobAssistantError
from .core.logging import setup_logging

# Initialize logging
setup_logging()

# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Convenience imports for main functionality
from .agents.job_application_agent import JobApplicationAgent
from .agents.interview_prep_agent import InterviewPreparationAgent
from .core.llm import LLMManager

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    "get_settings",
    "Settings",
    "JobAssistantError",
    "JobApplicationAgent",
    "InterviewPreparationAgent",
    "LLMManager",
]

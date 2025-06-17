"""Core package for job application assistant."""

from .config import Settings
from .exceptions import JobAssistantError, LLMError, DocumentProcessingError
from .llm import LLMManager
from .logging import setup_logging

__all__ = [
    "Settings",
    "JobAssistantError",
    "LLMError", 
    "DocumentProcessingError",
    "LLMManager",
    "setup_logging",
]

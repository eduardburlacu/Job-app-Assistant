"""Custom exceptions for the job application assistant."""


class JobAssistantError(Exception):
    """Base exception for job application assistant."""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class LLMError(JobAssistantError):
    """Exception raised when LLM operations fail."""
    pass


class DocumentProcessingError(JobAssistantError):
    """Exception raised when document processing fails."""
    pass


class ConfigurationError(JobAssistantError):
    """Exception raised when configuration is invalid."""
    pass


class NetworkError(JobAssistantError):
    """Exception raised when network operations fail."""
    pass


class ValidationError(JobAssistantError):
    """Exception raised when input validation fails."""
    pass

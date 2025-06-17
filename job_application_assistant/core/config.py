"""Configuration management for Job Application Assistant."""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .exceptions import ConfigurationError
from .logging import get_logger

logger = get_logger(__name__)


class ModelConfig(BaseModel):
    """LLM model configuration."""
    
    name: str = Field(description="Model name")
    provider: str = Field(default="ollama", description="Model provider")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    timeout: int = Field(default=60, gt=0)
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Model name cannot be empty")
        return v.strip()


class Settings(BaseSettings):
    """Application settings with validation."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="JOB_ASSISTANT_",
        extra="ignore",
    )
    
    # Application metadata
    app_name: str = Field(default="Job Application Assistant")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    # Data directories
    data_dir: Path = Field(default_factory=lambda: Path.home() / ".job_assistant")
    logs_dir: Path = Field(default_factory=lambda: Path.home() / ".job_assistant" / "logs")
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".job_assistant" / "cache")
    
    # Ollama settings
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_timeout: int = Field(default=60, gt=0)
    
    # Model configurations
    primary_model_name: str = Field(default="llama3.1:8b")
    fallback_model_names: List[str] = Field(
        default=["gemma2:9b", "qwen2.5:7b"]
    )
    model_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    model_max_tokens: Optional[int] = Field(default=None)
    
    # Web interface settings
    streamlit_host: str = Field(default="localhost")
    streamlit_port: int = Field(default=8501, gt=0, le=65535)
    streamlit_theme: str = Field(default="light")
    
    # Security settings
    max_file_size_mb: int = Field(default=10, gt=0)
    allowed_file_types: List[str] = Field(
        default=[".pdf", ".docx", ".txt", ".md"]
    )
    
    # Rate limiting and performance
    max_requests_per_minute: int = Field(default=30, gt=0)
    request_timeout: int = Field(default=30, gt=0)
    
    # Content generation settings
    max_content_length: int = Field(default=5000, gt=0)
    min_content_length: int = Field(default=100, gt=0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()
        self._validate_configuration()
    
    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        try:
            for directory in [self.data_dir, self.logs_dir, self.cache_dir]:
                directory.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Ensured directory exists: {directory}")
        except Exception as e:
            raise ConfigurationError(f"Failed to create directories: {e}")
    
    def _validate_configuration(self) -> None:
        """Validate configuration settings."""
        # Validate file types
        for file_type in self.allowed_file_types:
            if not file_type.startswith('.'):
                raise ConfigurationError(f"File type must start with '.': {file_type}")
        
        # Validate content length settings
        if self.min_content_length >= self.max_content_length:
            raise ConfigurationError(
                "min_content_length must be less than max_content_length"
            )
    
    @property
    def primary_model(self) -> ModelConfig:
        """Get primary model configuration."""
        return ModelConfig(
            name=self.primary_model_name,
            provider="ollama",
            temperature=self.model_temperature,
            max_tokens=self.model_max_tokens,
            timeout=self.ollama_timeout,
        )
    
    @property
    def fallback_models(self) -> List[ModelConfig]:
        """Get fallback model configurations."""
        return [
            ModelConfig(
                name=name,
                provider="ollama",
                temperature=self.model_temperature,
                max_tokens=self.model_max_tokens,
                timeout=self.ollama_timeout,
            )
            for name in self.fallback_model_names
        ]
    
    @property
    def is_ollama_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            import requests
            response = requests.get(
                f"{self.ollama_base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Ollama availability check failed: {e}")
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models."""
        if not self.is_ollama_available:
            return []
        
        try:
            import requests
            response = requests.get(
                f"{self.ollama_base_url}/api/tags",
                timeout=self.ollama_timeout
            )
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                logger.debug(f"Available models: {models}")
                return models
        except Exception as e:
            logger.warning(f"Failed to get available models: {e}")
        
        return []
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information."""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "debug_mode": self.debug,
            "ollama_available": self.is_ollama_available,
            "ollama_url": self.ollama_base_url,
            "available_models": self.get_available_models(),
            "primary_model": self.primary_model_name,
            "fallback_models": self.fallback_model_names,
            "data_directory": str(self.data_dir),
            "logs_directory": str(self.logs_dir),
        }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

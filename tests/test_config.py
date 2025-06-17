"""Test configuration management."""

import os
import tempfile
from pathlib import Path

from job_application_assistant.core.config import get_settings, Settings


class TestSettings:
    """Test Settings configuration."""
    
    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()
        
        assert settings.app_name == "Job Application Assistant"
        assert settings.app_version == "1.0.0"
        assert settings.debug == False
        assert settings.log_level == "INFO"
        assert settings.primary_model_name == "llama3.1:8b"
        assert settings.ollama_base_url == "http://localhost:11434"
    
    def test_environment_override(self):
        """Test environment variable override."""
        # Set environment variable
        os.environ["JOB_ASSISTANT_DEBUG"] = "true"
        os.environ["JOB_ASSISTANT_LOG_LEVEL"] = "DEBUG"
        
        try:
            settings = Settings()
            assert settings.debug == True
            assert settings.log_level == "DEBUG"
        finally:
            # Clean up
            os.environ.pop("JOB_ASSISTANT_DEBUG", None)
            os.environ.pop("JOB_ASSISTANT_LOG_LEVEL", None)
    
    def test_directory_creation(self):
        """Test that directories are created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Override directory paths
            os.environ["JOB_ASSISTANT_DATA_DIR"] = str(temp_path / "data")
            os.environ["JOB_ASSISTANT_LOGS_DIR"] = str(temp_path / "logs")
            os.environ["JOB_ASSISTANT_CACHE_DIR"] = str(temp_path / "cache")
            
            try:
                settings = Settings()
                
                # Check directories were created
                assert settings.data_dir.exists()
                assert settings.logs_dir.exists()
                assert settings.cache_dir.exists()
            finally:
                # Clean up
                os.environ.pop("JOB_ASSISTANT_DATA_DIR", None)
                os.environ.pop("JOB_ASSISTANT_LOGS_DIR", None)
                os.environ.pop("JOB_ASSISTANT_CACHE_DIR", None)
    
    def test_get_settings_singleton(self):
        """Test that get_settings returns the same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2

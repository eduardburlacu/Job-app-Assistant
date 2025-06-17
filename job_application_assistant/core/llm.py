"""LLM management with fallback support and health checking."""

import asyncio
from typing import List, Optional, Dict, Any, Union
from langchain_ollama import ChatOllama
from langchain_core.language_models import BaseLanguageModel

from .config import Settings, ModelConfig
from .exceptions import LLMError
from .logging import get_logger

logger = get_logger(__name__)


class LLMManager:
    """Manages LLM instances with fallback support and health monitoring."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._primary_llm: Optional[BaseLanguageModel] = None
        self._fallback_llms: List[BaseLanguageModel] = []
        self._model_health: Dict[str, bool] = {}
        self._initialized = False
        
    async def initialize(self) -> None:
        """Initialize LLM instances asynchronously."""
        if self._initialized:
            return
            
        logger.info("Initializing LLM manager...")
        
        # Check Ollama availability
        if not self.settings.is_ollama_available:
            raise LLMError(
                "Ollama is not available. Please ensure Ollama is installed and running.",
                details="Visit https://ollama.ai/download for installation instructions"
            )
        
        # Get available models
        available_models = self.settings.get_available_models()
        logger.info(f"Available models: {available_models}")
        
        if not available_models:
            raise LLMError(
                "No models available in Ollama",
                details="Please download at least one model using 'ollama pull <model-name>'"
            )
        
        # Initialize primary model
        primary_model = self.settings.primary_model
        if primary_model.name in available_models:
            self._primary_llm = await self._create_llm(primary_model)
            if not self._primary_llm:
                logger.warning(f"Failed to initialize primary model: {primary_model.name}")
        else:
            logger.warning(f"Primary model {primary_model.name} not available")
        
        # Initialize fallback models
        for model_config in self.settings.fallback_models:
            if model_config.name in available_models:
                fallback_llm = await self._create_llm(model_config)
                if fallback_llm:
                    self._fallback_llms.append(fallback_llm)
        
        logger.info(f"Initialized {len(self._fallback_llms)} fallback models")
        
        # Ensure we have at least one working model
        if not self._primary_llm and not self._fallback_llms:
            raise LLMError(
                "No working LLM models available",
                details="Please check your Ollama installation and model downloads"
            )
        
        self._initialized = True
        logger.info("LLM manager initialization complete")
    
    async def _create_llm(self, model_config: ModelConfig) -> Optional[BaseLanguageModel]:
        """Create LLM instance from configuration."""
        try:
            if model_config.provider == "ollama":
                llm = ChatOllama(
                    model=model_config.name,
                    base_url=self.settings.ollama_base_url,
                    temperature=model_config.temperature,
                    timeout=model_config.timeout,
                )
                
                # Test the model
                if await self._test_model(llm, model_config.name):
                    self._model_health[model_config.name] = True
                    logger.info(f"Successfully initialized model: {model_config.name}")
                    return llm
                else:
                    self._model_health[model_config.name] = False
                    logger.warning(f"Model failed health check: {model_config.name}")
                    
        except Exception as e:
            logger.error(f"Failed to create LLM {model_config.name}: {e}")
            self._model_health[model_config.name] = False
        
        return None
    
    async def _test_model(self, llm: BaseLanguageModel, model_name: str) -> bool:
        """Test if model is working."""
        try:
            # Simple test prompt
            test_prompt = "Respond with exactly 'OK' if you understand this message."
            response = await llm.ainvoke(test_prompt)
            
            # Handle different response types
            response_text = ""
            if hasattr(response, 'content'):
                response_text = response.content
            elif isinstance(response, str):
                response_text = response
            else:
                response_text = str(response)
            
            success = "ok" in response_text.lower()
            if success:
                logger.debug(f"Model {model_name} passed health check")
            else:
                logger.warning(f"Model {model_name} unexpected response: {response_text}")
            
            return success
            
        except Exception as e:
            logger.warning(f"Model {model_name} failed health check: {e}")
            return False
    
    def get_llm(self) -> BaseLanguageModel:
        """Get working LLM instance with fallback."""
        if not self._initialized:
            raise LLMError("LLM manager not initialized. Call initialize() first.")
        
        # Try primary model first
        primary_model_name = self.settings.primary_model.name
        if (self._primary_llm and 
            self._model_health.get(primary_model_name, False)):
            logger.debug(f"Using primary model: {primary_model_name}")
            return self._primary_llm
        
        # Try fallback models
        for llm in self._fallback_llms:
            model_name = getattr(llm, 'model', 'unknown')
            if self._model_health.get(model_name, False):
                logger.info(f"Using fallback model: {model_name}")
                return llm
        
        # If we get here, no models are working
        raise LLMError(
            "No working LLM models available",
            details="All configured models failed health checks"
        )
    
    async def get_llm_async(self) -> BaseLanguageModel:
        """Get working LLM instance asynchronously."""
        if not self._initialized:
            await self.initialize()
        return self.get_llm()
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all models."""
        health_status = {}
        
        # Check primary model
        if self._primary_llm:
            primary_name = self.settings.primary_model.name
            health_status[primary_name] = await self._test_model(
                self._primary_llm, primary_name
            )
            self._model_health[primary_name] = health_status[primary_name]
        
        # Check fallback models
        for llm in self._fallback_llms:
            model_name = getattr(llm, 'model', 'unknown')
            health_status[model_name] = await self._test_model(llm, model_name)
            self._model_health[model_name] = health_status[model_name]
        
        return {
            "models": health_status,
            "healthy_count": sum(health_status.values()),
            "total_count": len(health_status),
            "ollama_available": self.settings.is_ollama_available,
        }
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get status of all models."""
        return {
            "initialized": self._initialized,
            "ollama_available": self.settings.is_ollama_available,
            "available_models": self.settings.get_available_models(),
            "model_health": self._model_health.copy(),
            "primary_model": self.settings.primary_model.name,
            "fallback_models": [m.name for m in self.settings.fallback_models],
            "has_working_model": any(self._model_health.values()),
        }


# Global LLM manager instance
_llm_manager: Optional[LLMManager] = None


def get_llm_manager() -> LLMManager:
    """Get global LLM manager instance."""
    global _llm_manager
    if _llm_manager is None:
        from . import Settings
        _llm_manager = LLMManager(Settings())
    return _llm_manager


def get_llm() -> BaseLanguageModel:
    """Get LLM instance (convenience function)."""
    return get_llm_manager().get_llm()


async def get_llm_async() -> BaseLanguageModel:
    """Get LLM instance asynchronously (convenience function)."""
    return await get_llm_manager().get_llm_async()

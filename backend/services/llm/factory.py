"""
Factory pattern implementation for LLM providers.

This module implements the factory pattern for creating and managing LLM provider instances,
providing a centralized way to instantiate providers based on configuration.
"""

from typing import Dict, Optional, Type, Any
from functools import lru_cache

from .base import LLMProvider, LLMProviderError
from .config import (
    LLMConfig, 
    LLMProviderType, 
    get_llm_config,
    BaseProviderConfig
)
from .providers import MockProvider




class LLMFactory:
    """
    Factory class for creating and managing LLM provider instances.
    
    The factory uses the registry pattern to allow for easy extension with new providers.
    """
    
    # Registry of available provider classes
    _provider_registry: Dict[LLMProviderType, Type[LLMProvider]] = {
        LLMProviderType.MOCK: MockProvider
    }
    
    
    @classmethod
    def register_provider(cls, provider_type: LLMProviderType, provider_class: Type[LLMProvider]) -> None:
        """
        Register a new provider class with the factory.
        
        Args:
            provider_type: The provider type enum
            provider_class: The provider class to register
        """
        cls._provider_registry[provider_type] = provider_class
    
    @classmethod
    def get_registered_providers(cls) -> Dict[LLMProviderType, Type[LLMProvider]]:
        """Get all registered provider types and their classes."""
        return cls._provider_registry.copy()
    
    @classmethod
    def create_provider(cls, provider_type: LLMProviderType, config: Optional[LLMConfig] = None) -> LLMProvider:
        """
        Create a provider instance of the specified type.
        
        Args:
            provider_type: The type of provider to create
            config: Optional LLM configuration (uses global config if not provided)
            
        Returns:
            LLMProvider instance
            
        Raises:
            LLMProviderError: If the provider cannot be created
        """
        if config is None:
            config = get_llm_config()
        
        # Check if provider type is registered
        if provider_type not in cls._provider_registry:
            available = list(cls._provider_registry.keys())
            raise LLMProviderError(
                f"Provider type '{provider_type}' is not registered. Available: {available}",
                provider_type.value
            )
        
        # Get provider configuration
        provider_config = config.get_provider_config(provider_type)
        if provider_config is None:
            raise LLMProviderError(
                f"No configuration found for provider type '{provider_type}'",
                provider_type.value
            )
        
        # Check if provider is enabled
        if not provider_config.enabled:
            raise LLMProviderError(
                f"Provider '{provider_type}' is disabled in configuration",
                provider_type.value
            )
        
        # Create new provider instance
        try:
            provider_class = cls._provider_registry[provider_type]
            provider_instance = provider_class(provider_config)
            
            return provider_instance
            
        except Exception as e:
            raise LLMProviderError(
                f"Failed to create provider '{provider_type}': {str(e)}",
                provider_type.value,
                original_error=e
            )
    
    @classmethod
    def get_default_provider(cls, config: Optional[LLMConfig] = None) -> LLMProvider:
        """
        Get the default provider instance based on configuration.
        
        Args:
            config: Optional LLM configuration (uses global config if not provided)
            
        Returns:
            Default LLMProvider instance
            
        Raises:
            LLMProviderError: If no default provider can be created
        """
        if config is None:
            config = get_llm_config()
        
        return cls.create_provider(config.default_provider, config)
    
    @classmethod
    async def get_available_provider(cls, config: Optional[LLMConfig] = None) -> LLMProvider:
        """
        Get the first available (healthy) provider from the configuration.
        
        This method tries the default provider first, then falls back to the 
        configured fallback providers in order.
        
        Args:
            config: Optional LLM configuration (uses global config if not provided)
            
        Returns:
            First available LLMProvider instance
            
        Raises:
            LLMProviderError: If no providers are available
        """
        if config is None:
            config = get_llm_config()
        
        # Try default provider first
        providers_to_try = [config.default_provider] + config.fallback_providers
        
        # Remove duplicates while preserving order
        seen = set()
        unique_providers = []
        for provider_type in providers_to_try:
            if provider_type not in seen:
                seen.add(provider_type)
                unique_providers.append(provider_type)
        
        for provider_type in unique_providers:
            try:
                provider = cls.create_provider(provider_type, config)
                
                # Check if provider is healthy
                if await provider.health_check():
                    return provider
                else:
                    pass
            except LLMProviderError as e:
                continue
        
        # No providers available
        available_types = [p.value for p in unique_providers]
        raise LLMProviderError(
            f"No healthy providers available. Tried: {available_types}",
            "factory"
        )
    
    @classmethod
    def get_registry_info(cls) -> Dict[str, Any]:
        """Get information about the provider registry."""
        return {
            "registered_types": [p.value for p in cls._provider_registry.keys()]
        }


# Global factory instance
_llm_factory = LLMFactory()


def get_llm_factory() -> LLMFactory:
    """Get the global LLM factory instance."""
    return _llm_factory


# Convenience functions for common operations
@lru_cache(maxsize=1)
def get_default_provider() -> LLMProvider:
    """Get the default provider (cached)."""
    return _llm_factory.get_default_provider()


async def get_available_provider() -> LLMProvider:
    """Get the first available provider."""
    return await _llm_factory.get_available_provider()


def create_provider(provider_type: LLMProviderType, config: Optional[LLMConfig] = None) -> LLMProvider:
    """Create a specific provider instance."""
    return _llm_factory.create_provider(provider_type, config)


def register_provider(provider_type: LLMProviderType, provider_class: Type[LLMProvider]) -> None:
    """Register a new provider type."""
    _llm_factory.register_provider(provider_type, provider_class)
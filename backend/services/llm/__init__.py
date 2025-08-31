"""
LLM service package for the Interview Trainer application.

This package provides a model-agnostic LLM service architecture that supports
multiple LLM providers (OpenAI, Anthropic, local models, mock) with a unified interface.

Key components:
- base: Abstract interfaces and response models
- config: Configuration management with environment variable support
- factory: Factory pattern for provider instantiation and management
- providers: Concrete provider implementations

Usage:
    from services.llm import get_available_provider, JobAnalysis
    
    # Get the first available provider
    provider = await get_available_provider()
    
    # Analyze a job description
    response = await provider.analyze_job(job_description)
    if response.success:
        analysis = JobAnalysis(**response.data)
        print(f"Found {len(analysis.technical_skills)} technical skills")
"""

from .base import (
    LLMProvider,
    LLMResponse, 
    JobAnalysis,
    ExtractedSkill,
    LLMProviderError,
    RateLimitError,
    AuthenticationError,
    InvalidRequestError
)

from .config import (
    LLMConfig,
    LLMProviderType,
    BaseProviderConfig,
    OpenAIConfig,
    AnthropicConfig,
    LocalModelConfig,
    MockConfig,
    get_llm_config,
    set_llm_config,
    load_config_from_env
)

from .factory import (
    LLMFactory,
    get_llm_factory,
    get_default_provider,
    get_available_provider,
    create_provider,
    register_provider
)

from .providers import MockProvider

__all__ = [
    # Base classes and models
    "LLMProvider",
    "LLMResponse", 
    "JobAnalysis",
    "ExtractedSkill",
    
    # Exceptions
    "LLMProviderError",
    "RateLimitError", 
    "AuthenticationError",
    "InvalidRequestError",
    
    # Configuration
    "LLMConfig",
    "LLMProviderType",
    "BaseProviderConfig",
    "OpenAIConfig",
    "AnthropicConfig", 
    "LocalModelConfig",
    "MockConfig",
    "get_llm_config",
    "set_llm_config",
    "load_config_from_env",
    
    # Factory
    "LLMFactory",
    "get_llm_factory",
    "get_default_provider",
    "get_available_provider", 
    "create_provider",
    "register_provider",
    
    # Providers
    "MockProvider"
]
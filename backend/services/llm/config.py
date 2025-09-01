"""
Configuration models for LLM providers in the Interview Trainer application.

This module defines Pydantic models for configuring different LLM providers
and managing environment-based configuration settings.
"""

import os
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, validator
from enum import Enum


class LLMProviderType(str, Enum):
    """Supported LLM provider types"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    MOCK = "mock"


class BaseProviderConfig(BaseModel):
    """Base configuration for all LLM providers"""
    provider_type: LLMProviderType = Field(..., description="Type of LLM provider")
    enabled: bool = Field(True, description="Whether this provider is enabled")
    timeout_seconds: int = Field(30, description="Request timeout in seconds")
    max_retries: int = Field(3, description="Maximum number of retries")
    retry_delay_seconds: float = Field(1.0, description="Delay between retries")


class OpenAIConfig(BaseProviderConfig):
    """Configuration for OpenAI provider"""
    provider_type: Literal[LLMProviderType.OPENAI] = LLMProviderType.OPENAI
    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field("gpt-3.5-turbo", description="OpenAI model to use")
    base_url: Optional[str] = Field(None, description="Custom base URL for API")
    organization: Optional[str] = Field(None, description="OpenAI organization ID")
    max_tokens: int = Field(2000, description="Maximum tokens per request")
    temperature: float = Field(0.7, description="Sampling temperature")
    
    @validator("api_key")
    def validate_api_key(cls, v):
        if not v or not v.startswith("sk-"):
            raise ValueError("OpenAI API key must start with 'sk-'")
        return v
    
    @validator("temperature")
    def validate_temperature(cls, v):
        if not 0 <= v <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        return v


class AnthropicConfig(BaseProviderConfig):
    """Configuration for Anthropic provider"""
    provider_type: Literal[LLMProviderType.ANTHROPIC] = LLMProviderType.ANTHROPIC
    api_key: str = Field(..., description="Anthropic API key")
    model: str = Field("claude-3-haiku-20240307", description="Anthropic model to use")
    base_url: Optional[str] = Field(None, description="Custom base URL for API")
    max_tokens: int = Field(2000, description="Maximum tokens per request")
    temperature: float = Field(0.7, description="Sampling temperature")
    
    @validator("api_key")
    def validate_api_key(cls, v):
        if not v or len(v) < 10:
            raise ValueError("Invalid Anthropic API key format")
        return v


class LocalModelConfig(BaseProviderConfig):
    """Configuration for local model provider (Ollama, etc.)"""
    provider_type: Literal[LLMProviderType.LOCAL] = LLMProviderType.LOCAL
    base_url: str = Field("http://localhost:11434", description="Local model server URL")
    model: str = Field("llama2", description="Local model name")
    max_tokens: int = Field(2000, description="Maximum tokens per request")
    temperature: float = Field(0.7, description="Sampling temperature")
    
    @validator("base_url")
    def validate_base_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("Base URL must start with http:// or https://")
        return v


class MockConfig(BaseProviderConfig):
    """Configuration for mock provider (testing/development)"""
    provider_type: Literal[LLMProviderType.MOCK] = LLMProviderType.MOCK
    simulate_delay: bool = Field(True, description="Whether to simulate API delay")
    delay_seconds: float = Field(0.5, description="Simulated delay in seconds")
    failure_rate: float = Field(0.0, description="Simulated failure rate (0-1)")
    
    @validator("failure_rate")
    def validate_failure_rate(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Failure rate must be between 0 and 1")
        return v


class LLMConfig(BaseModel):
    """Main LLM configuration model"""
    default_provider: LLMProviderType = Field(LLMProviderType.MOCK, description="Default provider to use")
    fallback_providers: list[LLMProviderType] = Field(
        default_factory=lambda: [LLMProviderType.MOCK],
        description="Fallback providers in order of preference"
    )
    
    # Provider configurations
    openai: Optional[OpenAIConfig] = Field(None, description="OpenAI provider config")
    anthropic: Optional[AnthropicConfig] = Field(None, description="Anthropic provider config")
    local: Optional[LocalModelConfig] = Field(None, description="Local model provider config")
    mock: MockConfig = Field(default_factory=MockConfig, description="Mock provider config")
    
    # Global settings
    enable_analytics: bool = Field(True, description="Enable usage analytics")
    log_requests: bool = Field(False, description="Log all requests (disable in production)")
    
    @validator("fallback_providers")
    def validate_fallback_providers(cls, v):
        if not v:
            raise ValueError("At least one fallback provider must be specified")
        return v
    
    def get_provider_config(self, provider_type: LLMProviderType) -> Optional[BaseProviderConfig]:
        """Get configuration for a specific provider"""
        provider_configs = {
            LLMProviderType.OPENAI: self.openai,
            LLMProviderType.ANTHROPIC: self.anthropic,
            LLMProviderType.LOCAL: self.local,
            LLMProviderType.MOCK: self.mock
        }
        return provider_configs.get(provider_type)
    
    def get_enabled_providers(self) -> list[LLMProviderType]:
        """Get list of enabled providers"""
        enabled = []
        for provider_type in LLMProviderType:
            config = self.get_provider_config(provider_type)
            if config and config.enabled:
                enabled.append(provider_type)
        return enabled


def load_config_from_env() -> LLMConfig:
    """
    Load LLM configuration from environment variables.
    
    Environment variables:
    - LLM_DEFAULT_PROVIDER: Default provider (openai, anthropic, local, mock)
    - LLM_FALLBACK_PROVIDERS: Comma-separated list of fallback providers
    
    OpenAI:
    - OPENAI_API_KEY: API key
    - OPENAI_MODEL: Model name (default: gpt-3.5-turbo)
    - OPENAI_MAX_TOKENS: Max tokens (default: 2000)
    - OPENAI_TEMPERATURE: Temperature (default: 0.7)
    
    Anthropic:
    - ANTHROPIC_API_KEY: API key
    - ANTHROPIC_MODEL: Model name (default: claude-3-haiku-20240307)
    - ANTHROPIC_MAX_TOKENS: Max tokens (default: 2000)
    - ANTHROPIC_TEMPERATURE: Temperature (default: 0.7)
    
    Local:
    - LOCAL_MODEL_URL: Base URL (default: http://localhost:11434)
    - LOCAL_MODEL_NAME: Model name (default: llama2)
    - LOCAL_MAX_TOKENS: Max tokens (default: 2000)
    - LOCAL_TEMPERATURE: Temperature (default: 0.7)
    
    Mock:
    - MOCK_SIMULATE_DELAY: Whether to simulate delay (default: true)
    - MOCK_DELAY_SECONDS: Delay in seconds (default: 0.5)
    - MOCK_FAILURE_RATE: Failure rate 0-1 (default: 0.0)
    
    Returns:
        LLMConfig instance with environment-based configuration
    """
    
    # Parse default and fallback providers
    default_provider = LLMProviderType(os.getenv("LLM_DEFAULT_PROVIDER", "mock"))
    fallback_str = os.getenv("LLM_FALLBACK_PROVIDERS", "mock")
    fallback_providers = [LLMProviderType(p.strip()) for p in fallback_str.split(",")]
    
    # OpenAI configuration
    openai_config = None
    if os.getenv("OPENAI_API_KEY"):
        openai_config = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000")),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            organization=os.getenv("OPENAI_ORGANIZATION"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
    
    # Anthropic configuration
    anthropic_config = None
    if os.getenv("ANTHROPIC_API_KEY"):
        anthropic_config = AnthropicConfig(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
            max_tokens=int(os.getenv("ANTHROPIC_MAX_TOKENS", "2000")),
            temperature=float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7")),
            base_url=os.getenv("ANTHROPIC_BASE_URL")
        )
    
    # Local model configuration
    local_config = LocalModelConfig(
        base_url=os.getenv("LOCAL_MODEL_URL", "http://localhost:11434"),
        model=os.getenv("LOCAL_MODEL_NAME", "llama2"),
        max_tokens=int(os.getenv("LOCAL_MAX_TOKENS", "2000")),
        temperature=float(os.getenv("LOCAL_TEMPERATURE", "0.7"))
    )
    
    # Mock configuration
    mock_config = MockConfig(
        simulate_delay=os.getenv("MOCK_SIMULATE_DELAY", "true").lower() == "true",
        delay_seconds=float(os.getenv("MOCK_DELAY_SECONDS", "0.5")),
        failure_rate=float(os.getenv("MOCK_FAILURE_RATE", "0.0"))
    )
    
    # Global settings
    enable_caching = os.getenv("LLM_ENABLE_CACHING", "true").lower() == "true"
    enable_analytics = os.getenv("LLM_ENABLE_ANALYTICS", "true").lower() == "true"
    log_requests = os.getenv("LLM_LOG_REQUESTS", "false").lower() == "true"
    
    return LLMConfig(
        default_provider=default_provider,
        fallback_providers=fallback_providers,
        openai=openai_config,
        anthropic=anthropic_config,
        local=local_config,
        mock=mock_config,
        enable_caching=enable_caching,
        enable_analytics=enable_analytics,
        log_requests=log_requests
    )


# Global configuration instance
_llm_config: Optional[LLMConfig] = None


def get_llm_config() -> LLMConfig:
    """Get the global LLM configuration instance"""
    global _llm_config
    if _llm_config is None:
        _llm_config = load_config_from_env()
    return _llm_config


def set_llm_config(config: LLMConfig) -> None:
    """Set the global LLM configuration instance (useful for testing)"""
    global _llm_config
    _llm_config = config
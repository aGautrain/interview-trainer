"""
LLM provider implementations for the Interview Trainer application.

This package contains concrete implementations of LLM providers including:
- MockProvider: For development and testing
- OpenAIProvider: For OpenAI GPT models
- AnthropicProvider: For Anthropic Claude models
- LocalProvider: For local/self-hosted models
"""

from .mock_provider import MockProvider

__all__ = ["MockProvider"]
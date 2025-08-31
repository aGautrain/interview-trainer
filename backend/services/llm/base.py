"""
Base abstract interfaces for LLM providers in the Interview Trainer application.

This module defines the core abstractions that all LLM providers must implement,
ensuring consistent behavior across different LLM services (OpenAI, Anthropic, local models, etc.).
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime




class ExtractedSkill(BaseModel):
    """Represents a skill extracted from job analysis"""
    name: str = Field(..., description="Name of the skill")
    category: str = Field(..., description="Category of the skill (e.g., programming, framework)")
    importance: str = Field(..., description="Importance level (critical, important, preferred)")
    years_required: Optional[int] = Field(None, description="Years of experience required")
    context: Optional[str] = Field(None, description="Context where the skill was mentioned")


class JobAnalysis(BaseModel):
    """Comprehensive job analysis result"""
    job_title: Optional[str] = Field(None, description="Extracted job title/position")
    key_requirements: List[str] = Field(..., description="Main job requirements")
    technical_skills: List[ExtractedSkill] = Field(..., description="Technical skills required")
    soft_skills: List[ExtractedSkill] = Field(..., description="Soft skills required")
    experience_level: str = Field(..., description="Required experience level (junior, mid, senior)")
    industry: str = Field(..., description="Industry or domain")
    summary: str = Field(..., description="Brief summary of the role")
    difficulty_assessment: str = Field(..., description="Overall difficulty rating")


class LLMResponse(BaseModel):
    """Standardized response from LLM providers"""
    success: bool = Field(..., description="Whether the operation was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if operation failed")
    provider: str = Field(..., description="LLM provider that generated the response")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    tokens_used: Optional[int] = Field(None, description="Number of tokens consumed")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")


class LLMProviderError(Exception):
    """Base exception for LLM provider errors"""
    
    def __init__(self, message: str, provider: str, original_error: Optional[Exception] = None):
        self.message = message
        self.provider = provider
        self.original_error = original_error
        super().__init__(f"[{provider}] {message}")


class RateLimitError(LLMProviderError):
    """Exception raised when rate limits are exceeded"""
    pass


class AuthenticationError(LLMProviderError):
    """Exception raised for authentication failures"""
    pass


class InvalidRequestError(LLMProviderError):
    """Exception raised for invalid requests"""
    pass


class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    
    All concrete LLM provider implementations must inherit from this class
    and implement the required methods for job analysis and skill extraction.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM provider with configuration.
        
        Args:
            config: Provider-specific configuration dictionary
        """
        self.config = config
        self.provider_name = self.__class__.__name__.replace("Provider", "").lower()
    
    @abstractmethod
    async def analyze_job(self, job_description: str, company_context: Optional[str] = None) -> LLMResponse:
        """
        Analyze a job description and extract comprehensive information.
        
        Args:
            job_description: The job description text to analyze
            company_context: Optional context about the company
            
        Returns:
            LLMResponse containing JobAnalysis data
            
        Raises:
            LLMProviderError: If the analysis fails
            RateLimitError: If rate limits are exceeded
            AuthenticationError: If authentication fails
        """
        pass
    
    @abstractmethod
    async def extract_skills(self, text: str, context_type: str = "job_description") -> LLMResponse:
        """
        Extract skills from any text content.
        
        Args:
            text: The text to analyze for skills
            context_type: Type of content being analyzed (job_description, resume, etc.)
            
        Returns:
            LLMResponse containing list of ExtractedSkill objects
            
        Raises:
            LLMProviderError: If skill extraction fails
            RateLimitError: If rate limits are exceeded
            AuthenticationError: If authentication fails
        """
        pass
    
    async def health_check(self) -> bool:
        """
        Perform a health check to verify the provider is available.
        
        Returns:
            True if the provider is healthy, False otherwise
        """
        try:
            # Simple test with minimal content
            response = await self.extract_skills("Python programming", "test")
            return response.success
        except Exception as e:
            return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about this provider.
        
        Returns:
            Dictionary with provider metadata
        """
        return {
            "name": self.provider_name,
            "class": self.__class__.__name__,
            "config_keys": list(self.config.keys()) if self.config else [],
            "supports_streaming": getattr(self, "supports_streaming", False),
            "supports_function_calling": getattr(self, "supports_function_calling", False)
        }
    
    def _create_success_response(self, data: Any, tokens_used: Optional[int] = None, 
                               processing_time_ms: Optional[float] = None) -> LLMResponse:
        """
        Create a successful LLM response.
        
        Args:
            data: The response data
            tokens_used: Number of tokens consumed
            processing_time_ms: Processing time in milliseconds
            
        Returns:
            LLMResponse with success=True
        """
        return LLMResponse(
            success=True,
            data=data if isinstance(data, dict) else data.model_dump(),
            provider=self.provider_name,
            tokens_used=tokens_used,
            processing_time_ms=processing_time_ms
        )
    
    def _create_error_response(self, error: str, tokens_used: Optional[int] = None,
                             processing_time_ms: Optional[float] = None) -> LLMResponse:
        """
        Create an error LLM response.
        
        Args:
            error: Error message
            tokens_used: Number of tokens consumed
            processing_time_ms: Processing time in milliseconds
            
        Returns:
            LLMResponse with success=False
        """
        return LLMResponse(
            success=False,
            error=error,
            provider=self.provider_name,
            tokens_used=tokens_used,
            processing_time_ms=processing_time_ms
        )
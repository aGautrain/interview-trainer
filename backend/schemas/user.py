from typing import List, Optional
from pydantic import BaseModel, Field
from .base import BaseSchema


class UserSession(BaseModel):
    """User session information"""
    id: str = Field(..., description="Session identifier")
    apiKey: str = Field(..., description="API key for external services")
    model: str = Field(..., description="Preferred AI model")
    createdAt: str = Field(..., description="Session creation time")
    updatedAt: str = Field(..., description="Last update time")


class LLMConfig(BaseModel):
    """LLM configuration settings"""
    apiKey: str = Field(..., description="API key for LLM service")
    model: str = Field(..., description="LLM model name")
    temperature: float = Field(..., ge=0.0, le=2.0, description="Model temperature setting")
    maxTokens: int = Field(..., ge=1, description="Maximum tokens for responses")


class UserProfile(BaseSchema):
    """User profile information"""
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User full name")
    lastActive: str = Field(..., description="Last activity time")

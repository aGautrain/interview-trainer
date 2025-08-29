from datetime import datetime
from typing import Optional, List, Union
from enum import Enum
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema with common fields"""
    id: str = Field(..., description="Unique identifier")
    createdAt: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updatedAt: Optional[datetime] = Field(None, description="Last update timestamp")


class DifficultyLevel(str, Enum):
    """Standard difficulty levels across the application"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class QuestionType(str, Enum):
    """Standard question types across the application"""
    THEORETICAL = "theoretical"
    PRACTICAL = "practical"
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    SITUATIONAL = "situational"
    CODING = "coding"
    SYSTEM_DESIGN = "system_design"


class SkillType(str, Enum):
    """Skill type enumeration"""
    PROGRAMMING = "programming"
    FRAMEWORK = "framework"
    DATABASE = "database"
    DEVOPS = "devops"
    SOFT_SKILL = "soft_skill"
    SYSTEM_DESIGN = "system_design"
    ALGORITHMS = "algorithms"
    TESTING = "testing"
    ARCHITECTURE = "architecture"
    TOOLS = "tools"


class Skill(BaseModel):
    """Unified skill representation"""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Skill name")
    category: str = Field(..., description="Skill category")
    type: SkillType = Field(..., description="Skill type")
    proficiency: str = Field(..., description="Proficiency level")
    yearsOfExperience: Optional[int] = Field(None, description="Years of experience")


class ApiResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = Field(..., description="Operation success status")
    data: Optional[dict] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if any")
    message: Optional[str] = Field(None, description="Success message")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    data: List[dict] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    hasNext: bool = Field(..., description="Whether there's a next page")
    hasPrev: bool = Field(..., description="Whether there's a previous page")

from typing import List, Optional, Any
from pydantic import BaseModel, Field
from .base import Skill


class QuestionGenerationRequest(BaseModel):
    """Request for generating training questions"""
    skills: List[Skill] = Field(..., description="Skills to generate questions for")
    type: str = Field(..., description="Question type")
    difficulty: str = Field(..., description="Difficulty level")
    count: int = Field(..., ge=1, le=50, description="Number of questions to generate")
    context: Optional[str] = Field(None, description="Additional context for generation")


class ExerciseGenerationRequest(BaseModel):
    """Request for generating coding exercises"""
    skills: List[Skill] = Field(..., description="Skills to generate exercises for")
    language: str = Field(..., description="Programming language")
    difficulty: str = Field(..., description="Difficulty level")
    count: int = Field(..., ge=1, le=20, description="Number of exercises to generate")
    focus: Optional[str] = Field(None, description="Specific focus area")


class GenerationHistory(BaseModel):
    """History of AI generation requests"""
    id: str = Field(..., description="Generation history identifier")
    type: str = Field(..., description="Generation type (job-analysis/question-generation/exercise-generation)")
    input: Any = Field(..., description="Input data for generation")
    output: Any = Field(..., description="Generated output")
    model: str = Field(..., description="AI model used")
    tokensUsed: int = Field(..., ge=0, description="Number of tokens consumed")
    duration: float = Field(..., ge=0.0, description="Generation duration in seconds")
    createdAt: str = Field(..., description="Generation timestamp")


class QuestionForm(BaseModel):
    """Form data for question generation"""
    skills: List[str] = Field(..., description="Skill names")
    type: str = Field(..., description="Question type")
    difficulty: str = Field(..., description="Difficulty level")
    count: int = Field(..., ge=1, le=50, description="Question count")
    context: str = Field(..., description="Generation context")


class ExerciseForm(BaseModel):
    """Form data for exercise generation"""
    skills: List[str] = Field(..., description="Skill names")
    language: str = Field(..., description="Programming language")
    difficulty: str = Field(..., description="Difficulty level")
    count: int = Field(..., ge=1, le=20, description="Exercise count")
    focus: str = Field(..., description="Focus area")

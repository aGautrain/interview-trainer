"""
Job analysis schema models for the Interview Trainer application.

This module defines Pydantic models for job analysis operations including:
- Analysis requests and responses
- Training recommendations
- Skill matching and scoring
- Caching and metadata structures
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator
from .base import BaseSchema, DifficultyLevel, SkillType
from .jobs import Job


class AnalysisStatus(str, Enum):
    """Status of job analysis operations"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class SkillImportance(str, Enum):
    """Importance levels for extracted skills"""
    CRITICAL = "critical"
    IMPORTANT = "important"
    PREFERRED = "preferred"
    NICE_TO_HAVE = "nice_to_have"


class TrainingPriority(str, Enum):
    """Priority levels for training recommendations"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SkillRecommendation(BaseModel):
    """Unified skill extraction and training recommendation"""
    # Core skill information
    name: str = Field(..., description="Skill name")
    category: str = Field(..., description="Skill category (programming, framework, etc.)")
    skill_type: Optional[SkillType] = Field(None, description="Standardized skill type")
    
    # Importance and priority
    importance: SkillImportance = Field(..., description="Importance level in job context")
    priority: TrainingPriority = Field(..., description="Training priority level (derived from importance)")
    
    # Experience and context
    years_required: Optional[int] = Field(None, ge=0, le=20, description="Years of experience required")
    context: Optional[str] = Field(None, description="Context where skill was mentioned")
    
    # Training information
    recommended_actions: List[str] = Field(default_factory=list, description="Specific actions to take")
    estimated_duration: Optional[str] = Field(None, description="Estimated time commitment")
    difficulty_level: DifficultyLevel = Field(DifficultyLevel.INTERMEDIATE, description="Difficulty of training")
    prerequisite_skills: List[str] = Field(default_factory=list, description="Skills needed first")
    learning_resources: List[str] = Field(default_factory=list, description="Recommended resources")
    success_metrics: List[str] = Field(default_factory=list, description="How to measure progress")
    
    # Metadata
    synonyms: List[str] = Field(default_factory=list, description="Alternative names for this skill")
    related_skills: List[str] = Field(default_factory=list, description="Related/complementary skills")


class JobAnalysisResult(BaseModel):
    """Comprehensive job analysis result"""
    # Basic job information
    job_title: Optional[str] = Field(None, description="Analyzed job title")
    company_name: Optional[str] = Field(None, description="Company name")
    industry: str = Field(..., description="Industry or domain")
    
    # Core analysis
    key_requirements: List[str] = Field(..., description="Main job requirements")
    skill_recommendations: List[SkillRecommendation] = Field(..., description="Unified skill analysis and training recommendations")
    
    # Analysis insights
    experience_level: str = Field(..., description="Required experience level")
    difficulty_assessment: DifficultyLevel = Field(..., description="Overall role difficulty")
    role_summary: str = Field(..., description="Brief summary of the role")
    compensation_insights: Optional[str] = Field(None, description="Salary/compensation insights")
    
    # Metadata
    analysis_metadata: Dict[str, Any] = Field(default_factory=dict, description="Analysis metadata")



class JobAnalysisResponse(BaseModel):
    """Response wrapper for job analysis"""
    success: bool = Field(..., description="Whether analysis was successful")
    status: AnalysisStatus = Field(..., description="Analysis status")
    result: Optional[JobAnalysisResult] = Field(None, description="Analysis result if successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    llm_provider: Optional[str] = Field(None, description="LLM provider used for analysis")
    tokens_used: Optional[int] = Field(None, description="Tokens consumed during analysis")
    analysis_id: str = Field(..., description="Unique analysis ID for tracking")




class AnalysisMetrics(BaseModel):
    """Metrics and statistics for analysis operations"""
    total_analyses: int = Field(default=0, description="Total number of analyses performed")
    successful_analyses: int = Field(default=0, description="Number of successful analyses")
    failed_analyses: int = Field(default=0, description="Number of failed analyses")
    avg_processing_time_ms: Optional[float] = Field(None, description="Average processing time")
    total_tokens_used: int = Field(default=0, description="Total tokens consumed")
    most_analyzed_skills: List[Dict[str, Any]] = Field(default_factory=list, description="Most frequently analyzed skills")

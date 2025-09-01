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
    CACHED = "cached"


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


class JobAnalysisRequest(BaseModel):
    """Request model for job analysis"""
    job_description: str = Field(..., description="Full job description text to analyze")
    job_title: Optional[str] = Field(None, description="Job title for context")
    company_name: Optional[str] = Field(None, description="Company name for context")
    company_context: Optional[str] = Field(None, description="Additional company information")
    analysis_depth: str = Field("standard", description="Analysis depth (basic, standard, comprehensive)")
    user_id: Optional[str] = Field(None, description="User ID for personalized recommendations")
    
    @validator('analysis_depth')
    def validate_analysis_depth(cls, v):
        allowed_depths = ['basic', 'standard', 'comprehensive']
        if v not in allowed_depths:
            raise ValueError(f"Analysis depth must be one of {allowed_depths}")
        return v


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


# Backward compatibility aliases
ExtractedSkillEnhanced = SkillRecommendation
TrainingRecommendation = SkillRecommendation


class JobAnalysisResponse(BaseModel):
    """Response wrapper for job analysis"""
    success: bool = Field(..., description="Whether analysis was successful")
    status: AnalysisStatus = Field(..., description="Analysis status")
    result: Optional[JobAnalysisResult] = Field(None, description="Analysis result if successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    llm_provider: Optional[str] = Field(None, description="LLM provider used for analysis")
    tokens_used: Optional[int] = Field(None, description="Tokens consumed during analysis")
    cache_hit: bool = Field(False, description="Whether result came from cache")
    analysis_id: str = Field(..., description="Unique analysis ID for tracking")


class JobAnalysisCache(BaseSchema):
    """Cache entry for job analysis results"""
    job_description_hash: str = Field(..., description="Hash of job description for cache key")
    analysis_request: JobAnalysisRequest = Field(..., description="Original analysis request")
    analysis_result: JobAnalysisResult = Field(..., description="Cached analysis result")
    llm_provider: str = Field(..., description="LLM provider used")
    tokens_used: Optional[int] = Field(None, description="Tokens used for analysis")
    expires_at: datetime = Field(..., description="Cache expiration timestamp")
    hit_count: int = Field(default=0, description="Number of times cache was accessed")
    last_accessed: Optional[datetime] = Field(None, description="Last access timestamp")


class AnalysisMetrics(BaseModel):
    """Metrics and statistics for analysis operations"""
    total_analyses: int = Field(default=0, description="Total number of analyses performed")
    successful_analyses: int = Field(default=0, description="Number of successful analyses")
    failed_analyses: int = Field(default=0, description="Number of failed analyses")
    cache_hits: int = Field(default=0, description="Number of cache hits")
    cache_misses: int = Field(default=0, description="Number of cache misses")
    avg_processing_time_ms: Optional[float] = Field(None, description="Average processing time")
    total_tokens_used: int = Field(default=0, description="Total tokens consumed")
    most_analyzed_skills: List[Dict[str, Any]] = Field(default_factory=list, description="Most frequently analyzed skills")


class BulkJobAnalysisRequest(BaseModel):
    """Request for analyzing multiple jobs at once"""
    job_descriptions: List[str] = Field(..., min_items=1, max_items=50, description="Job descriptions to analyze")
    analysis_depth: str = Field("standard", description="Analysis depth for all jobs")
    user_id: Optional[str] = Field(None, description="User ID for personalized recommendations")
    batch_id: Optional[str] = Field(None, description="Optional batch ID for tracking")
    
    @validator('job_descriptions')
    def validate_job_descriptions(cls, v):
        if not v:
            raise ValueError("At least one job description is required")
        for desc in v:
            if not desc.strip():
                raise ValueError("Job descriptions cannot be empty")
        return v


class BulkJobAnalysisResponse(BaseModel):
    """Response for bulk job analysis"""
    success: bool = Field(..., description="Whether bulk analysis was successful")
    batch_id: str = Field(..., description="Batch ID for tracking")
    total_jobs: int = Field(..., description="Total number of jobs processed")
    successful_analyses: int = Field(..., description="Number of successful analyses")
    failed_analyses: int = Field(..., description="Number of failed analyses")
    results: List[JobAnalysisResponse] = Field(..., description="Individual analysis results")
    processing_time_ms: float = Field(..., description="Total processing time")
    total_tokens_used: Optional[int] = Field(None, description="Total tokens consumed")
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


class ExtractedSkillEnhanced(BaseModel):
    """Enhanced extracted skill with additional metadata"""
    name: str = Field(..., description="Skill name")
    category: str = Field(..., description="Skill category (programming, framework, etc.)")
    skill_type: Optional[SkillType] = Field(None, description="Standardized skill type")
    importance: SkillImportance = Field(..., description="Importance level in job context")
    years_required: Optional[int] = Field(None, ge=0, le=20, description="Years of experience required")
    context: Optional[str] = Field(None, description="Context where skill was mentioned")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in skill extraction")
    synonyms: List[str] = Field(default_factory=list, description="Alternative names for this skill")
    related_skills: List[str] = Field(default_factory=list, description="Related/complementary skills")


class SkillMatch(BaseModel):
    """Represents a match between extracted and existing skills"""
    extracted_skill: ExtractedSkillEnhanced = Field(..., description="The extracted skill")
    matched_skill_id: Optional[str] = Field(None, description="ID of matched skill in database")
    matched_skill_name: Optional[str] = Field(None, description="Name of matched skill")
    match_confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the match")
    match_type: str = Field(..., description="Type of match (exact, synonym, partial, semantic)")
    is_new_skill: bool = Field(False, description="Whether this is a new skill not in database")


class SkillGapAnalysis(BaseModel):
    """Analysis of skill gaps for a user"""
    skill_name: str = Field(..., description="Name of the skill")
    required_level: str = Field(..., description="Required proficiency level")
    current_level: Optional[str] = Field(None, description="User's current level")
    gap_severity: TrainingPriority = Field(..., description="How critical this gap is")
    estimated_study_time: Optional[int] = Field(None, ge=0, description="Estimated hours to bridge gap")


class TrainingRecommendation(BaseModel):
    """Training recommendation based on job analysis"""
    skill_name: str = Field(..., description="Skill to focus on")
    skill_category: str = Field(..., description="Category of the skill")
    priority: TrainingPriority = Field(..., description="Training priority level")
    recommended_actions: List[str] = Field(..., description="Specific actions to take")
    estimated_duration: Optional[str] = Field(None, description="Estimated time commitment")
    difficulty_level: DifficultyLevel = Field(..., description="Difficulty of training")
    prerequisite_skills: List[str] = Field(default_factory=list, description="Skills needed first")
    learning_resources: List[str] = Field(default_factory=list, description="Recommended resources")
    success_metrics: List[str] = Field(default_factory=list, description="How to measure progress")


class JobAnalysisResult(BaseModel):
    """Comprehensive job analysis result"""
    # Basic job information
    job_title: Optional[str] = Field(None, description="Analyzed job title")
    company_name: Optional[str] = Field(None, description="Company name")
    industry: str = Field(..., description="Industry or domain")
    
    # Core analysis
    key_requirements: List[str] = Field(..., description="Main job requirements")
    extracted_skills: List[ExtractedSkillEnhanced] = Field(..., description="All extracted skills")
    skill_matches: List[SkillMatch] = Field(..., description="Matched skills with database")
    
    # Analysis insights
    experience_level: str = Field(..., description="Required experience level")
    difficulty_assessment: DifficultyLevel = Field(..., description="Overall role difficulty")
    role_summary: str = Field(..., description="Brief summary of the role")
    compensation_insights: Optional[str] = Field(None, description="Salary/compensation insights")
    
    # Recommendations
    training_recommendations: List[TrainingRecommendation] = Field(..., description="Training suggestions")
    skill_gaps: List[SkillGapAnalysis] = Field(default_factory=list, description="Identified skill gaps")
    readiness_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Overall readiness for role")
    
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
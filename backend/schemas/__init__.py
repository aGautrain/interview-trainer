# Schemas package for Interview Trainer backend

# Base schemas
from .base import (
    BaseSchema, 
    Skill, 
    ApiResponse, 
    PaginatedResponse,
    DifficultyLevel,
    QuestionType,
    SkillType
)

# Training schemas
from .training import (
    Question,
    Exercise,
    TestCase,
    SkillCard,
    SkillTrainingProgress,
    SkillTrainingSession,
    SkillTrainingData
)

# Job schemas
from .jobs import (
    Job,
    JobAnalysisResult,
    JobAnalysisForm
)

# Dashboard schemas
from .dashboard import (
    DashboardStats,
    SkillDistributionData,
    PerformanceData,
    DashboardData
)

# User schemas
from .user import (
    UserSession,
    LLMConfig,
    UserProfile
)

# AI generation schemas
from .ai_generation import (
    QuestionGenerationRequest,
    ExerciseGenerationRequest,
    GenerationHistory,
    QuestionForm,
    ExerciseForm
)

__all__ = [
    # Base
    "BaseSchema",
    "Skill",
    "ApiResponse",
    "PaginatedResponse",
    "DifficultyLevel",
    "QuestionType",
    "SkillType",
    
    # Training
    "Question",
    "Exercise",
    "TestCase",
    "SkillCard",
    "SkillTrainingProgress",
    "SkillTrainingSession",
    "SkillTrainingData",
    
    # Jobs
    "Job",
    "JobAnalysisResult",
    "JobAnalysisForm",
    
    # Dashboard
    "DashboardStats",
    "SkillDistributionData",
    "PerformanceData",
    "DashboardData",
    
    # User
    "UserSession",
    "LLMConfig",
    "UserProfile",
    
    # AI generation
    "QuestionGenerationRequest",
    "ExerciseGenerationRequest",
    "GenerationHistory",
    "QuestionForm",
    "ExerciseForm",
]

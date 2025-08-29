from typing import List
from pydantic import BaseModel, Field
from .jobs import Job


class DashboardStats(BaseModel):
    """Dashboard statistics"""
    activeJobs: int = Field(..., ge=0, description="Number of active job applications")
    questionsCompleted: int = Field(..., ge=0, description="Total questions completed")
    avgProgress: int = Field(..., ge=0, le=100, description="Average progress across all jobs")
    successRate: int = Field(..., ge=0, le=100, description="Success rate percentage")


class SkillDistributionData(BaseModel):
    """Skill distribution chart data"""
    name: str = Field(..., description="Skill category name")
    value: int = Field(..., ge=0, description="Percentage value")
    color: str = Field(..., description="Chart color hex code")


class PerformanceData(BaseModel):
    """Performance metrics by difficulty"""
    difficulty: str = Field(..., description="Difficulty level")
    success: int = Field(..., ge=0, description="Number of successful attempts")
    failure: int = Field(..., ge=0, description="Number of failed attempts")


class DashboardData(BaseModel):
    """Complete dashboard data"""
    stats: DashboardStats
    jobs: List[Job]
    skillDistributionData: List[SkillDistributionData]
    performanceData: List[PerformanceData]

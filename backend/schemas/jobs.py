from typing import List, Optional
from pydantic import BaseModel, Field
from .base import BaseSchema, Skill


class Job(BaseModel):
    """Unified job posting schema"""
    id: str = Field(..., description="Unique identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    description: str = Field(..., description="Job description")
    requirements: List[str] = Field(..., description="Job requirements")
    skills: List[str] = Field(..., description="Required skills")
    techStack: List[str] = Field(..., description="Required technologies")
    location: str = Field(..., description="Job location")
    type: str = Field(..., description="Employment type")
    level: str = Field(..., description="Experience level")
    salaryRange: Optional[str] = Field(None, description="Salary range")
    isRemote: bool = Field(False, description="Whether the job is remote")
    progress: Optional[int] = Field(None, ge=0, le=100, description="Application progress percentage")
    createdAt: str = Field(..., description="Creation date")
    updatedAt: str = Field(..., description="Last update date")


class JobAnalysisResult(BaseModel):
    """Result of job posting analysis"""
    skills: List[Skill] = Field(..., description="Identified skills from job posting")
    requirements: List[str] = Field(..., description="Extracted requirements")
    summary: str = Field(..., description="Job analysis summary")
    difficulty: str = Field(..., description="Estimated difficulty level (beginner/intermediate/advanced)")
    estimatedExperience: str = Field(..., description="Estimated years of experience needed")
    recommendations: List[str] = Field(..., description="Training recommendations")


class JobAnalysisForm(BaseModel):
    """Form data for job analysis"""
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    description: str = Field(..., description="Job description")
    requirements: str = Field(..., description="Job requirements")

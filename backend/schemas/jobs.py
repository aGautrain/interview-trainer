from typing import List, Optional, TYPE_CHECKING, Any
from pydantic import BaseModel, Field
from .base import BaseSchema, Skill

if TYPE_CHECKING:
    from .job_analysis import SkillRecommendation


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


class JobWithAnalyzedSkills(BaseModel):
    """Job with populated skills from analysis"""
    id: str = Field(..., description="Unique identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    description: str = Field(..., description="Job description")
    requirements: List[str] = Field(..., description="Job requirements")
    skills: List[Skill] = Field(..., description="Analyzed and populated skills")
    analyzedSkills: List[Any] = Field(..., description="Detailed skill analysis")
    techStack: List[str] = Field(..., description="Required technologies")
    location: str = Field(..., description="Job location")
    type: str = Field(..., description="Employment type")
    level: str = Field(..., description="Experience level")
    salaryRange: Optional[str] = Field(None, description="Salary range")
    isRemote: bool = Field(False, description="Whether the job is remote")
    progress: Optional[int] = Field(None, ge=0, le=100, description="Application progress percentage")
    createdAt: str = Field(..., description="Creation date")
    updatedAt: str = Field(..., description="Last update date")

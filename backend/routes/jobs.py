"""
Jobs routes for the Interview Trainer API.

This module contains all job-related endpoints including:
- Job listing
- Individual job retrieval
- Job analysis integration
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from schemas import Job
from schemas.jobs import JobWithAnalyzedSkills
from schemas.base import Skill, SkillType
from schemas.job_analysis import JobAnalysisRequest, JobAnalysisResponse, SkillRecommendation
from database import fetch_all, fetch_one
from services.job_analysis import get_job_analysis_service
import uuid

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[Job])
async def get_jobs():
    """Get all jobs from the database"""
    jobs_data = await fetch_all("SELECT * FROM jobs ORDER BY created_at DESC")
    
    return [Job(
        id=str(job['id']),
        title=job['title'],
        company=job['company'],
        description=job['description'],
        requirements=job['requirements'],
        skills=job['skills'],
        techStack=job['tech_stack'],
        location=job['location'],
        type=job['type'],
        level=job['level'],
        salaryRange=job['salary_range'],
        isRemote=job['is_remote'],
        progress=job['progress'],
        createdAt=job['created_at'].isoformat() + 'Z',
        updatedAt=job['updated_at'].isoformat() + 'Z'
    ) for job in jobs_data]


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """Get a specific job by ID from the database"""
    try:
        # Validate UUID format
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    
    job_data = await fetch_one("SELECT * FROM jobs WHERE id = $1", job_uuid)
    
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return Job(
        id=str(job_data['id']),
        title=job_data['title'],
        company=job_data['company'],
        description=job_data['description'],
        requirements=job_data['requirements'],
        skills=job_data['skills'],
        techStack=job_data['tech_stack'],
        location=job_data['location'],
        type=job_data['type'],
        level=job_data['level'],
        salaryRange=job_data['salary_range'],
        isRemote=job_data['is_remote'],
        progress=job_data['progress'],
        createdAt=job_data['created_at'].isoformat() + 'Z',
        updatedAt=job_data['updated_at'].isoformat() + 'Z'
    )


@router.post("/{job_id}/analyze", response_model=JobAnalysisResponse)
async def analyze_job(
    job_id: str,
    user_id: Optional[str] = Query(None, description="User ID for personalized analysis"),
    analysis_depth: str = Query("standard", description="Analysis depth (basic, standard, comprehensive)")
):
    """
    Analyze a specific job from the database using the job analysis service.
    
    This endpoint integrates the job analysis service with existing job data,
    providing comprehensive analysis including skill extraction, training recommendations,
    and personalized skill gap analysis if a user ID is provided.
    """
    try:
        # Validate UUID format
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    
    # Get job from database
    job_data = await fetch_one("SELECT * FROM jobs WHERE id = $1", job_uuid)
    
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # Create analysis request
        analysis_request = JobAnalysisRequest(
            job_description=job_data['description'],
            job_title=job_data['title'],
            company_name=job_data['company'],
            analysis_depth=analysis_depth,
            user_id=user_id
        )
        
        # Get analysis service and perform analysis
        service = await get_job_analysis_service()
        analysis_response = await service.analyze_job_description(analysis_request)
        
        return analysis_response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Job analysis failed: {str(e)}"
        )


@router.get("/{job_id}/with-skills", response_model=JobWithAnalyzedSkills)
async def get_job_with_skills(
    job_id: str,
    user_id: Optional[str] = Query(None, description="User ID for personalized analysis"),
    analysis_depth: str = Query("standard", description="Analysis depth (basic, standard, comprehensive)")
):
    """
    Get a job with populated skills from analysis.
    
    This endpoint combines job retrieval with skill analysis, returning a job
    with enriched skill information including detailed skill recommendations,
    training priorities, and personalized suggestions.
    """
    try:
        # Validate UUID format
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    
    # Get job from database
    job_data = await fetch_one("SELECT * FROM jobs WHERE id = $1", job_uuid)
    
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # Create analysis request
        analysis_request = JobAnalysisRequest(
            job_description=job_data['description'],
            job_title=job_data['title'],
            company_name=job_data['company'],
            analysis_depth=analysis_depth,
            user_id=user_id
        )
        
        # Get analysis service and perform analysis
        service = await get_job_analysis_service()
        analysis_response = await service.analyze_job_description(analysis_request)
        
        if not analysis_response.success or not analysis_response.result:
            raise HTTPException(
                status_code=500,
                detail=f"Job analysis failed: {analysis_response.error_message}"
            )
        
        # Convert skill recommendations to Skill objects for the skills field
        analyzed_skills = []
        for skill_rec in analysis_response.result.skill_recommendations:
            skill = Skill(
                id=f"skill_{uuid.uuid4().hex[:8]}",
                name=skill_rec.name,
                category=skill_rec.category,
                type=skill_rec.skill_type or SkillType.SOFT_SKILL,
                proficiency=skill_rec.importance.value,
                yearsOfExperience=skill_rec.years_required
            )
            analyzed_skills.append(skill)
        
        # Create the job with analyzed skills
        job_with_skills = JobWithAnalyzedSkills(
            id=str(job_data['id']),
            title=job_data['title'],
            company=job_data['company'],
            description=job_data['description'],
            requirements=job_data['requirements'],
            skills=analyzed_skills,
            analyzedSkills=analysis_response.result.skill_recommendations,
            techStack=job_data['tech_stack'],
            location=job_data['location'],
            type=job_data['type'],
            level=job_data['level'],
            salaryRange=job_data['salary_range'],
            isRemote=job_data['is_remote'],
            progress=job_data['progress'],
            createdAt=job_data['created_at'].isoformat() + 'Z',
            updatedAt=job_data['updated_at'].isoformat() + 'Z'
        )
        
        return job_with_skills
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get job with skills: {str(e)}"
        )

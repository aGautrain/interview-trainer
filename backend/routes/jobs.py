"""
Jobs routes for the Interview Trainer API.

This module contains all job-related endpoints including:
- Job listing
- Individual job retrieval
- Job analysis integration
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from schemas import Job
from schemas.jobs import JobCreateRequest, JobWithAnalyzedSkills
from schemas.base import Skill, SkillType
from schemas.job_analysis import JobAnalysisResponse
from database import fetch_all, fetch_one, execute_transaction, execute
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


@router.put("", response_model=JobWithAnalyzedSkills)
async def create_job(job_request: JobCreateRequest):
    """
    Create a new job with analysis and skill extraction.
    
    This endpoint:
    1. Validates the input job data
    2. Performs job analysis using the existing job analysis service
    3. Creates a new job record in the database with a generated UUID
    4. Extracts and stores skills as separate entities
    5. Returns the created job with populated analyzed skills
    
    The analysis is performed using the configured LLM provider and includes
    skill extraction, importance assessment, and training recommendations.
    """
    try:
        # Generate UUID for the new job
        job_id = uuid.uuid4()
        
        # Create analysis request
        analysis_request = JobAnalysisRequest(
            job_description=job_request.description,
        )
        
        # Get analysis service and perform analysis
        service = await get_job_analysis_service()
        analysis_response = await service.analyze_job_description(analysis_request)
        
        if not analysis_response.success or not analysis_response.result:
            raise HTTPException(
                status_code=500,
                detail=f"Job analysis failed: {analysis_response.error_message or 'Unknown error'}"
            )
        
        # Prepare database transaction queries
        queries = []
        
        # 1. Insert the job record
        insert_job_query = """
            INSERT INTO jobs (
                id, title, company, description, requirements, skills, tech_stack,
                location, type, level, salary_range, is_remote, progress
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            RETURNING *
        """
        
        # Merge analyzed skills with initial skills from request
        all_skills = list()
        for skill_rec in analysis_response.result.skill_recommendations:
            if skill_rec.name not in all_skills:
                all_skills.append(skill_rec.name)
        
        job_query_args = (
            job_id,
            job_request.description,
            all_skills,
        )
        
        queries.append((insert_job_query, *job_query_args))
        
        # Execute the job insertion first
        results = await execute_transaction(queries)
        
        # The first result should be the inserted job
        job_data = results[0]
        if not job_data:
            raise HTTPException(status_code=500, detail="Failed to create job record")
        
        # 2. Create skill entities for analyzed skills (outside the main transaction for flexibility)
        skill_queries = []
        for skill_rec in analysis_response.result.skill_recommendations:
            # Insert skill if it doesn't exist (we'll let duplicates be handled by checking first)
            insert_skill_query = """
                INSERT INTO skills (name, category, type, proficiency, years_of_experience)
                SELECT $1, $2, $3, $4, $5
                WHERE NOT EXISTS (
                    SELECT 1 FROM skills WHERE LOWER(name) = LOWER($1)
                )
                RETURNING id
            """
            
            # Map skill recommendation to database fields
            skill_proficiency = skill_rec.importance.value
            skill_type_str = skill_rec.skill_type.value if skill_rec.skill_type else 'soft_skill'
            
            skill_query_args = (
                skill_rec.name,
                skill_rec.category,
                skill_type_str,
                skill_proficiency,
                skill_rec.years_required
            )
            
            skill_queries.append((insert_skill_query, *skill_query_args))
        
        # Execute skill insertions if there are any
        if skill_queries:
            try:
                await execute_transaction(skill_queries)
            except Exception as skill_error:
                # Log skill creation errors but don't fail the job creation
                print(f"Warning: Some skills could not be created: {skill_error}")
        
        # Convert skill recommendations to Skill objects for the response
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
        
        # Create the response with analyzed skills
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
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error and return a generic error response
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create job: {str(e)}"
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

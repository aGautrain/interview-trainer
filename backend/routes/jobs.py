"""
Jobs routes for the Interview Trainer API.

This module contains all job-related endpoints including:
- Job listing
- Individual job retrieval
"""

from fastapi import APIRouter, HTTPException
from schemas import Job
from database import fetch_all, fetch_one
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

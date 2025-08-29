"""
Jobs routes for the Interview Trainer API.

This module contains all job-related endpoints including:
- Job listing
- Individual job retrieval
"""

from fastapi import APIRouter, HTTPException
from schemas import Job
from sample_data import SAMPLE_JOBS

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[Job])
def get_jobs():
    """Get all jobs"""
    return SAMPLE_JOBS


@router.get("/{job_id}", response_model=Job)
def get_job(job_id: str):
    """Get a specific job by ID"""
    for job in SAMPLE_JOBS:
        if job.id == job_id:
            return job
    
    raise HTTPException(status_code=404, detail="Job not found")

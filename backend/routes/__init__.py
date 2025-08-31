"""
Routes package for the Interview Trainer API.

This package contains all the route handlers organized by domain:
- dashboard: Dashboard-related endpoints
- jobs: Job-related endpoints  
- skills: Skills and training endpoints
- job_analysis: Job analysis and LLM-powered insights
- legacy: Legacy endpoints for backward compatibility
"""

from .dashboard import router as dashboard_router
from .jobs import router as jobs_router
from .skills import router as skills_router
from .job_analysis import router as job_analysis_router

__all__ = [
    "dashboard_router",
    "jobs_router", 
    "skills_router",
    "job_analysis_router"
]

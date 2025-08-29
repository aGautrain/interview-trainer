"""
Routes package for the Interview Trainer API.

This package contains all the route handlers organized by domain:
- dashboard: Dashboard-related endpoints
- jobs: Job-related endpoints  
- skills: Skills and training endpoints
- legacy: Legacy endpoints for backward compatibility
"""

from .dashboard import router as dashboard_router
from .jobs import router as jobs_router
from .skills import router as skills_router
from .legacy import router as legacy_router

__all__ = [
    "dashboard_router",
    "jobs_router", 
    "skills_router",
    "legacy_router"
]

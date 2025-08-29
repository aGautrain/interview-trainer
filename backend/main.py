"""
Main application entry point for the Interview Trainer API.

This module initializes the FastAPI application and includes all route modules.
Routes are organized by domain in separate modules for better maintainability.
"""

from fastapi import FastAPI

# Import route modules
from routes import (
    dashboard_router,
    jobs_router,
    skills_router,
    legacy_router
)

# Create FastAPI application
app = FastAPI(
    title="Interview Trainer API",
    description="Backend API for the Interview Trainer application",
    version="1.0.0"
)

# Include all route modules
app.include_router(dashboard_router)
app.include_router(jobs_router)
app.include_router(skills_router)
app.include_router(legacy_router)

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint for the API"""
    return {"Hello": "Interview Trainer API"}
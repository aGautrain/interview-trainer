"""
Main application entry point for the Interview Trainer API.

This module initializes the FastAPI application and includes all route modules.
Routes are organized by domain in separate modules for better maintainability.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, close_db

# Import route modules
from routes import (
    dashboard_router,
    jobs_router,
    skills_router,
    job_analysis_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown"""
    # Startup
    await init_db()
    print("Database connection pool initialized")
    
    yield
    
    # Shutdown
    await close_db()
    print("Database connection pool closed")


# Create FastAPI application
app = FastAPI(
    title="Interview Trainer API",
    description="Backend API for the Interview Trainer application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(dashboard_router)
app.include_router(jobs_router)
app.include_router(skills_router)
app.include_router(job_analysis_router)

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint for the API"""
    return {"Hello": "Interview Trainer API"}
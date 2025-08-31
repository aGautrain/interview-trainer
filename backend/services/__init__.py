"""
Services package for the Interview Trainer application.

This package contains service layers and business logic components including:
- llm: LLM provider abstraction and management
- job_analysis: Job analysis and skills extraction service
"""

from .job_analysis import JobAnalysisService, get_job_analysis_service

__all__ = [
    "JobAnalysisService",
    "get_job_analysis_service"
]
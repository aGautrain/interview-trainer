"""
Job analysis endpoints for the Interview Trainer API.

This module provides REST API endpoints for job analysis functionality including:
- Single job analysis
- Skill extraction from text
- Bulk job analysis
- Training recommendations
- Analysis metrics and statistics
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse

from schemas.job_analysis import (
    JobAnalysisRequest, JobAnalysisResponse, 
    BulkJobAnalysisRequest, BulkJobAnalysisResponse,
    ExtractedSkillEnhanced, TrainingRecommendation, AnalysisMetrics
)
from schemas.base import ApiResponse
from services.job_analysis import get_job_analysis_service, JobAnalysisService


# Create router
router = APIRouter(prefix="/job-analysis", tags=["Job Analysis"])


async def get_analysis_service() -> JobAnalysisService:
    """Dependency to get job analysis service instance"""
    return await get_job_analysis_service()


@router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job(
    request: JobAnalysisRequest,
    service: JobAnalysisService = Depends(get_analysis_service)
) -> JobAnalysisResponse:
    """
    Analyze a job description and extract comprehensive information.
    
    This endpoint performs complete job analysis including:
    - Skill extraction and categorization
    - Experience level assessment
    - Training recommendations
    - Skill gap analysis (if user provided)
    
    The analysis leverages LLM providers and includes intelligent caching
    to optimize performance and cost.
    """
    try:
        
        response = await service.analyze_job_description(request)
        
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Job analysis failed: {str(e)}"
        )


@router.post("/extract-skills", response_model=List[ExtractedSkillEnhanced])
async def extract_skills(
    text: str,
    context_type: str = Query(default="job_description", description="Type of content being analyzed"),
    service: JobAnalysisService = Depends(get_analysis_service)
) -> List[ExtractedSkillEnhanced]:
    """
    Extract skills from any text content.
    
    This endpoint can analyze various types of content:
    - Job descriptions
    - Resumes/CVs  
    - Project descriptions
    - Course descriptions
    
    Returns a list of extracted skills with confidence scores and metadata.
    """
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text content cannot be empty")
        
        
        skills = await service.extract_skills_from_text(text, context_type)
        
        
        return skills
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Skill extraction failed: {str(e)}"
        )


@router.post("/analyze-bulk", response_model=BulkJobAnalysisResponse)
async def analyze_bulk_jobs(
    request: BulkJobAnalysisRequest,
    service: JobAnalysisService = Depends(get_analysis_service)
) -> BulkJobAnalysisResponse:
    """
    Analyze multiple job descriptions in parallel.
    
    This endpoint allows efficient analysis of multiple job postings
    with optimized parallel processing and resource management.
    
    Supports up to 50 job descriptions per request with configurable
    analysis depth and user personalization.
    """
    try:
        
        response = await service.bulk_analyze_jobs(request)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bulk job analysis failed: {str(e)}"
        )


@router.get("/metrics", response_model=AnalysisMetrics)
async def get_analysis_metrics(
    service: JobAnalysisService = Depends(get_analysis_service)
) -> AnalysisMetrics:
    """
    Get job analysis service metrics and statistics.
    
    Returns comprehensive metrics including:
    - Analysis success/failure rates
    - Cache performance statistics
    - Processing time averages
    - Token usage statistics
    - Most frequently analyzed skills
    """
    try:
        metrics = await service.get_analysis_metrics()
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get analysis metrics: {str(e)}"
        )


@router.post("/recommendations", response_model=List[TrainingRecommendation])
async def get_training_recommendations(
    analysis_id: str,
    user_id: Optional[str] = Query(None, description="User ID for personalized recommendations"),
    service: JobAnalysisService = Depends(get_analysis_service)
) -> List[TrainingRecommendation]:
    """
    Get training recommendations based on a previous job analysis.
    
    This endpoint retrieves detailed training recommendations from a cached
    job analysis result, with optional user personalization for skill gap analysis.
    """
    try:
        # This would typically fetch a cached analysis result
        # For now, return a placeholder response
        
        raise HTTPException(
            status_code=501,
            detail="Training recommendations endpoint is not yet implemented. Use the main analyze endpoint instead."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get training recommendations: {str(e)}"
        )


@router.get("/cache/stats")
async def get_cache_statistics() -> JSONResponse:
    """
    Get cache performance statistics.
    
    Returns information about cache hit rates, storage usage,
    and performance metrics for the job analysis caching system.
    """
    try:
        # This would query the database for cache statistics
        # For now, return placeholder data
        
        stats = {
            "message": "Cache statistics endpoint is available but not fully implemented",
            "cache_enabled": True,
            "placeholder_data": {
                "total_entries": 0,
                "hit_rate": 0.0,
                "avg_hit_time_ms": 0.0,
                "cache_size_mb": 0.0
            }
        }
        
        return JSONResponse(content=stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get cache statistics: {str(e)}"
        )


@router.delete("/cache/clear")
async def clear_analysis_cache(
    force: bool = Query(False, description="Force clear all cache entries"),
) -> ApiResponse:
    """
    Clear expired cache entries or force clear all cache.
    
    By default, only removes expired cache entries. Use force=true
    to clear all cache entries (useful for development/testing).
    """
    try:
        if force:
            # This would clear all cache entries
            return ApiResponse(
                success=False,
                message="Force cache clear is not yet implemented"
            )
        else:
            # This would clear only expired entries
            return ApiResponse(
                success=False,
                message="Expired cache clear is not yet implemented"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )


@router.get("/health")
async def health_check(
    service: JobAnalysisService = Depends(get_analysis_service)
) -> JSONResponse:
    """
    Health check endpoint for job analysis service.
    
    Verifies that the service and its dependencies (LLM providers, database)
    are functioning correctly.
    """
    try:
        # Check LLM provider health
        from services.llm import get_available_provider
        
        health_status = {
            "service": "job_analysis",
            "status": "healthy",
            "timestamp": None,
            "components": {
                "llm_provider": "unknown",
                "database": "unknown",
                "cache": "unknown"
            }
        }
        
        try:
            provider = await get_available_provider()
            if provider:
                provider_healthy = await provider.health_check()
                health_status["components"]["llm_provider"] = "healthy" if provider_healthy else "unhealthy"
            else:
                health_status["components"]["llm_provider"] = "unavailable"
                
        except Exception as e:
            health_status["components"]["llm_provider"] = f"error: {str(e)}"
        
        # Database and cache checks would go here
        health_status["components"]["database"] = "not_checked"
        health_status["components"]["cache"] = "not_checked"
        
        # Determine overall health
        if health_status["components"]["llm_provider"] in ["healthy", "unknown"]:
            health_status["status"] = "healthy"
        else:
            health_status["status"] = "degraded"
        
        from datetime import datetime
        health_status["timestamp"] = datetime.utcnow().isoformat()
        
        return JSONResponse(content=health_status)
        
    except Exception as e:
        return JSONResponse(
            content={
                "service": "job_analysis",
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            },
            status_code=503
        )


# Additional utility endpoints for development and debugging

@router.get("/debug/llm-providers")
async def debug_llm_providers() -> JSONResponse:
    """
    Debug endpoint to check available LLM providers.
    
    This endpoint is useful for development and troubleshooting
    to see which LLM providers are configured and available.
    """
    try:
        from services.llm import get_llm_factory
        
        factory = get_llm_factory()
        available_providers = []
        
        # This would enumerate all configured providers
        # For now, just check the default
        try:
            from services.llm import get_available_provider
            provider = await get_available_provider()
            
            if provider:
                info = provider.get_provider_info()
                available_providers.append({
                    "provider": info["name"],
                    "class": info["class"],
                    "healthy": await provider.health_check(),
                    "config_keys": info.get("config_keys", [])
                })
                
        except Exception as e:
            available_providers.append({
                "provider": "unknown",
                "error": str(e),
                "healthy": False
            })
        
        return JSONResponse(content={
            "available_providers": available_providers,
            "total_providers": len(available_providers)
        })
        
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
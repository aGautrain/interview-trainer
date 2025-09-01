"""
Job analysis endpoints for the Interview Trainer API.

This module provides REST API endpoints for job analysis functionality including:
- Single job analysis
- Skill extraction from text
- Bulk job analysis
- Training recommendations
- Analysis metrics and statistics
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from schemas.job_analysis import (
    AnalysisMetrics
)
from services.job_analysis import get_job_analysis_service, JobAnalysisService


# Create router
router = APIRouter(prefix="/job-analysis", tags=["Job Analysis"])


async def get_analysis_service() -> JobAnalysisService:
    """Dependency to get job analysis service instance"""
    return await get_job_analysis_service()



@router.get("/metrics", response_model=AnalysisMetrics)
async def get_analysis_metrics(
    service: JobAnalysisService = Depends(get_analysis_service)
) -> AnalysisMetrics:
    """
    Get job analysis service metrics and statistics.
    
    Returns comprehensive metrics including:
    - Analysis success/failure rates
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
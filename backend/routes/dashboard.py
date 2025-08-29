"""
Dashboard routes for the Interview Trainer API.

This module contains all dashboard-related endpoints including:
- Dashboard data retrieval
- Statistics endpoints
"""

from fastapi import APIRouter
from schemas import DashboardData, DashboardStats
from sample_data import (
    SAMPLE_DASHBOARD_STATS,
    SAMPLE_JOBS,
    SAMPLE_SKILL_DISTRIBUTION_DATA,
    SAMPLE_PERFORMANCE_DATA
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardData)
def get_dashboard_data():
    """Get dashboard data using our Pydantic schemas"""
    return DashboardData(
        stats=SAMPLE_DASHBOARD_STATS,
        jobs=SAMPLE_JOBS,
        skillDistributionData=SAMPLE_SKILL_DISTRIBUTION_DATA,
        performanceData=SAMPLE_PERFORMANCE_DATA
    )


@router.get("/stats", response_model=DashboardStats)
def get_stats():
    """Get dashboard statistics"""
    return SAMPLE_DASHBOARD_STATS

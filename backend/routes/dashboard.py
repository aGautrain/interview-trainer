"""
Dashboard routes for the Interview Trainer API.

This module contains all dashboard-related endpoints including:
- Dashboard data retrieval
- Statistics endpoints
"""

from fastapi import APIRouter
from schemas import DashboardData, DashboardStats, Job, SkillDistributionData, PerformanceData
from database import fetch_one, fetch_all
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardData)
async def get_dashboard_data():
    """Get dashboard data from the database"""
    # Get dashboard stats
    stats_data = await fetch_one("SELECT * FROM dashboard_stats LIMIT 1")
    stats = DashboardStats(
        activeJobs=stats_data['active_jobs'],
        questionsCompleted=stats_data['questions_completed'],
        avgProgress=stats_data['avg_progress'],
        successRate=stats_data['success_rate']
    ) if stats_data else DashboardStats(activeJobs=0, questionsCompleted=0, avgProgress=0, successRate=0)
    
    # Get jobs
    jobs_data = await fetch_all("SELECT * FROM jobs ORDER BY created_at DESC")
    jobs = [Job(
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
    
    # Get skill distribution data
    skill_dist_data = await fetch_all("SELECT * FROM skill_distribution_data")
    skill_distribution = [SkillDistributionData(
        name=item['name'],
        value=item['value'],
        color=item['color']
    ) for item in skill_dist_data]
    
    # Get performance data
    perf_data = await fetch_all("SELECT * FROM performance_data ORDER BY difficulty")
    performance_data = [PerformanceData(
        difficulty=item['difficulty'],
        success=item['success'],
        failure=item['failure']
    ) for item in perf_data]
    
    return DashboardData(
        stats=stats,
        jobs=jobs,
        skillDistributionData=skill_distribution,
        performanceData=performance_data
    )


@router.get("/stats", response_model=DashboardStats)
async def get_stats():
    """Get dashboard statistics from the database"""
    stats_data = await fetch_one("SELECT * FROM dashboard_stats LIMIT 1")
    
    if stats_data:
        return DashboardStats(
            activeJobs=stats_data['active_jobs'],
            questionsCompleted=stats_data['questions_completed'],
            avgProgress=stats_data['avg_progress'],
            successRate=stats_data['success_rate']
        )
    
    return DashboardStats(activeJobs=0, questionsCompleted=0, avgProgress=0, successRate=0)

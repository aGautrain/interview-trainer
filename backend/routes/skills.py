"""
Skills routes for the Interview Trainer API.

This module contains all skills and training-related endpoints including:
- Skills listing
- Questions for specific skills
- Exercises for specific skills
"""

from fastapi import APIRouter
from schemas import SkillCard
from sample_data import SAMPLE_SKILLS, get_sample_questions, get_sample_exercises

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=list[SkillCard])
def get_skills():
    """Get all skills"""
    return SAMPLE_SKILLS


@router.get("/{skill_name}/questions")
def get_skill_questions(skill_name: str):
    """Get questions for a specific skill"""
    return get_sample_questions(skill_name)


@router.get("/{skill_name}/exercises")
def get_skill_exercises(skill_name: str):
    """Get exercises for a specific skill"""
    return get_sample_exercises(skill_name)

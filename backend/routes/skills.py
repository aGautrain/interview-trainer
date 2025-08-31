"""
Skills routes for the Interview Trainer API.

This module contains all skills and training-related endpoints including:
- Skills listing
- Questions for specific skills
- Exercises for specific skills
"""

from fastapi import APIRouter
from schemas import SkillCard, Question, Exercise
from database import fetch_all

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=list[SkillCard])
async def get_skills():
    """Get all skills from the database"""
    skills_data = await fetch_all("SELECT * FROM skill_cards ORDER BY name")
    
    return [SkillCard(
        name=skill['name'],
        type=skill['type'],
        questionsCompleted=skill['questions_completed'],
        questionsTotal=skill['questions_total'],
        exercisesCompleted=skill['exercises_completed'],
        exercisesTotal=skill['exercises_total']
    ) for skill in skills_data]


@router.get("/{skill_name}/questions")
async def get_skill_questions(skill_name: str):
    """Get questions for a specific skill from the database"""
    questions_data = await fetch_all(
        "SELECT * FROM questions WHERE category = $1 ORDER BY created_at", 
        skill_name
    )
    
    return [Question(
        id=str(question['id']),
        text=question['text'],
        type=question['type'],
        difficulty=question['difficulty'],
        category=question['category'],
        skills=[],  # This would need a separate relation table
        isCompleted=question['is_completed'],
        createdAt=question['created_at'].isoformat() + 'Z'
    ) for question in questions_data]


@router.get("/{skill_name}/exercises")
async def get_skill_exercises(skill_name: str):
    """Get exercises for a specific skill from the database"""
    exercises_data = await fetch_all(
        "SELECT * FROM exercises WHERE category = $1 ORDER BY created_at", 
        skill_name
    )
    
    return [Exercise(
        id=str(exercise['id']),
        title=exercise['title'],
        description=exercise['description'],
        difficulty=exercise['difficulty'],
        category=exercise['category'],
        skills=[],  # This would need a separate relation table
        isCompleted=exercise['is_completed'],
        createdAt=exercise['created_at'].isoformat() + 'Z'
    ) for exercise in exercises_data]

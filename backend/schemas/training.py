from typing import List, Optional
from pydantic import BaseModel, Field
from .base import BaseSchema, Skill, DifficultyLevel, QuestionType, SkillType


class Question(BaseModel):
    """Unified training question schema"""
    id: str = Field(..., description="Unique identifier")
    text: str = Field(..., description="Question text")
    type: QuestionType = Field(..., description="Question type")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level")
    category: str = Field(..., description="Question category")
    skills: List[Skill] = Field(..., description="Related skills")
    sampleAnswer: Optional[str] = Field(None, description="Sample answer")
    tips: Optional[List[str]] = Field(None, description="Helpful tips")
    isCompleted: bool = Field(False, description="Whether question is completed")
    createdAt: str = Field(..., description="Creation date")


class Exercise(BaseModel):
    """Unified training exercise schema"""
    id: str = Field(..., description="Unique identifier")
    title: str = Field(..., description="Exercise title")
    description: str = Field(..., description="Exercise description")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level")
    category: str = Field(..., description="Exercise category")
    programmingLanguage: Optional[str] = Field(None, description="Programming language")
    skills: List[Skill] = Field(..., description="Related skills")
    requirements: Optional[List[str]] = Field(None, description="Exercise requirements")
    code: Optional[str] = Field(None, description="Starter code")
    solution: Optional[str] = Field(None, description="Solution code")
    hints: Optional[List[str]] = Field(None, description="Helpful hints")
    timeLimit: Optional[int] = Field(None, description="Time limit in minutes")
    isCompleted: bool = Field(False, description="Whether exercise is completed")
    createdAt: str = Field(..., description="Creation date")


class TestCase(BaseModel):
    """Test case for coding exercises"""
    input: str = Field(..., description="Input data")
    expectedOutput: str = Field(..., description="Expected output")
    description: Optional[str] = Field(None, description="Test case description")


class SkillCard(BaseModel):
    """Skill card for training display"""
    name: str = Field(..., description="Skill name")
    type: SkillType = Field(..., description="Skill type")
    questionsCompleted: int = Field(..., ge=0, description="Number of completed questions")
    questionsTotal: int = Field(..., ge=0, description="Total number of questions")
    exercisesCompleted: int = Field(..., ge=0, description="Number of completed exercises")
    exercisesTotal: int = Field(..., ge=0, description="Total number of exercises")


class SkillTrainingProgress(BaseModel):
    """Skill training progress tracking"""
    skillId: str = Field(..., description="Skill identifier")
    skillName: str = Field(..., description="Skill name")
    questionsCompleted: int = Field(..., ge=0, description="Completed questions count")
    questionsTotal: int = Field(..., ge=0, description="Total questions count")
    exercisesCompleted: int = Field(..., ge=0, description="Completed exercises count")
    exercisesTotal: int = Field(..., ge=0, description="Total exercises count")
    progressPercentage: float = Field(..., ge=0.0, le=100.0, description="Overall progress percentage")


class SkillTrainingSession(BaseModel):
    """Skill training session data"""
    id: str = Field(..., description="Session identifier")
    skillId: str = Field(..., description="Skill being trained")
    userId: str = Field(..., description="User identifier")
    startTime: str = Field(..., description="Session start time")
    endTime: Optional[str] = Field(None, description="Session end time")
    questionsAnswered: int = Field(0, description="Questions answered in session")
    exercisesCompleted: int = Field(0, description="Exercises completed in session")
    score: Optional[float] = Field(None, description="Session score")


class SkillTrainingData(BaseModel):
    """Complete skill training data"""
    skill: SkillCard
    questions: List[Question]
    exercises: List[Exercise]

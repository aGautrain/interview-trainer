"""
Database models for the Interview Trainer application.
Defines the structure and relationships between different entities.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

# Import the database instance from the app factory
from . import db

# Association table for many-to-many relationships
job_skills = Table(
    'job_skills',
    db.metadata,
    Column('job_posting_id', Integer, ForeignKey('job_posting.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skill.id'), primary_key=True)
)

class JobPosting(db.Model):
    """
    Model representing a job posting with its requirements and description.
    
    Attributes:
        id: Unique identifier for the job posting
        title: Job title/position name
        company: Company offering the position
        description: Full job description text
        requirements: Job requirements text
        location: Job location (city, country, remote, etc.)
        created_at: Timestamp when the job posting was created
        skills: Associated skills extracted from the job posting
        questions: Questions generated for this job posting
        exercises: Coding exercises generated for this job posting
    """
    
    __tablename__ = 'job_posting'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    skills = relationship('Skill', secondary=job_skills, back_populates='job_postings')
    questions = relationship('Question', back_populates='job_posting', cascade='all, delete-orphan')
    exercises = relationship('CodingExercise', back_populates='job_posting', cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of the job posting."""
        return f'<JobPosting {self.title} at {self.company}>'
    
    def to_dict(self):
        """Convert job posting to dictionary for API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'requirements': self.requirements,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'skills': [skill.to_dict() for skill in self.skills],
            'questions_count': len(self.questions),
            'exercises_count': len(self.exercises)
        }

class Skill(db.Model):
    """
    Model representing a skill that can be required for job positions.
    
    Attributes:
        id: Unique identifier for the skill
        name: Skill name (e.g., 'Python', 'React', 'Machine Learning')
        category: Skill category (e.g., 'Programming Language', 'Framework', 'Concept')
        level: Skill level (e.g., 'Beginner', 'Intermediate', 'Advanced')
        description: Detailed description of the skill
        job_postings: Job postings that require this skill
    """
    
    __tablename__ = 'skill'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=True, index=True)
    level = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    job_postings = relationship('JobPosting', secondary=job_skills, back_populates='skills')
    
    def __repr__(self):
        """String representation of the skill."""
        return f'<Skill {self.name} ({self.category})>'
    
    def to_dict(self):
        """Convert skill to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'level': self.level,
            'description': self.description
        }

class Question(db.Model):
    """
    Model representing an interview question generated for a specific job posting.
    
    Attributes:
        id: Unique identifier for the question
        text: The actual question text
        question_type: Type of question (e.g., 'technical', 'behavioral', 'situational')
        difficulty: Difficulty level (e.g., 'beginner', 'intermediate', 'advanced')
        category: Question category (e.g., 'algorithms', 'system_design', 'leadership')
        answer_hints: Hints or guidance for answering the question
        created_at: Timestamp when the question was created
        job_posting_id: Reference to the associated job posting
        job_posting: The associated job posting object
    """
    
    __tablename__ = 'question'
    
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    answer_hints = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Foreign key relationships
    job_posting_id = Column(Integer, ForeignKey('job_posting.id'), nullable=False)
    job_posting = relationship('JobPosting', back_populates='questions')
    
    def __repr__(self):
        """String representation of the question."""
        return f'<Question {self.question_type} - {self.difficulty}>'
    
    def to_dict(self):
        """Convert question to dictionary for API responses."""
        return {
            'id': self.id,
            'text': self.text,
            'question_type': self.question_type,
            'difficulty': self.difficulty,
            'category': self.category,
            'answer_hints': self.answer_hints,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'job_posting_id': self.job_posting_id
        }

class CodingExercise(db.Model):
    """
    Model representing a coding exercise generated for a specific job posting.
    
    Attributes:
        id: Unique identifier for the exercise
        title: Exercise title/name
        description: Problem description and requirements
        programming_language: Target programming language
        difficulty: Difficulty level (e.g., 'beginner', 'intermediate', 'advanced')
        category: Exercise category (e.g., 'algorithms', 'data_structures', 'system_design')
        solution: Sample solution or approach
        test_cases: Example test cases
        time_limit: Estimated time to complete (in minutes)
        created_at: Timestamp when the exercise was created
        job_posting_id: Reference to the associated job posting
        job_posting: The associated job posting object
    """
    
    __tablename__ = 'coding_exercise'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    programming_language = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    solution = Column(Text, nullable=True)
    test_cases = Column(Text, nullable=True)
    time_limit = Column(Integer, nullable=True)  # in minutes
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Foreign key relationships
    job_posting_id = Column(Integer, ForeignKey('job_posting.id'), nullable=False)
    job_posting = relationship('JobPosting', back_populates='exercises')
    
    def __repr__(self):
        """String representation of the coding exercise."""
        return f'<CodingExercise {self.title} ({self.programming_language})>'
    
    def to_dict(self):
        """Convert coding exercise to dictionary for API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'programming_language': self.programming_language,
            'difficulty': self.difficulty,
            'category': self.category,
            'solution': self.solution,
            'test_cases': self.test_cases,
            'time_limit': self.time_limit,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'job_posting_id': self.job_posting_id
        }

class UserSession(db.Model):
    """
    Model representing a user session with LLM preferences and API keys.
    
    Attributes:
        id: Unique identifier for the session
        session_id: Unique session identifier
        openai_api_key: OpenAI API key (encrypted in production)
        preferred_model: Preferred OpenAI model
        created_at: Timestamp when the session was created
        last_used: Timestamp of last activity
        is_active: Whether the session is currently active
    """
    
    __tablename__ = 'user_session'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    openai_api_key = Column(String(255), nullable=True)  # Should be encrypted in production
    preferred_model = Column(String(100), default='gpt-3.5-turbo')
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_used = Column(DateTime, default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    def __repr__(self):
        """String representation of the user session."""
        return f'<UserSession {self.session_id}>'
    
    def to_dict(self):
        """Convert user session to dictionary for API responses."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'preferred_model': self.preferred_model,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'is_active': self.is_active
        }

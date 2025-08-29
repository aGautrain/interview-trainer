#!/usr/bin/env python3
"""
Script to populate the PostgreSQL database with sample data.
This script reads the sample data from the backend and inserts it into the database.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path so we can import the sample data
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sample_data import (
    SAMPLE_DASHBOARD_STATS,
    SAMPLE_JOBS,
    SAMPLE_SKILL_DISTRIBUTION_DATA,
    SAMPLE_PERFORMANCE_DATA,
    SAMPLE_SKILLS,
    SAMPLE_QUESTIONS,
    SAMPLE_EXERCISES,
    SAMPLE_USER_PREFERENCES,
    SAMPLE_LLM_CONFIG
)

# Database connection configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'interview_trainer'),
    'user': os.getenv('DB_USER', 'interview_user'),
    'password': os.getenv('DB_PASSWORD', 'interview_password')
}

def connect_to_db():
    """Establish connection to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def check_if_data_exists(cursor, table_name):
    """Check if data already exists in a table"""
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    return count > 0

def insert_dashboard_stats(cursor):
    """Insert dashboard statistics data"""
    if check_if_data_exists(cursor, 'dashboard_stats'):
        print("Dashboard stats already exist, skipping...")
        return
    
    cursor.execute("""
        INSERT INTO dashboard_stats (active_jobs, questions_completed, avg_progress, success_rate)
        VALUES (%s, %s, %s, %s)
    """, (
        SAMPLE_DASHBOARD_STATS.activeJobs,
        SAMPLE_DASHBOARD_STATS.questionsCompleted,
        SAMPLE_DASHBOARD_STATS.avgProgress,
        SAMPLE_DASHBOARD_STATS.successRate
    ))
    print("Inserted dashboard stats")

def insert_jobs(cursor):
    """Insert sample jobs data"""
    if check_if_data_exists(cursor, 'jobs'):
        print("Jobs already exist, skipping...")
        return
    
    for job in SAMPLE_JOBS:
        cursor.execute("""
            INSERT INTO jobs (
                id, title, company, description, requirements, skills, tech_stack,
                location, type, level, salary_range, is_remote, progress,
                created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            job.id, job.title, job.company, job.description, job.requirements,
            job.skills, job.techStack, job.location, job.type, job.level,
            job.salaryRange, job.isRemote, job.progress,
            datetime.fromisoformat(job.createdAt.replace('Z', '+00:00')),
            datetime.fromisoformat(job.updatedAt.replace('Z', '+00:00'))
        ))
    print(f"Inserted {len(SAMPLE_JOBS)} jobs")

def insert_skill_distribution_data(cursor):
    """Insert skill distribution data"""
    if check_if_data_exists(cursor, 'skill_distribution_data'):
        print("Skill distribution data already exists, skipping...")
        return
    
    for skill_data in SAMPLE_SKILL_DISTRIBUTION_DATA:
        cursor.execute("""
            INSERT INTO skill_distribution_data (name, value, color)
            VALUES (%s, %s, %s)
        """, (skill_data.name, skill_data.value, skill_data.color))
    print(f"Inserted {len(SAMPLE_SKILL_DISTRIBUTION_DATA)} skill distribution records")

def insert_performance_data(cursor):
    """Insert performance data"""
    if check_if_data_exists(cursor, 'performance_data'):
        print("Performance data already exists, skipping...")
        return
    
    for perf_data in SAMPLE_PERFORMANCE_DATA:
        cursor.execute("""
            INSERT INTO performance_data (difficulty, success, failure)
            VALUES (%s, %s, %s)
        """, (perf_data.difficulty, perf_data.success, perf_data.failure))
    print(f"Inserted {len(SAMPLE_PERFORMANCE_DATA)} performance records")

def insert_skill_cards(cursor):
    """Insert skill cards data"""
    if check_if_data_exists(cursor, 'skill_cards'):
        print("Skill cards already exist, skipping...")
        return
    
    for skill in SAMPLE_SKILLS:
        cursor.execute("""
            INSERT INTO skill_cards (
                name, type, questions_completed, questions_total,
                exercises_completed, exercises_total
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            skill.name, skill.type.value, skill.questionsCompleted,
            skill.questionsTotal, skill.exercisesCompleted, skill.exercisesTotal
        ))
    print(f"Inserted {len(SAMPLE_SKILLS)} skill cards")

def insert_questions(cursor):
    """Insert sample questions data"""
    if check_if_data_exists(cursor, 'questions'):
        print("Questions already exist, skipping...")
        return
    
    for skill_name, questions in SAMPLE_QUESTIONS.items():
        for question in questions:
            cursor.execute("""
                INSERT INTO questions (
                    id, text, type, difficulty, category, is_completed, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                question.id, question.text, question.type.value, question.difficulty.value,
                question.category, question.isCompleted,
                datetime.fromisoformat(question.createdAt.replace('Z', '+00:00'))
            ))
    
    total_questions = sum(len(questions) for questions in SAMPLE_QUESTIONS.values())
    print(f"Inserted {total_questions} questions")

def insert_exercises(cursor):
    """Insert sample exercises data"""
    if check_if_data_exists(cursor, 'exercises'):
        print("Exercises already exist, skipping...")
        return
    
    for skill_name, exercises in SAMPLE_EXERCISES.items():
        for exercise in exercises:
            cursor.execute("""
                INSERT INTO exercises (
                    id, title, description, difficulty, category, is_completed, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                exercise.id, exercise.title, exercise.description, exercise.difficulty.value,
                exercise.category, exercise.isCompleted,
                datetime.fromisoformat(exercise.createdAt.replace('Z', '+00:00'))
            ))
    
    total_exercises = sum(len(exercises) for exercises in SAMPLE_EXERCISES.values())
    print(f"Inserted {total_exercises} exercises")

def insert_user_preferences(cursor):
    """Insert user preferences data"""
    if check_if_data_exists(cursor, 'user_preferences'):
        print("User preferences already exist, skipping...")
        return
    
    # First create a dummy user
    cursor.execute("""
        INSERT INTO users (email, username) VALUES (%s, %s)
        RETURNING id
    """, ('sample@example.com', 'sample_user'))
    
    user_id = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO user_preferences (
            user_id, default_difficulty, preferred_languages, question_types, theme
        ) VALUES (%s, %s, %s, %s, %s)
    """, (
        user_id, SAMPLE_USER_PREFERENCES.defaultDifficulty,
        SAMPLE_USER_PREFERENCES.preferredLanguages,
        SAMPLE_USER_PREFERENCES.questionTypes,
        SAMPLE_USER_PREFERENCES.theme
    ))
    print("Inserted user preferences")

def insert_llm_config(cursor):
    """Insert LLM configuration data"""
    if check_if_data_exists(cursor, 'llm_config'):
        print("LLM config already exists, skipping...")
        return
    
    cursor.execute("""
        INSERT INTO llm_config (api_key, model, temperature, max_tokens)
        VALUES (%s, %s, %s, %s)
    """, (
        SAMPLE_LLM_CONFIG.apiKey,
        SAMPLE_LLM_CONFIG.model,
        SAMPLE_LLM_CONFIG.temperature,
        SAMPLE_LLM_CONFIG.maxTokens
    ))
    print("Inserted LLM configuration")

def main():
    """Main function to populate the database"""
    print("Starting database population...")
    
    conn = connect_to_db()
    cursor = conn.cursor()
    
    try:
        # Insert all sample data
        insert_dashboard_stats(cursor)
        insert_jobs(cursor)
        insert_skill_distribution_data(cursor)
        insert_performance_data(cursor)
        insert_skill_cards(cursor)
        insert_questions(cursor)
        insert_exercises(cursor)
        insert_user_preferences(cursor)
        insert_llm_config(cursor)
        
        # Commit all changes
        conn.commit()
        print("\nDatabase population completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during database population: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

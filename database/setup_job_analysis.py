#!/usr/bin/env python3
"""
Setup script for job analysis database tables.
Creates all necessary tables, indexes, and functions for the job analysis service.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
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


def execute_sql_file(cursor, filepath):
    """Execute SQL statements from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Execute the SQL (split by statements if needed for complex files)
        cursor.execute(sql_content)
        print(f"Successfully executed SQL from {filepath}")
        return True
        
    except Exception as e:
        print(f"Error executing SQL file {filepath}: {e}")
        return False


def verify_tables_created(cursor):
    """Verify that all expected tables were created"""
    expected_tables = [
        'job_analysis_cache',
        'job_analysis_history', 
        'job_analysis_cache_skills',
        'user_skills',
        'training_recommendations',
        'bulk_job_analyses'
    ]
    
    for table in expected_tables:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, (table,))
        
        exists = cursor.fetchone()[0]
        if exists:
            print(f"[OK] Table '{table}' created successfully")
        else:
            print(f"[ERROR] Table '{table}' was not created")
            return False
    
    return True


def verify_functions_created(cursor):
    """Verify that database functions were created"""
    expected_functions = [
        'cleanup_expired_cache',
        'get_skill_analysis_stats',
        'refresh_job_analysis_metrics'
    ]
    
    for function in expected_functions:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.routines
                WHERE routine_schema = 'public'
                AND routine_name = %s
                AND routine_type = 'FUNCTION'
            );
        """, (function,))
        
        exists = cursor.fetchone()[0]
        if exists:
            print(f"[OK] Function '{function}' created successfully")
        else:
            print(f"[ERROR] Function '{function}' was not created")
            return False
    
    return True


def verify_materialized_view(cursor):
    """Verify that materialized view was created"""
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM pg_matviews
            WHERE schemaname = 'public'
            AND matviewname = 'job_analysis_metrics'
        );
    """)
    
    exists = cursor.fetchone()[0]
    if exists:
        print("[OK] Materialized view 'job_analysis_metrics' created successfully")
        return True
    else:
        print("[ERROR] Materialized view 'job_analysis_metrics' was not created")
        return False


def create_sample_data(cursor):
    """Create some sample data for testing"""
    try:
        # Insert a sample user skill for testing gap analysis
        cursor.execute("""
            INSERT INTO user_skills (user_id, skill_name, proficiency_level, years_experience, confidence_score)
            VALUES 
                ('sample_user', 'JavaScript', 'intermediate', 3, 0.8),
                ('sample_user', 'Python', 'beginner', 1, 0.6),
                ('sample_user', 'React', 'intermediate', 2, 0.7),
                ('sample_user', 'SQL', 'beginner', 1, 0.5)
            ON CONFLICT (user_id, skill_name) DO NOTHING;
        """)
        
        print("[OK] Sample user skills created")
        
    except Exception as e:
        print(f"Warning: Could not create sample data: {e}")


def main():
    """Main setup function"""
    print("Setting up job analysis database tables...")
    
    # Connect to database
    conn = connect_to_db()
    cursor = conn.cursor()
    
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sql_file_path = os.path.join(script_dir, 'create_job_analysis_tables.sql')
        
        # Execute the SQL file
        if not execute_sql_file(cursor, sql_file_path):
            conn.rollback()
            print("Setup failed!")
            sys.exit(1)
        
        # Verify tables were created
        if not verify_tables_created(cursor):
            conn.rollback()
            print("Table verification failed!")
            sys.exit(1)
        
        # Verify functions were created
        if not verify_functions_created(cursor):
            conn.rollback()
            print("Function verification failed!")
            sys.exit(1)
        
        # Verify materialized view was created
        if not verify_materialized_view(cursor):
            conn.rollback()
            print("Materialized view verification failed!")
            sys.exit(1)
        
        # Create sample data
        create_sample_data(cursor)
        
        # Commit all changes
        conn.commit()
        print("\n[SUCCESS] Job analysis database setup completed successfully!")
        
        # Show summary
        print("\nCreated tables:")
        print("- job_analysis_cache: Caches LLM analysis results")
        print("- job_analysis_history: Tracks analysis operations")
        print("- job_analysis_cache_skills: Tracks extracted skills")
        print("- user_skills: User skill proficiency levels")
        print("- training_recommendations: Generated recommendations")
        print("- bulk_job_analyses: Bulk operation tracking")
        print("\nCreated functions:")
        print("- cleanup_expired_cache(): Removes expired cache entries")
        print("- get_skill_analysis_stats(): Skill analysis statistics")
        print("- refresh_job_analysis_metrics(): Refreshes metrics view")
        print("\nCreated materialized view:")
        print("- job_analysis_metrics: Aggregated metrics and statistics")
        
    except Exception as e:
        conn.rollback()
        print(f"Setup failed with error: {e}")
        sys.exit(1)
        
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
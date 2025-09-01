-- Drop all database objects for Interview Trainer application
-- This script provides a clean slate by removing all tables, triggers, functions, types, and extensions
-- Run this script when you want to start fresh

-- Disable triggers temporarily to avoid conflicts during deletion
SET session_replication_role = replica;

-- Drop all triggers first
DROP TRIGGER IF EXISTS update_jobs_updated_at ON jobs CASCADE;
DROP TRIGGER IF EXISTS update_questions_updated_at ON questions CASCADE;
DROP TRIGGER IF EXISTS update_exercises_updated_at ON exercises CASCADE;
DROP TRIGGER IF EXISTS update_skills_updated_at ON skills CASCADE;
DROP TRIGGER IF EXISTS update_skill_cards_updated_at ON skill_cards CASCADE;
DROP TRIGGER IF EXISTS update_llm_config_updated_at ON llm_config CASCADE;

-- Drop all tables in dependency order (junction tables first, then main tables)
DROP TABLE IF EXISTS question_skills CASCADE;
DROP TABLE IF EXISTS exercise_skills CASCADE;
DROP TABLE IF EXISTS llm_config CASCADE;
DROP TABLE IF EXISTS skill_distribution_data CASCADE;
DROP TABLE IF EXISTS performance_data CASCADE;
DROP TABLE IF EXISTS dashboard_stats CASCADE;
DROP TABLE IF EXISTS skill_cards CASCADE;
DROP TABLE IF EXISTS exercises CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop all indexes
DROP INDEX IF EXISTS idx_jobs_company CASCADE;
DROP INDEX IF EXISTS idx_jobs_title CASCADE;
DROP INDEX IF EXISTS idx_questions_category CASCADE;
DROP INDEX IF EXISTS idx_questions_difficulty CASCADE;
DROP INDEX IF EXISTS idx_exercises_category CASCADE;
DROP INDEX IF EXISTS idx_exercises_difficulty CASCADE;
DROP INDEX IF EXISTS idx_skills_type CASCADE;
DROP INDEX IF EXISTS idx_skill_cards_name CASCADE;

-- Drop the trigger function
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Drop custom enum types
DROP TYPE IF EXISTS difficulty_level CASCADE;
DROP TYPE IF EXISTS question_type CASCADE;
DROP TYPE IF EXISTS skill_type CASCADE;

-- Re-enable triggers
SET session_replication_role = DEFAULT;

-- Note: The uuid-ossp extension is not dropped as it's a system extension
-- and may be used by other parts of the system

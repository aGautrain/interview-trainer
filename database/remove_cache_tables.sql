-- Migration script to remove caching tables and simplify database schema
-- This script removes all job analysis cache-related tables

-- Drop materialized view first (depends on history table)
DROP MATERIALIZED VIEW IF EXISTS job_analysis_metrics;

-- Drop dependent tables first
DROP TABLE IF EXISTS job_analysis_cache_skills;
DROP TABLE IF EXISTS training_recommendations;
DROP TABLE IF EXISTS bulk_job_analyses;

-- Drop main cache table
DROP TABLE IF EXISTS job_analysis_cache;

-- Drop history table (contains cache_hit column)
DROP TABLE IF EXISTS job_analysis_history;

-- Drop user_skills table if not needed elsewhere
DROP TABLE IF EXISTS user_skills;

-- Drop functions related to cache
DROP FUNCTION IF EXISTS cleanup_expired_cache();
DROP FUNCTION IF EXISTS get_skill_analysis_stats();
DROP FUNCTION IF EXISTS refresh_job_analysis_metrics();

-- Clean up any indexes that might still exist
DROP INDEX IF EXISTS idx_job_analysis_cache_hash;
DROP INDEX IF EXISTS idx_job_analysis_cache_expires;
DROP INDEX IF EXISTS idx_job_analysis_cache_provider;
DROP INDEX IF EXISTS idx_job_analysis_history_user;
DROP INDEX IF EXISTS idx_job_analysis_history_status;
DROP INDEX IF EXISTS idx_job_analysis_history_provider;
DROP INDEX IF EXISTS idx_job_analysis_history_created;
DROP INDEX IF EXISTS idx_job_analysis_cache_skills_name;
DROP INDEX IF EXISTS idx_job_analysis_cache_skills_category;
DROP INDEX IF EXISTS idx_job_analysis_cache_skills_type;
DROP INDEX IF EXISTS idx_user_skills_user_id;
DROP INDEX IF EXISTS idx_user_skills_name;
DROP INDEX IF EXISTS idx_user_skills_level;
DROP INDEX IF EXISTS idx_training_recommendations_analysis;
DROP INDEX IF EXISTS idx_training_recommendations_user;
DROP INDEX IF EXISTS idx_training_recommendations_skill;
DROP INDEX IF EXISTS idx_training_recommendations_priority;
DROP INDEX IF EXISTS idx_training_recommendations_status;
DROP INDEX IF EXISTS idx_bulk_job_analyses_batch;
DROP INDEX IF EXISTS idx_bulk_job_analyses_user;
DROP INDEX IF EXISTS idx_bulk_job_analyses_status;
DROP INDEX IF EXISTS idx_job_analysis_metrics_date;

COMMIT;
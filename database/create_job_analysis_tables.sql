-- Database tables for job analysis service
-- These tables support caching, tracking, and metrics for job analysis operations

-- Job analysis cache table
CREATE TABLE IF NOT EXISTS job_analysis_cache (
    id SERIAL PRIMARY KEY,
    job_description_hash VARCHAR(32) UNIQUE NOT NULL,
    analysis_request JSONB NOT NULL,
    analysis_result JSONB NOT NULL,
    llm_provider VARCHAR(50) NOT NULL,
    tokens_used INTEGER,
    expires_at TIMESTAMP NOT NULL,
    hit_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for efficient cache lookups
CREATE INDEX IF NOT EXISTS idx_job_analysis_cache_hash ON job_analysis_cache(job_description_hash);
CREATE INDEX IF NOT EXISTS idx_job_analysis_cache_expires ON job_analysis_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_job_analysis_cache_provider ON job_analysis_cache(llm_provider);

-- Job analysis history table for tracking and metrics
CREATE TABLE IF NOT EXISTS job_analysis_history (
    id SERIAL PRIMARY KEY,
    analysis_id UUID UNIQUE NOT NULL,
    user_id VARCHAR(100),
    job_title VARCHAR(500),
    company_name VARCHAR(200),
    analysis_depth VARCHAR(20) DEFAULT 'standard',
    status VARCHAR(20) NOT NULL,
    processing_time_ms FLOAT,
    llm_provider VARCHAR(50),
    tokens_used INTEGER,
    skills_extracted INTEGER DEFAULT 0,
    skills_matched INTEGER DEFAULT 0,
    cache_hit BOOLEAN DEFAULT FALSE,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for analysis history
CREATE INDEX IF NOT EXISTS idx_job_analysis_history_user ON job_analysis_history(user_id);
CREATE INDEX IF NOT EXISTS idx_job_analysis_history_status ON job_analysis_history(status);
CREATE INDEX IF NOT EXISTS idx_job_analysis_history_provider ON job_analysis_history(llm_provider);
CREATE INDEX IF NOT EXISTS idx_job_analysis_history_created ON job_analysis_history(created_at);

-- Skills extraction tracking table
CREATE TABLE IF NOT EXISTS job_analysis_cache_skills (
    id SERIAL PRIMARY KEY,
    cache_id INTEGER REFERENCES job_analysis_cache(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    skill_category VARCHAR(50),
    skill_type VARCHAR(50),
    importance VARCHAR(20),
    confidence_score FLOAT,
    is_matched BOOLEAN DEFAULT FALSE,
    matched_skill_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for skills tracking
CREATE INDEX IF NOT EXISTS idx_job_analysis_cache_skills_name ON job_analysis_cache_skills(skill_name);
CREATE INDEX IF NOT EXISTS idx_job_analysis_cache_skills_category ON job_analysis_cache_skills(skill_category);
CREATE INDEX IF NOT EXISTS idx_job_analysis_cache_skills_type ON job_analysis_cache_skills(skill_type);

-- User skills table for gap analysis (if not exists)
CREATE TABLE IF NOT EXISTS user_skills (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    proficiency_level VARCHAR(20) DEFAULT 'beginner', -- beginner, intermediate, advanced, expert
    years_experience INTEGER DEFAULT 0,
    confidence_score FLOAT,
    last_practiced DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, skill_name)
);

-- Index for user skills
CREATE INDEX IF NOT EXISTS idx_user_skills_user_id ON user_skills(user_id);
CREATE INDEX IF NOT EXISTS idx_user_skills_name ON user_skills(skill_name);
CREATE INDEX IF NOT EXISTS idx_user_skills_level ON user_skills(proficiency_level);

-- Training recommendations tracking
CREATE TABLE IF NOT EXISTS training_recommendations (
    id SERIAL PRIMARY KEY,
    analysis_id UUID REFERENCES job_analysis_history(analysis_id),
    user_id VARCHAR(100),
    skill_name VARCHAR(100) NOT NULL,
    skill_category VARCHAR(50),
    priority VARCHAR(20) NOT NULL, -- high, medium, low
    difficulty_level VARCHAR(20) NOT NULL, -- beginner, intermediate, advanced
    estimated_duration VARCHAR(50),
    recommended_actions JSONB,
    learning_resources JSONB,
    success_metrics JSONB,
    status VARCHAR(20) DEFAULT 'pending', -- pending, in_progress, completed, skipped
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for training recommendations
CREATE INDEX IF NOT EXISTS idx_training_recommendations_analysis ON training_recommendations(analysis_id);
CREATE INDEX IF NOT EXISTS idx_training_recommendations_user ON training_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_training_recommendations_skill ON training_recommendations(skill_name);
CREATE INDEX IF NOT EXISTS idx_training_recommendations_priority ON training_recommendations(priority);
CREATE INDEX IF NOT EXISTS idx_training_recommendations_status ON training_recommendations(status);

-- Bulk analysis tracking
CREATE TABLE IF NOT EXISTS bulk_job_analyses (
    id SERIAL PRIMARY KEY,
    batch_id UUID UNIQUE NOT NULL,
    user_id VARCHAR(100),
    total_jobs INTEGER NOT NULL,
    successful_analyses INTEGER DEFAULT 0,
    failed_analyses INTEGER DEFAULT 0,
    processing_time_ms FLOAT,
    total_tokens_used INTEGER,
    status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Index for bulk analyses
CREATE INDEX IF NOT EXISTS idx_bulk_job_analyses_batch ON bulk_job_analyses(batch_id);
CREATE INDEX IF NOT EXISTS idx_bulk_job_analyses_user ON bulk_job_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_bulk_job_analyses_status ON bulk_job_analyses(status);

-- Analysis metrics materialized view for performance
CREATE MATERIALIZED VIEW IF NOT EXISTS job_analysis_metrics AS
SELECT 
    COUNT(*) as total_analyses,
    COUNT(*) FILTER (WHERE status = 'completed') as successful_analyses,
    COUNT(*) FILTER (WHERE status = 'failed') as failed_analyses,
    COUNT(*) FILTER (WHERE cache_hit = true) as cache_hits,
    COUNT(*) FILTER (WHERE cache_hit = false) as cache_misses,
    AVG(processing_time_ms) as avg_processing_time_ms,
    SUM(tokens_used) as total_tokens_used,
    date_trunc('day', created_at) as analysis_date
FROM job_analysis_history
GROUP BY date_trunc('day', created_at)
ORDER BY analysis_date DESC;

-- Index for metrics view
CREATE INDEX IF NOT EXISTS idx_job_analysis_metrics_date ON job_analysis_metrics(analysis_date);

-- Function to refresh metrics view
CREATE OR REPLACE FUNCTION refresh_job_analysis_metrics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY job_analysis_metrics;
END;
$$ LANGUAGE plpgsql;

-- Function to clean up expired cache entries
CREATE OR REPLACE FUNCTION cleanup_expired_cache()
RETURNS integer AS $$
DECLARE
    deleted_count integer;
BEGIN
    DELETE FROM job_analysis_cache WHERE expires_at < CURRENT_TIMESTAMP;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to get skill statistics
CREATE OR REPLACE FUNCTION get_skill_analysis_stats()
RETURNS TABLE (
    skill_name text,
    analysis_count bigint,
    avg_confidence float,
    match_rate float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.skill_name::text,
        COUNT(*)::bigint as analysis_count,
        AVG(s.confidence_score)::float as avg_confidence,
        (COUNT(*) FILTER (WHERE s.is_matched = true)::float / COUNT(*)::float)::float as match_rate
    FROM job_analysis_cache_skills s
    GROUP BY s.skill_name
    ORDER BY analysis_count DESC
    LIMIT 50;
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE job_analysis_cache IS 'Caches job analysis results to avoid repeated LLM calls';
COMMENT ON TABLE job_analysis_history IS 'Tracks all job analysis operations for metrics and debugging';
COMMENT ON TABLE job_analysis_cache_skills IS 'Tracks individual skills extracted from cached analyses';
COMMENT ON TABLE user_skills IS 'Stores user skill proficiency levels for gap analysis';
COMMENT ON TABLE training_recommendations IS 'Tracks training recommendations generated from job analyses';
COMMENT ON TABLE bulk_job_analyses IS 'Tracks bulk job analysis operations';
COMMENT ON MATERIALIZED VIEW job_analysis_metrics IS 'Aggregated metrics for job analysis operations';

COMMENT ON FUNCTION cleanup_expired_cache() IS 'Removes expired cache entries to keep the cache table clean';
COMMENT ON FUNCTION get_skill_analysis_stats() IS 'Returns statistics about skills found in job analyses';
COMMENT ON FUNCTION refresh_job_analysis_metrics() IS 'Refreshes the materialized view with latest metrics';
-- Create tables for Interview Trainer application
-- This script creates all necessary tables based on the Pydantic schemas

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE difficulty_level AS ENUM ('beginner', 'intermediate', 'advanced');
CREATE TYPE question_type AS ENUM ('theoretical', 'practical', 'behavioral', 'technical', 'situational', 'coding', 'system_design');
CREATE TYPE skill_type AS ENUM ('programming', 'framework', 'database', 'devops', 'soft_skill', 'system_design', 'algorithms', 'testing', 'architecture', 'tools');

-- Create users table (for future use)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create skills table
CREATE TABLE IF NOT EXISTS skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    type skill_type NOT NULL,
    proficiency VARCHAR(100) NOT NULL,
    years_of_experience INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT[] NOT NULL,
    skills TEXT[] NOT NULL,
    tech_stack TEXT[] NOT NULL,
    location VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    level VARCHAR(100) NOT NULL,
    salary_range VARCHAR(100),
    is_remote BOOLEAN DEFAULT FALSE,
    progress INTEGER CHECK (progress >= 0 AND progress <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create questions table
CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    text TEXT NOT NULL,
    type question_type NOT NULL,
    difficulty difficulty_level NOT NULL,
    category VARCHAR(255) NOT NULL,
    sample_answer TEXT,
    tips TEXT[],
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create exercises table
CREATE TABLE IF NOT EXISTS exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    difficulty difficulty_level NOT NULL,
    category VARCHAR(255) NOT NULL,
    programming_language VARCHAR(100),
    requirements TEXT[],
    code TEXT,
    solution TEXT,
    hints TEXT[],
    time_limit INTEGER,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create skill_cards table (for training display)
CREATE TABLE IF NOT EXISTS skill_cards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type skill_type NOT NULL,
    questions_completed INTEGER DEFAULT 0 CHECK (questions_completed >= 0),
    questions_total INTEGER DEFAULT 0 CHECK (questions_total >= 0),
    exercises_completed INTEGER DEFAULT 0 CHECK (exercises_completed >= 0),
    exercises_total INTEGER DEFAULT 0 CHECK (exercises_total >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create dashboard_stats table
CREATE TABLE IF NOT EXISTS dashboard_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    active_jobs INTEGER DEFAULT 0 CHECK (active_jobs >= 0),
    questions_completed INTEGER DEFAULT 0 CHECK (questions_completed >= 0),
    avg_progress INTEGER DEFAULT 0 CHECK (avg_progress >= 0 AND avg_progress <= 100),
    success_rate INTEGER DEFAULT 0 CHECK (success_rate >= 0 AND success_rate <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create skill_distribution_data table
CREATE TABLE IF NOT EXISTS skill_distribution_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    value INTEGER NOT NULL CHECK (value >= 0),
    color VARCHAR(7) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create performance_data table
CREATE TABLE IF NOT EXISTS performance_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    difficulty difficulty_level NOT NULL,
    success INTEGER DEFAULT 0 CHECK (success >= 0),
    failure INTEGER DEFAULT 0 CHECK (failure >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create llm_config table
CREATE TABLE IF NOT EXISTS llm_config (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    api_key VARCHAR(255) NOT NULL,
    model VARCHAR(100) NOT NULL,
    temperature DECIMAL(3,2) DEFAULT 0.7 CHECK (temperature >= 0.0 AND temperature <= 2.0),
    max_tokens INTEGER DEFAULT 2000 CHECK (max_tokens > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create junction tables for many-to-many relationships

-- Questions-Skills relationship
CREATE TABLE IF NOT EXISTS question_skills (
    question_id UUID REFERENCES questions(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, skill_id)
);

-- Exercises-Skills relationship
CREATE TABLE IF NOT EXISTS exercise_skills (
    exercise_id UUID REFERENCES exercises(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (exercise_id, skill_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(category);
CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);
CREATE INDEX IF NOT EXISTS idx_exercises_category ON exercises(category);
CREATE INDEX IF NOT EXISTS idx_exercises_difficulty ON exercises(difficulty);
CREATE INDEX IF NOT EXISTS idx_skills_type ON skills(type);
CREATE INDEX IF NOT EXISTS idx_skill_cards_name ON skill_cards(name);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_questions_updated_at BEFORE UPDATE ON questions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_exercises_updated_at BEFORE UPDATE ON exercises
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_skills_updated_at BEFORE UPDATE ON skills
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_skill_cards_updated_at BEFORE UPDATE ON skill_cards
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_llm_config_updated_at BEFORE UPDATE ON llm_config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

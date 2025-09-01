-- Sample data for Interview Trainer application
-- This script inserts sample data into all tables for development and testing purposes

-- Insert sample dashboard stats
INSERT INTO dashboard_stats (id, active_jobs, questions_completed, avg_progress, success_rate)
VALUES 
    (uuid_generate_v4(), 2, 1, 53, 78)
ON CONFLICT DO NOTHING;

-- Insert sample jobs
INSERT INTO jobs (id, title, company, description, requirements, skills, tech_stack, location, type, level, salary_range, is_remote, progress, created_at, updated_at)
VALUES 
    (
        uuid_generate_v4(),
        'Senior Frontend Developer',
        'TechCorp',
        'We are looking for a Senior Frontend Developer to join our team and help build amazing user experiences.',
        ARRAY['5+ years of frontend development experience', 'Strong knowledge of React and TypeScript', 'Experience with modern frontend tooling'],
        ARRAY['React', 'TypeScript', 'JavaScript', 'CSS', 'HTML'],
        ARRAY['React', 'TypeScript'],
        'Remote Friendly',
        'Full-time',
        'Senior',
        '$90k - $120k',
        true,
        65,
        '2024-01-15T00:00:00Z'::timestamp with time zone,
        '2024-01-15T00:00:00Z'::timestamp with time zone
    ),
    (
        uuid_generate_v4(),
        'Full Stack Engineer',
        'StartupXYZ',
        'Join our fast-growing startup as a Full Stack Engineer and help us build the next big thing.',
        ARRAY['3+ years of full stack development', 'Experience with Python and Django', 'Knowledge of modern web technologies'],
        ARRAY['Python', 'Django', 'JavaScript', 'SQL', 'AWS'],
        ARRAY['Python', 'Django'],
        'Fully Remote',
        'Full-time',
        'Mid-level',
        '$80k - $110k',
        true,
        40,
        '2024-01-10T00:00:00Z'::timestamp with time zone,
        '2024-01-10T00:00:00Z'::timestamp with time zone
    )
ON CONFLICT DO NOTHING;

-- Insert sample skill distribution data
INSERT INTO skill_distribution_data (id, name, value, color)
VALUES 
    (uuid_generate_v4(), 'Frontend', 35, '#f97316'),
    (uuid_generate_v4(), 'Backend', 25, '#14b8a6'),
    (uuid_generate_v4(), 'Full Stack', 20, '#1e40af'),
    (uuid_generate_v4(), 'DevOps', 12, '#eab308'),
    (uuid_generate_v4(), 'Data Science', 8, '#06b6d4')
ON CONFLICT DO NOTHING;

-- Insert sample performance data
INSERT INTO performance_data (id, difficulty, success, failure)
VALUES 
    (uuid_generate_v4(), 'beginner', 12, 3),
    (uuid_generate_v4(), 'intermediate', 6, 4),
    (uuid_generate_v4(), 'advanced', 2, 4)
ON CONFLICT DO NOTHING;

-- Insert sample skill cards
INSERT INTO skill_cards (id, name, type, questions_completed, questions_total, exercises_completed, exercises_total, created_at, updated_at)
VALUES 
    (uuid_generate_v4(), 'JavaScript', 'programming', 7, 12, 4, 8, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'System Design', 'system_design', 4, 10, 0, 0, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Team Leadership', 'soft_skill', 5, 9, 0, 0, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'React', 'framework', 9, 15, 6, 10, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Communication', 'soft_skill', 8, 14, 0, 0, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Node.js', 'framework', 6, 11, 3, 9, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'TypeScript', 'programming', 3, 8, 2, 5, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Problem Solving', 'algorithms', 10, 16, 7, 12, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'API Design', 'architecture', 2, 7, 1, 4, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone)
ON CONFLICT DO NOTHING;

-- Insert sample questions for JavaScript
INSERT INTO questions (id, text, type, difficulty, category, is_completed, created_at, updated_at)
VALUES 
    (uuid_generate_v4(), 'Explain the difference between let, const, and var in JavaScript.', 'theoretical', 'beginner', 'JavaScript', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'What are closures in JavaScript and how do they work?', 'theoretical', 'intermediate', 'JavaScript', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Explain the event loop in JavaScript and how it handles asynchronous operations.', 'theoretical', 'advanced', 'JavaScript', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone)
ON CONFLICT DO NOTHING;

-- Insert sample questions for React
INSERT INTO questions (id, text, type, difficulty, category, is_completed, created_at, updated_at)
VALUES 
    (uuid_generate_v4(), 'What is the difference between state and props in React?', 'theoretical', 'beginner', 'React', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Explain the React component lifecycle methods.', 'theoretical', 'intermediate', 'React', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'What are React hooks and how do they work?', 'theoretical', 'intermediate', 'React', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone)
ON CONFLICT DO NOTHING;

-- Insert sample questions for System Design
INSERT INTO questions (id, text, type, difficulty, category, is_completed, created_at, updated_at)
VALUES 
    (uuid_generate_v4(), 'What are the key considerations when designing a scalable system?', 'theoretical', 'intermediate', 'System Design', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Explain the CAP theorem and its implications for distributed systems.', 'theoretical', 'advanced', 'System Design', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone)
ON CONFLICT DO NOTHING;

-- Insert sample exercises for JavaScript
INSERT INTO exercises (id, title, description, difficulty, category, is_completed, created_at, updated_at)
VALUES 
    (uuid_generate_v4(), 'Implement a debounce function', 'Create a debounce function that delays the execution of a function until after a specified delay has elapsed since the last time it was invoked.', 'intermediate', 'JavaScript', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Array flattening', 'Write a function that flattens a nested array to a single level.', 'beginner', 'JavaScript', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Promise.all implementation', 'Implement your own version of Promise.all that handles an array of promises.', 'advanced', 'JavaScript', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone)
ON CONFLICT DO NOTHING;

-- Insert sample exercises for React
INSERT INTO exercises (id, title, description, difficulty, category, is_completed, created_at, updated_at)
VALUES 
    (uuid_generate_v4(), 'Custom hook for form handling', 'Create a custom React hook that manages form state and validation.', 'intermediate', 'React', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Context API implementation', 'Implement a theme switcher using React Context API.', 'beginner', 'React', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone)
ON CONFLICT DO NOTHING;

-- Insert sample exercises for Problem Solving
INSERT INTO exercises (id, title, description, difficulty, category, is_completed, created_at, updated_at)
VALUES 
    (uuid_generate_v4(), 'Two Sum', 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.', 'beginner', 'Algorithms', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone),
    (uuid_generate_v4(), 'Valid Parentheses', 'Given a string s containing just the characters ''('', '')'', ''{'', ''}'', ''['' and '']'', determine if the input string is valid.', 'intermediate', 'Algorithms', false, '2024-01-15T00:00:00Z'::timestamp with time zone, '2024-01-15T00:00:00Z'::timestamp with time zone)
ON CONFLICT DO NOTHING;

-- Insert sample LLM configuration
INSERT INTO llm_config (id, api_key, model, temperature, max_tokens)
VALUES 
    (uuid_generate_v4(), 'sample-api-key', 'gpt-4', 0.7, 2000)
ON CONFLICT DO NOTHING;

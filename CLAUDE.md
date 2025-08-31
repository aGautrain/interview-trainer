# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interview Trainer is a fullstack application that helps users prepare for job interviews by analyzing job requirements and generating custom questions and coding exercises. It runs locally with LLM integration for personalized content generation.

## Architecture

- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI (Python) with modular route organization
- **Database**: PostgreSQL (containerized)
- **Development**: Docker Compose for database, direct execution for services

## Development Commands

### Frontend Development

```bash
# From frontend/ directory
npm run dev          # Start development server (port 5173)
npm run build        # Build for production (TypeScript compilation + Vite)
npm run test         # Run Vitest tests
npm run test:coverage # Run tests with coverage report
npm run lint         # ESLint with TypeScript support
npm run lint:fix     # Fix linting issues automatically
```

### Backend Development

```bash
# From backend/ directory
uvicorn main:app --reload    # Start FastAPI server (port 8000)
python -m pytest            # Run tests (if test files exist)
```

### Database Management

```bash
# Start PostgreSQL container
docker-compose -f docker-compose.postgres.yml up -d

# From database/ directory
python manage_db.py status     # Check database connection and stats
python manage_db.py schema     # View table structure
python manage_db.py reset      # Reset all data (preserves schema)
python populate_sample_data.py # Populate with sample data
```

## Code Architecture

### Backend Structure (FastAPI)

The backend uses a modular route organization pattern:

- `main.py` - Application entry point with CORS configuration
- `routes/` - Organized by domain:
  - `dashboard.py` - Dashboard statistics and data
  - `jobs.py` - Job-related endpoints
  - `skills.py` - Skills and training endpoints
  - `legacy.py` - Backward compatibility endpoints
- `schemas/` - Pydantic models for request/response validation
- `sample_data.py` - Mock data for development

Key API endpoints:

- `GET /dashboard` - Complete dashboard data
- `GET /jobs` - Available jobs
- `GET /skills` - Available skills
- `GET /skills/{skill}/questions` - Questions for specific skill
- `GET /skills/{skill}/exercises` - Exercises for specific skill

### Frontend Structure (React + TypeScript)

The frontend follows a component-based architecture:

- `App.tsx` - Main router with route definitions
- `pages/` - Page components:
  - `HomePage.tsx` - Landing page
  - `JobTargeting.tsx` - Job analysis interface
  - `JobTraining.tsx` - Job-specific training
  - `SkillTraining.tsx` - Skill-focused training
- `components/` - Reusable UI components
- `services/` - API integration layer
  - `api.ts` - Base API configuration
  - `dashboardService.ts` - Dashboard data fetching

### Database Schema

PostgreSQL database with tables for:

- Core entities: users, skills, jobs, questions, exercises
- Training data: skill_cards, question_skills, exercise_skills
- Dashboard metrics: dashboard_stats, skill_distribution_data, performance_data
- Configuration: user_preferences, llm_config

## Development Workflow

### Commit Convention

All commits must follow Conventional Commits 1.0.0:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

Format: `<type>[optional scope]: <description>`

### Service Integration

- Backend runs on port 8000 with auto-reload
- Frontend runs on port 5173 with Vite HMR
- CORS configured for localhost:5173 and localhost:3000
- Database runs in Docker on port 5432 (configurable)

### Key Dependencies

**Frontend:**

- React 19 with React Router for navigation
- Headless UI + Heroicons for accessible components
- Axios for API communication
- React Hook Form for form handling
- Recharts for data visualization
- Vitest + Testing Library for testing

**Backend:**

- FastAPI 0.104.1 with Uvicorn server
- Pydantic 2.5.0 for data validation
- Modular route organization for maintainability

### Testing Strategy

- Frontend: Vitest with React Testing Library
- Backend: FastAPI test client (pytest framework ready)
- Database: Management utilities for development data

## Important Notes

- The application is in active development with some routes marked "Coming Soon"
- Database population scripts provide realistic sample data
- Frontend includes a DebugButton component for development assistance
- Environment configuration uses .env files (never commit these)
- All services support hot reload for efficient development

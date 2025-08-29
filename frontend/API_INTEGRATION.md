# Frontend API Integration

This document describes the changes made to integrate the frontend with the backend API endpoints.

## Changes Made

### 1. Type System Updates

- Updated all type definitions in `src/types/index.ts` to match backend schemas exactly
- Consolidated types from separate files into the main types file
- Updated enums to match backend values:
  - `DifficultyLevel`: `beginner`, `intermediate`, `advanced`
  - `QuestionType`: `theoretical`, `practical`, `behavioral`, `technical`, `situational`, `coding`, `system_design`
  - `SkillType`: `programming`, `framework`, `database`, `devops`, `soft_skill`, `system_design`, `algorithms`, `testing`, `architecture`, `tools`

### 2. API Services Created

- `src/services/api.ts` - Base API service with HTTP methods
- `src/services/dashboardService.ts` - Dashboard data endpoints
- `src/services/jobsService.ts` - Job-related endpoints
- `src/services/skillsService.ts` - Skills and training endpoints
- `src/services/index.ts` - Service exports

### 3. Component Updates

- **HomePage**: Now fetches real dashboard data from `/dashboard` endpoint
- **JobTraining**: Fetches real skills data from `/skills` endpoint
- **SkillTraining**: Receives real questions and exercises data via navigation state
- **QuestionCard & ExerciseCard**: Updated to use new difficulty values and type structure

### 4. Removed Mocked Data

- Replaced all hardcoded sample data with API calls
- Added proper loading states and error handling
- Implemented retry mechanisms for failed API calls

## API Endpoints Used

### Dashboard

- `GET /dashboard` - Complete dashboard data
- `GET /dashboard/stats` - Dashboard statistics only

### Jobs

- `GET /jobs` - All available jobs
- `GET /jobs/{job_id}` - Specific job by ID

### Skills & Training

- `GET /skills` - All available skills
- `GET /skills/{skill_name}/questions` - Questions for a specific skill
- `GET /skills/{skill_name}/exercises` - Exercises for a specific skill

## Error Handling

- Loading states with spinners for all async operations
- Error states with retry buttons
- Graceful fallbacks when API calls fail
- Console logging for debugging

## Type Safety

- All API responses are properly typed using TypeScript interfaces
- Consistent type usage across components
- Proper error handling for type mismatches

## Usage

1. Start the backend: `cd backend && uvicorn main:app --reload`
2. Start the frontend: `cd frontend && npm run dev`
3. The frontend will automatically connect to `http://localhost:8000`

## Notes

- The backend currently uses sample data, but the frontend is ready for real data
- All components now handle loading and error states properly
- Type definitions are synchronized with backend schemas
- The integration follows React best practices with proper state management

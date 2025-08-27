// Core types for the Interview Trainer application

export interface JobPosting {
  id: string;
  title: string;
  company: string;
  description: string;
  requirements: string[];
  skills: Skill[];
  location: string;
  type: "full-time" | "part-time" | "contract" | "internship";
  level: "entry" | "mid" | "senior" | "lead";
  createdAt: string;
  updatedAt: string;
}

export interface Skill {
  id: string;
  name: string;
  category:
    | "programming"
    | "framework"
    | "database"
    | "cloud"
    | "tool"
    | "soft-skill"
    | "other";
  proficiency: "beginner" | "intermediate" | "advanced" | "expert";
  yearsOfExperience?: number;
}

export interface Question {
  id: string;
  text: string;
  type: "behavioral" | "technical" | "situational" | "coding" | "system-design";
  difficulty: "beginner" | "intermediate" | "advanced";
  category: string;
  skills: Skill[];
  sampleAnswer?: string;
  tips?: string[];
  createdAt: string;
}

export interface CodingExercise {
  id: string;
  title: string;
  description: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  programmingLanguage: string;
  skills: Skill[];
  requirements: string[];
  testCases?: TestCase[];
  solution?: string;
  hints?: string[];
  timeLimit?: number; // in minutes
  createdAt: string;
}

export interface TestCase {
  input: string;
  expectedOutput: string;
  description?: string;
}

export interface UserSession {
  id: string;
  apiKey: string;
  model: string;
  preferences: UserPreferences;
  createdAt: string;
  updatedAt: string;
}

export interface UserPreferences {
  defaultDifficulty: "beginner" | "intermediate" | "advanced";
  preferredLanguages: string[];
  questionTypes: string[];
  theme: "light" | "dark" | "auto";
}

export interface GenerationHistory {
  id: string;
  type: "job-analysis" | "question-generation" | "exercise-generation";
  input: any;
  output: any;
  model: string;
  tokensUsed: number;
  duration: number;
  createdAt: string;
}

export interface LLMConfig {
  apiKey: string;
  model: string;
  temperature: number;
  maxTokens: number;
}

export interface JobAnalysisResult {
  skills: Skill[];
  requirements: string[];
  summary: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  estimatedExperience: string;
  recommendations: string[];
}

export interface QuestionGenerationRequest {
  skills: Skill[];
  type: string;
  difficulty: string;
  count: number;
  context?: string;
}

export interface ExerciseGenerationRequest {
  skills: Skill[];
  language: string;
  difficulty: string;
  count: number;
  focus?: string;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  hasNext: boolean;
  hasPrev: boolean;
}

// Form types
export interface JobAnalysisForm {
  title: string;
  company: string;
  description: string;
  requirements: string;
}

export interface QuestionForm {
  skills: string[];
  type: string;
  difficulty: string;
  count: number;
  context: string;
}

export interface ExerciseForm {
  skills: string[];
  language: string;
  difficulty: string;
  count: number;
  focus: string;
}

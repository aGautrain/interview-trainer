// Core types for the Interview Trainer application - Updated to match backend schemas

// Base types matching backend schemas
export interface BaseSchema {
  id: string;
  createdAt: string;
  updatedAt?: string;
}

export enum DifficultyLevel {
  BEGINNER = "beginner",
  INTERMEDIATE = "intermediate",
  ADVANCED = "advanced",
}

export enum QuestionType {
  THEORETICAL = "theoretical",
  PRACTICAL = "practical",
  BEHAVIORAL = "behavioral",
  TECHNICAL = "technical",
  SITUATIONAL = "situational",
  CODING = "coding",
  SYSTEM_DESIGN = "system_design",
}

export enum SkillType {
  PROGRAMMING = "programming",
  FRAMEWORK = "framework",
  DATABASE = "database",
  DEVOPS = "devops",
  SOFT_SKILL = "soft_skill",
  SYSTEM_DESIGN = "system_design",
  ALGORITHMS = "algorithms",
  TESTING = "testing",
  ARCHITECTURE = "architecture",
  TOOLS = "tools",
}

export interface Skill {
  id: string;
  name: string;
  category: string;
  type: SkillType;
  proficiency: string;
  yearsOfExperience?: number;
}

// Job types matching backend schemas
export interface Job {
  id: string;
  title: string;
  company: string;
  description: string;
  requirements: string[];
  skills: string[];
  techStack: string[];
  location: string;
  type: string;
  level: string;
  salaryRange?: string;
  isRemote: boolean;
  progress?: number;
  createdAt: string;
  updatedAt: string;
}

export interface JobAnalysisResult {
  skills: Skill[];
  requirements: string[];
  summary: string;
  difficulty: string;
  estimatedExperience: string;
  recommendations: string[];
}

export interface JobAnalysisForm {
  title: string;
  company: string;
  description: string;
  requirements: string;
}

// Training types matching backend schemas
export interface Question {
  id: string;
  text: string;
  type: QuestionType;
  difficulty: DifficultyLevel;
  category: string;
  skills: Skill[];
  sampleAnswer?: string;
  tips?: string[];
  isCompleted: boolean;
  createdAt: string;
}

export interface Exercise {
  id: string;
  title: string;
  description: string;
  difficulty: DifficultyLevel;
  category: string;
  programmingLanguage?: string;
  skills: Skill[];
  requirements?: string[];
  code?: string;
  solution?: string;
  hints?: string[];
  timeLimit?: number;
  isCompleted: boolean;
  createdAt: string;
}

export interface TestCase {
  input: string;
  expectedOutput: string;
  description?: string;
}

export interface SkillCard {
  name: string;
  type: SkillType;
  questionsCompleted: number;
  questionsTotal: number;
  exercisesCompleted: number;
  exercisesTotal: number;
}

export interface SkillTrainingProgress {
  skillId: string;
  skillName: string;
  questionsCompleted: number;
  questionsTotal: number;
  exercisesCompleted: number;
  exercisesTotal: number;
  progressPercentage: number;
}

export interface SkillTrainingSession {
  id: string;
  skillId: string;
  userId: string;
  startTime: string;
  endTime?: string;
  questionsAnswered: number;
  exercisesCompleted: number;
  score?: number;
}

export interface SkillTrainingData {
  skill: SkillCard;
  questions: Question[];
  exercises: Exercise[];
}

// Dashboard types matching backend schemas
export interface DashboardStats {
  activeJobs: number;
  questionsCompleted: number;
  avgProgress: number;
  successRate: number;
}

export interface SkillDistributionData {
  name: string;
  value: number;
  color: string;
}

export interface PerformanceData {
  difficulty: string;
  success: number;
  failure: number;
}

export interface DashboardData {
  stats: DashboardStats;
  jobs: Job[];
  skillDistributionData: SkillDistributionData[];
  performanceData: PerformanceData[];
}

// User and session types
export interface UserSession {
  id: string;
  apiKey: string;
  model: string;
  createdAt: string;
  updatedAt: string;
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

// Form types
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

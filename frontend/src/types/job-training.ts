// Job training types - Updated to match backend schemas
// Note: These types are now also exported from the main types file

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

export interface SkillCard {
  name: string;
  type: SkillType;
  questionsCompleted: number;
  questionsTotal: number;
  exercisesCompleted: number;
  exercisesTotal: number;
}

export interface Question {
  id: string;
  text: string;
  type:
    | "theoretical"
    | "practical"
    | "behavioral"
    | "technical"
    | "situational"
    | "coding"
    | "system_design";
  difficulty: "beginner" | "intermediate" | "advanced";
  category: string;
  skills: any[];
  sampleAnswer?: string;
  tips?: string[];
  isCompleted: boolean;
  createdAt: string;
}

export interface Exercise {
  id: string;
  title: string;
  description: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  category: string;
  programmingLanguage?: string;
  skills: any[];
  requirements?: string[];
  code?: string;
  solution?: string;
  hints?: string[];
  timeLimit?: number;
  isCompleted: boolean;
  createdAt: string;
}

export interface SkillTrainingData {
  skill: SkillCard;
  questions: Question[];
  exercises: Exercise[];
}

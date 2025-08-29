// Skill type enum for categorizing different types of skills
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
  type: "theoretical" | "practical";
  difficulty: "easy" | "medium" | "hard";
  category: string;
  answer?: string;
  isCompleted: boolean;
}

export interface Exercise {
  id: string;
  title: string;
  description: string;
  difficulty: "easy" | "medium" | "hard";
  category: string;
  code?: string;
  isCompleted: boolean;
}

export interface SkillTrainingData {
  skill: SkillCard;
  questions: Question[];
  exercises: Exercise[];
}

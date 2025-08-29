// Skills service for calling skills and training-related backend endpoints

import apiService from "./api";
import { SkillCard, Question, Exercise } from "../types";

export class SkillsService {
  /**
   * Get all available skills
   */
  async getSkills(): Promise<SkillCard[]> {
    return apiService.get<SkillCard[]>("/skills");
  }

  /**
   * Get questions for a specific skill
   */
  async getSkillQuestions(skillName: string): Promise<Question[]> {
    return apiService.get<Question[]>(`/skills/${skillName}/questions`);
  }

  /**
   * Get exercises for a specific skill
   */
  async getSkillExercises(skillName: string): Promise<Exercise[]> {
    return apiService.get<Exercise[]>(`/skills/${skillName}/exercises`);
  }
}

export const skillsService = new SkillsService();
export default skillsService;

/**
 * Job Analysis Service
 * 
 * Provides TypeScript interfaces and API service functions for job analysis operations.
 * Handles job description analysis, skill extraction, and training recommendations
 * with comprehensive error handling and type safety.
 */

import apiService from './api';

// Enums matching backend models
export enum AnalysisStatus {
  PENDING = "pending",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
  FAILED = "failed",
  CACHED = "cached"
}

export enum SkillImportance {
  CRITICAL = "critical",
  IMPORTANT = "important",
  PREFERRED = "preferred",
  NICE_TO_HAVE = "nice_to_have"
}

export enum TrainingPriority {
  HIGH = "high",
  MEDIUM = "medium",
  LOW = "low"
}

export enum DifficultyLevel {
  BEGINNER = "beginner",
  INTERMEDIATE = "intermediate",
  ADVANCED = "advanced",
  EXPERT = "expert"
}

export enum SkillType {
  PROGRAMMING_LANGUAGE = "programming_language",
  FRAMEWORK = "framework",
  LIBRARY = "library",
  DATABASE = "database",
  TOOL = "tool",
  CLOUD_PLATFORM = "cloud_platform",
  SOFT_SKILL = "soft_skill",
  DOMAIN_KNOWLEDGE = "domain_knowledge",
  CERTIFICATION = "certification",
  OTHER = "other"
}

// Request/Response interfaces
export interface JobAnalysisRequest {
  job_description: string;
  job_title?: string;
  company_name?: string;
  company_context?: string;
  analysis_depth?: 'basic' | 'standard' | 'comprehensive';
  user_id?: string;
}

export interface ExtractedSkillEnhanced {
  name: string;
  category: string;
  skill_type?: SkillType;
  importance: SkillImportance;
  years_required?: number;
  context?: string;
  confidence_score: number;
  synonyms: string[];
  related_skills: string[];
}

export interface SkillMatch {
  extracted_skill: ExtractedSkillEnhanced;
  matched_skill_id?: string;
  matched_skill_name?: string;
  match_confidence: number;
  match_type: string;
  is_new_skill: boolean;
}

export interface SkillGapAnalysis {
  skill_name: string;
  required_level: string;
  current_level?: string;
  gap_severity: TrainingPriority;
  estimated_study_time?: number;
}

export interface TrainingRecommendation {
  skill_name: string;
  skill_category: string;
  priority: TrainingPriority;
  recommended_actions: string[];
  estimated_duration?: string;
  difficulty_level: DifficultyLevel;
  prerequisite_skills: string[];
  learning_resources: string[];
  success_metrics: string[];
}

export interface JobAnalysisResult {
  // Basic job information
  job_title?: string;
  company_name?: string;
  industry: string;
  
  // Core analysis
  key_requirements: string[];
  extracted_skills: ExtractedSkillEnhanced[];
  skill_matches: SkillMatch[];
  
  // Analysis insights
  experience_level: string;
  difficulty_assessment: DifficultyLevel;
  role_summary: string;
  compensation_insights?: string;
  
  // Recommendations
  training_recommendations: TrainingRecommendation[];
  skill_gaps: SkillGapAnalysis[];
  readiness_score?: number;
  
  // Metadata
  analysis_metadata: Record<string, any>;
}

export interface JobAnalysisResponse {
  success: boolean;
  status: AnalysisStatus;
  result?: JobAnalysisResult;
  error_message?: string;
  processing_time_ms?: number;
  llm_provider?: string;
  tokens_used?: number;
  cache_hit: boolean;
  analysis_id: string;
}

// Error types
export interface JobAnalysisError {
  message: string;
  status?: number;
  code?: string;
  details?: Record<string, any>;
}

// Service state types
export interface JobAnalysisState {
  isLoading: boolean;
  error: JobAnalysisError | null;
  result: JobAnalysisResult | null;
  analysisId?: string;
}

/**
 * Job Analysis API Service Class
 */
class JobAnalysisService {
  private readonly baseUrl = '/job-analysis';

  /**
   * Analyze a job description
   */
  async analyzeJob(request: JobAnalysisRequest): Promise<JobAnalysisResponse> {
    try {
      const response = await apiService.post<JobAnalysisResponse>(
        `${this.baseUrl}/analyze`,
        request
      );
      
      return response;
    } catch (error) {
      throw this.handleError(error, 'Failed to analyze job description');
    }
  }

  /**
   * Extract skills from text content
   */
  async extractSkills(
    text: string, 
    contextType: string = 'job_description'
  ): Promise<ExtractedSkillEnhanced[]> {
    try {
      if (!text.trim()) {
        throw new Error('Text content cannot be empty');
      }

      const response = await apiService.post<ExtractedSkillEnhanced[]>(
        `${this.baseUrl}/extract-skills?context_type=${encodeURIComponent(contextType)}`,
        text
      );
      
      return response;
    } catch (error) {
      throw this.handleError(error, 'Failed to extract skills from text');
    }
  }

  /**
   * Get training recommendations for a specific analysis
   */
  async getTrainingRecommendations(
    analysisId: string,
    userId?: string
  ): Promise<TrainingRecommendation[]> {
    try {
      const params = new URLSearchParams();
      if (userId) {
        params.append('user_id', userId);
      }
      
      const url = `${this.baseUrl}/recommendations/${analysisId}${params.toString() ? `?${params.toString()}` : ''}`;
      
      const response = await apiService.get<TrainingRecommendation[]>(url);
      return response;
    } catch (error) {
      throw this.handleError(error, 'Failed to get training recommendations');
    }
  }

  /**
   * Get analysis service health status
   */
  async getHealthStatus(): Promise<Record<string, any>> {
    try {
      const response = await apiService.get<Record<string, any>>(`${this.baseUrl}/health`);
      return response;
    } catch (error) {
      throw this.handleError(error, 'Failed to get service health status');
    }
  }

  /**
   * Handle and format errors consistently
   */
  private handleError(error: any, defaultMessage: string): JobAnalysisError {
    if (error instanceof Error) {
      // Check if it's an HTTP error with status
      const httpError = error as any;
      if (httpError.response) {
        return {
          message: httpError.response.data?.detail || httpError.response.data?.message || defaultMessage,
          status: httpError.response.status,
          details: httpError.response.data
        };
      }
      
      return {
        message: error.message || defaultMessage,
        details: { originalError: error }
      };
    }

    return {
      message: defaultMessage,
      details: { error }
    };
  }

  /**
   * Validate job analysis request
   */
  validateJobAnalysisRequest(request: Partial<JobAnalysisRequest>): JobAnalysisError[] {
    const errors: JobAnalysisError[] = [];

    if (!request.job_description?.trim()) {
      errors.push({
        message: 'Job description is required',
        code: 'MISSING_JOB_DESCRIPTION'
      });
    }

    if (request.job_description && request.job_description.length < 50) {
      errors.push({
        message: 'Job description should be at least 50 characters long',
        code: 'JOB_DESCRIPTION_TOO_SHORT'
      });
    }

    if (request.analysis_depth && !['basic', 'standard', 'comprehensive'].includes(request.analysis_depth)) {
      errors.push({
        message: 'Invalid analysis depth. Must be basic, standard, or comprehensive',
        code: 'INVALID_ANALYSIS_DEPTH'
      });
    }

    return errors;
  }
}

// Export service instance
export const jobAnalysisService = new JobAnalysisService();
export default jobAnalysisService;

// Utility functions for working with analysis results
export const analysisUtils = {
  /**
   * Get skills grouped by importance level
   */
  getSkillsByImportance(skills: ExtractedSkillEnhanced[]): Record<SkillImportance, ExtractedSkillEnhanced[]> {
    return skills.reduce((groups, skill) => {
      if (!groups[skill.importance]) {
        groups[skill.importance] = [];
      }
      groups[skill.importance].push(skill);
      return groups;
    }, {} as Record<SkillImportance, ExtractedSkillEnhanced[]>);
  },

  /**
   * Get skills grouped by category
   */
  getSkillsByCategory(skills: ExtractedSkillEnhanced[]): Record<string, ExtractedSkillEnhanced[]> {
    return skills.reduce((groups, skill) => {
      if (!groups[skill.category]) {
        groups[skill.category] = [];
      }
      groups[skill.category].push(skill);
      return groups;
    }, {} as Record<string, ExtractedSkillEnhanced[]>);
  },

  /**
   * Calculate average confidence score
   */
  getAverageConfidence(skills: ExtractedSkillEnhanced[]): number {
    if (skills.length === 0) return 0;
    const total = skills.reduce((sum, skill) => sum + skill.confidence_score, 0);
    return total / skills.length;
  },

  /**
   * Get high priority training recommendations
   */
  getHighPriorityRecommendations(recommendations: TrainingRecommendation[]): TrainingRecommendation[] {
    return recommendations.filter(rec => rec.priority === TrainingPriority.HIGH);
  },

  /**
   * Format experience level for display
   */
  formatExperienceLevel(level: string): string {
    return level.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
  },

  /**
   * Get difficulty color class for UI
   */
  getDifficultyColorClass(difficulty: DifficultyLevel): string {
    switch (difficulty) {
      case DifficultyLevel.BEGINNER:
        return 'text-green-600 bg-green-50';
      case DifficultyLevel.INTERMEDIATE:
        return 'text-yellow-600 bg-yellow-50';
      case DifficultyLevel.ADVANCED:
        return 'text-orange-600 bg-orange-50';
      case DifficultyLevel.EXPERT:
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  },

  /**
   * Get importance color class for UI
   */
  getImportanceColorClass(importance: SkillImportance): string {
    switch (importance) {
      case SkillImportance.CRITICAL:
        return 'text-red-700 bg-red-50 border-red-200';
      case SkillImportance.IMPORTANT:
        return 'text-orange-700 bg-orange-50 border-orange-200';
      case SkillImportance.PREFERRED:
        return 'text-blue-700 bg-blue-50 border-blue-200';
      case SkillImportance.NICE_TO_HAVE:
        return 'text-gray-700 bg-gray-50 border-gray-200';
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  }
};
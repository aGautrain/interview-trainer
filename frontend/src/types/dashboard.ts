// Dashboard types - Updated to match backend schemas
// Note: These types are now also exported from the main types file

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

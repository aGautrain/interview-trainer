export interface Job {
  id: string;
  title: string;
  company: string;
  salaryRange: string;
  location: string;
  techStack: string[];
  progress: number;
  isRemote: boolean;
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

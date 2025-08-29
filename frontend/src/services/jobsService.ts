// Jobs service for calling job-related backend endpoints

import apiService from "./api";
import { Job } from "../types";

export class JobsService {
  /**
   * Get all available jobs
   */
  async getJobs(): Promise<Job[]> {
    return apiService.get<Job[]>("/jobs");
  }

  /**
   * Get a specific job by ID
   */
  async getJob(jobId: string): Promise<Job> {
    return apiService.get<Job>(`/jobs/${jobId}`);
  }
}

export const jobsService = new JobsService();
export default jobsService;

// Dashboard service for calling dashboard-related backend endpoints

import apiService from "./api";
import { DashboardData, DashboardStats } from "../types";

export class DashboardService {
  /**
   * Get complete dashboard data
   */
  async getDashboardData(): Promise<DashboardData> {
    return apiService.get<DashboardData>("/dashboard");
  }

  /**
   * Get dashboard statistics only
   */
  async getDashboardStats(): Promise<DashboardStats> {
    return apiService.get<DashboardStats>("/dashboard/stats");
  }
}

export const dashboardService = new DashboardService();
export default dashboardService;

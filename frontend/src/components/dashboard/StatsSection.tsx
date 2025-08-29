import {
  BriefcaseIcon,
  CheckCircleIcon,
  ClockIcon,
} from "@heroicons/react/24/outline";
import StatCard from "./StatCard";

import { DashboardStats } from "../../types/dashboard";

interface StatsSectionProps {
  stats: DashboardStats;
}

const StatsSection = ({ stats }: StatsSectionProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatCard
        icon={BriefcaseIcon}
        title="Active Jobs"
        value={stats.activeJobs}
        color="#3b82f6"
      />
      <StatCard
        icon={CheckCircleIcon}
        title="Questions Completed"
        value={stats.questionsCompleted}
        color="#10b981"
      />
      <StatCard
        icon={ClockIcon}
        title="Avg Progress"
        value={stats.avgProgress}
        color="#f59e0b"
        animateValue={true}
        isPercentage={true}
      />
      <StatCard
        icon={ClockIcon}
        title="Success Rate"
        value={stats.successRate}
        color="#8b5cf6"
        animateValue={true}
        isPercentage={true}
      />
    </div>
  );
};

export default StatsSection;

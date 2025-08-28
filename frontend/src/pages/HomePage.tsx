import { useState } from "react";
import {
  DashboardLayout,
  WelcomeSection,
  StatsSection,
  JobTargetsSection,
  ChartsSection,
} from "../components/dashboard";
import { Job, DashboardStats } from "../types/dashboard";

const HomePage = () => {
  const [stats] = useState<DashboardStats>({
    activeJobs: 2,
    questionsCompleted: 1,
    avgProgress: 53,
    successRate: 78,
  });

  const [jobs] = useState<Job[]>([
    {
      id: "1",
      title: "Senior Frontend Developer",
      company: "TechCorp",
      salaryRange: "$90k - $120k",
      location: "Remote Friendly",
      techStack: ["React", "TypeScript"],
      progress: 65,
      isRemote: true,
    },
    {
      id: "2",
      title: "Full Stack Engineer",
      company: "StartupXYZ",
      salaryRange: "$80k - $110k",
      location: "Fully Remote",
      techStack: ["Python", "Django"],
      progress: 40,
      isRemote: true,
    },
  ]);

  const skillDistributionData = [
    { name: "Frontend", value: 35, color: "#f97316" },
    { name: "Backend", value: 25, color: "#14b8a6" },
    { name: "Full Stack", value: 20, color: "#1e40af" },
    { name: "DevOps", value: 12, color: "#eab308" },
    { name: "Data Science", value: 8, color: "#06b6d4" },
  ];

  const performanceData = [
    { difficulty: "Easy", success: 12, failure: 3 },
    { difficulty: "Medium", success: 6, failure: 4 },
    { difficulty: "Hard", success: 2, failure: 4 },
  ];

  return (
    <DashboardLayout>
      <WelcomeSection />
      <StatsSection stats={stats} />
      <JobTargetsSection jobs={jobs} />
      <ChartsSection
        skillDistributionData={skillDistributionData}
        performanceData={performanceData}
      />
    </DashboardLayout>
  );
};

export default HomePage;

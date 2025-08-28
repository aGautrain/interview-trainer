import { useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import {
  BriefcaseIcon,
  CheckCircleIcon,
  ClockIcon,
  PlusIcon,
  ArrowDownTrayIcon,
  MapPinIcon,
  CodeBracketIcon,
} from "@heroicons/react/24/outline";

interface JobTarget {
  id: string;
  title: string;
  company: string;
  salaryRange: string;
  location: string;
  techStack: string[];
  progress: number;
  isRemote: boolean;
}

interface DashboardStats {
  activeJobs: number;
  questionsCompleted: number;
  avgProgress: number;
  successRate: number;
}

const HomePage = () => {
  const [stats] = useState<DashboardStats>({
    activeJobs: 2,
    questionsCompleted: 1,
    avgProgress: 53,
    successRate: 78,
  });

  const [jobTargets] = useState<JobTarget[]>([
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

  const StatCard = ({
    icon: Icon,
    title,
    value,
    color,
  }: {
    icon: any;
    title: string;
    value: string | number;
    color: string;
  }) => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center space-x-3">
        <div
          className="p-3 rounded-lg"
          style={{ backgroundColor: `${color}20` }}
        >
          <Icon className="w-6 h-6" style={{ color }} />
        </div>
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  );

  const JobTargetCard = ({ job }: { job: JobTarget }) => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {job.title}
          </h3>
          <p className="text-gray-600 mb-2">({job.company})</p>
          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
            <span className="font-medium">{job.salaryRange}</span>
            <div className="flex items-center space-x-1">
              <MapPinIcon className="w-4 h-4" />
              <span>{job.location}</span>
            </div>
          </div>
        </div>
        <button className="btn-primary text-sm px-4 py-2">Practice →</button>
      </div>

      <div className="flex items-center space-x-3 mb-4">
        <div className="flex items-center space-x-2">
          <CodeBracketIcon className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">Tech Stack:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {job.techStack.map((tech, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-md"
            >
              {tech}
            </span>
          ))}
          {job.techStack.length > 2 && (
            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-md">
              +{job.techStack.length - 2}
            </span>
          )}
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Progress</span>
          <span className="font-medium text-gray-900">{job.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${job.progress}%` }}
          />
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg flex items-center justify-center">
              <BriefcaseIcon className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold text-gray-900">InterviewAce</h1>
          </div>
          <nav className="flex space-x-8">
            <a
              href="#"
              className="text-primary-600 border-b-2 border-primary-600 pb-2 font-medium"
            >
              Dashboard
            </a>
            <a
              href="#"
              className="text-gray-500 hover:text-gray-700 pb-2 font-medium"
            >
              Job Targeting
            </a>
          </nav>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back!
          </h2>
          <p className="text-gray-600 text-lg">
            Track your interview preparation progress and practice questions.
          </p>
        </div>

        {/* Summary Cards */}
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
            value={`${stats.avgProgress}%`}
            color="#f59e0b"
          />
          <StatCard
            icon={ClockIcon}
            title="Success Rate"
            value={`${stats.successRate}%`}
            color="#8b5cf6"
          />
        </div>

        {/* Job Targets Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-1">
                Job Targets
              </h3>
              <p className="text-gray-600">
                Manage your target positions and track preparation progress.
              </p>
            </div>
            <div className="flex space-x-3">
              <button className="btn-secondary flex items-center space-x-2">
                <ArrowDownTrayIcon className="w-4 h-4" />
                <span>Export to CSV</span>
              </button>
              <button className="btn-primary flex items-center space-x-2">
                <PlusIcon className="w-4 h-4" />
                <span>Add New Job Target</span>
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {jobTargets.map((job) => (
              <JobTargetCard key={job.id} job={job} />
            ))}
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Question Distribution by Skills */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Question Distribution by Skills
            </h3>
            <p className="text-gray-600 text-sm mb-6">
              Overview of questions practiced across different skill areas.
            </p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={skillDistributionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {skillDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value, name) => [`${value}%`, name]}
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #e5e7eb",
                      borderRadius: "8px",
                      boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex flex-wrap justify-center gap-4 mt-4">
              {skillDistributionData.map((item) => (
                <div key={item.name} className="flex items-center space-x-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="text-sm text-gray-600">
                    {item.name}: {item.value}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Performance by Difficulty */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Performance by Difficulty
            </h3>
            <p className="text-gray-600 text-sm mb-6">
              Success and failure rates across question difficulty levels.
            </p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={performanceData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                  <XAxis
                    dataKey="difficulty"
                    axisLine={false}
                    tickLine={false}
                    tick={{ fontSize: 12, fill: "#6b7280" }}
                  />
                  <YAxis
                    axisLine={false}
                    tickLine={false}
                    tick={{ fontSize: 12, fill: "#6b7280" }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #e5e7eb",
                      borderRadius: "8px",
                      boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                    }}
                  />
                  <Bar
                    dataKey="success"
                    fill="#14b8a6"
                    radius={[4, 4, 0, 0]}
                    name="Success"
                  />
                  <Bar
                    dataKey="failure"
                    fill="#f97316"
                    radius={[4, 4, 0, 0]}
                    name="Failure"
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-center space-x-6 mt-4">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-teal-500 rounded-full" />
                <span className="text-sm text-gray-600">Success</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-orange-500 rounded-full" />
                <span className="text-sm text-gray-600">Failure</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

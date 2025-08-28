import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layouts/DashboardLayout";
import { Job } from "../types/dashboard";

// Skill type enum for categorizing different types of skills
enum SkillType {
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

interface SkillCard {
  name: string;
  type: SkillType;
  questionsCompleted: number;
  questionsTotal: number;
  exercisesCompleted: number;
  exercisesTotal: number;
}

// Placeholder job for when none is selected
const placeholderJob: Job = {
  id: "placeholder",
  title: "Select a Job to Train For",
  company: "Choose from your job targets",
  salaryRange: "Not specified",
  location: "Not specified",
  techStack: ["Select a job first"],
  progress: 0,
  isRemote: false,
};

const JobTraining = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedJob, setSelectedJob] = useState<Job>(placeholderJob);
  const [isPlaceholderMode, setIsPlaceholderMode] = useState(true);
  const [skills] = useState<SkillCard[]>([
    {
      name: "JavaScript",
      type: SkillType.PROGRAMMING,
      questionsCompleted: 7,
      questionsTotal: 12,
      exercisesCompleted: 4,
      exercisesTotal: 8,
    },
    {
      name: "System Design",
      type: SkillType.SYSTEM_DESIGN,
      questionsCompleted: 4,
      questionsTotal: 10,
      exercisesCompleted: 0,
      exercisesTotal: 0,
    },
    {
      name: "Team Leadership",
      type: SkillType.SOFT_SKILL,
      questionsCompleted: 5,
      questionsTotal: 9,
      exercisesCompleted: 0,
      exercisesTotal: 0,
    },
    {
      name: "React",
      type: SkillType.FRAMEWORK,
      questionsCompleted: 9,
      questionsTotal: 15,
      exercisesCompleted: 6,
      exercisesTotal: 10,
    },
    {
      name: "Communication",
      type: SkillType.SOFT_SKILL,
      questionsCompleted: 8,
      questionsTotal: 14,
      exercisesCompleted: 0,
      exercisesTotal: 0,
    },
    {
      name: "Node.js",
      type: SkillType.FRAMEWORK,
      questionsCompleted: 6,
      questionsTotal: 11,
      exercisesCompleted: 3,
      exercisesTotal: 9,
    },
    {
      name: "TypeScript",
      type: SkillType.PROGRAMMING,
      questionsCompleted: 3,
      questionsTotal: 8,
      exercisesCompleted: 2,
      exercisesTotal: 5,
    },
    {
      name: "Problem Solving",
      type: SkillType.ALGORITHMS,
      questionsCompleted: 10,
      questionsTotal: 16,
      exercisesCompleted: 7,
      exercisesTotal: 12,
    },
    {
      name: "API Design",
      type: SkillType.ARCHITECTURE,
      questionsCompleted: 2,
      questionsTotal: 7,
      exercisesCompleted: 1,
      exercisesTotal: 4,
    },
  ]);

  useEffect(() => {
    const jobFromState = location.state?.selectedJob;
    if (jobFromState) {
      setSelectedJob(jobFromState);
      setIsPlaceholderMode(false);
    } else {
      // Instead of redirecting, use placeholder job
      setSelectedJob(placeholderJob);
      setIsPlaceholderMode(true);
    }
  }, [location.state]);

  const calculateProgress = (completed: number, total: number) => {
    if (total === 0) return 0;
    return Math.round((completed / total) * 100);
  };

  const handleSelectJob = () => {
    navigate("/");
  };

  const handleCreateJob = () => {
    navigate("/job-targeting");
  };

  return (
    <DashboardLayout>
      {/* Header Section */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Practice by Skills
            </h1>
            <p className="text-lg text-gray-600">
              Select questions or coding exercises for specific skills
            </p>
          </div>
          <button
            onClick={() => navigate("/")}
            className="btn-secondary flex items-center space-x-2"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>

      {/* Job Card */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              {selectedJob.title}
            </h2>
            <p className="text-gray-600 mb-3">
              {selectedJob.company} • {selectedJob.salaryRange} •{" "}
              {selectedJob.location}
            </p>
            {isPlaceholderMode ? (
              <div className="space-y-4">
                <p className="text-gray-700">
                  No job selected for training. Choose an existing job target or
                  create a new one to get started.
                </p>
                <div className="flex space-x-3">
                  <button
                    onClick={handleSelectJob}
                    className="btn-primary px-4 py-2 text-sm"
                  >
                    Select Existing Job
                  </button>
                  <button
                    onClick={handleCreateJob}
                    className="btn-secondary px-4 py-2 text-sm"
                  >
                    Create New Job Target
                  </button>
                </div>
              </div>
            ) : (
              <p className="text-gray-700">
                We are looking for a senior frontend developer with React
                experience.
              </p>
            )}
          </div>
          <div className="flex flex-wrap gap-2 ml-4">
            {selectedJob.techStack.map((skill) => (
              <span
                key={skill}
                className={`px-3 py-1 text-sm font-medium rounded-full ${
                  isPlaceholderMode
                    ? "bg-gray-100 text-gray-500"
                    : "bg-primary-100 text-primary-800"
                }`}
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Skills Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {skills.map((skill) => (
          <div
            key={skill.name}
            className={`bg-white rounded-lg shadow-sm border border-gray-200 p-6 transition-shadow ${
              isPlaceholderMode
                ? "opacity-60 cursor-not-allowed"
                : "hover:shadow-md cursor-pointer"
            }`}
            onClick={!isPlaceholderMode ? () => {} : undefined}
          >
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {skill.name}
              </h3>
            </div>

            {/* Questions Progress */}
            <div className="mb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Questions
                </span>
                <span className="text-sm text-gray-500">
                  {skill.questionsCompleted}/{skill.questionsTotal}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{
                    width: `${calculateProgress(
                      skill.questionsCompleted,
                      skill.questionsTotal
                    )}%`,
                  }}
                ></div>
              </div>
              <span className="text-xs text-gray-500 mt-1 block">
                {calculateProgress(
                  skill.questionsCompleted,
                  skill.questionsTotal
                )}
                % complete
              </span>
            </div>

            {/* Coding Exercises Progress */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Coding Exercises
                </span>
                {skill.exercisesTotal > 0 ? (
                  <span className="text-sm text-gray-500">
                    {skill.exercisesCompleted}/{skill.exercisesTotal}
                  </span>
                ) : (
                  <span className="text-sm text-gray-400">
                    No coding exercises
                  </span>
                )}
              </div>
              {skill.exercisesTotal > 0 ? (
                <>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-green-600 h-2 rounded-full transition-all duration-300"
                      style={{
                        width: `${calculateProgress(
                          skill.exercisesCompleted,
                          skill.exercisesTotal
                        )}%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-xs text-gray-500 mt-1 block">
                    {calculateProgress(
                      skill.exercisesCompleted,
                      skill.exercisesTotal
                    )}
                    % complete
                  </span>
                </>
              ) : (
                <p className="text-sm text-gray-400 italic">
                  No coding exercises for this skill
                </p>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Placeholder Mode Overlay */}
      {isPlaceholderMode && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md mx-4 text-center">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              Select a Job to Start Training
            </h3>
            <p className="text-gray-600 mb-6">
              Choose an existing job target or create a new one to begin your
              skill training.
            </p>
            <div className="flex flex-col space-y-3">
              <button
                onClick={handleSelectJob}
                className="btn-primary w-full py-3"
              >
                Go to Dashboard
              </button>
              <button
                onClick={handleCreateJob}
                className="btn-secondary w-full py-3"
              >
                Create New Job Target
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
};

export default JobTraining;

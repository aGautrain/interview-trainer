import { Job } from "../../types/dashboard";

interface JobCardProps {
  job: Job;
  isPlaceholderMode: boolean;
  onSelectJob: () => void;
  onCreateJob: () => void;
}

const JobCard = ({
  job,
  isPlaceholderMode,
  onSelectJob,
  onCreateJob,
}: JobCardProps) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            {job.title}
          </h2>
          <p className="text-gray-600 mb-3">
            {job.company} • {job.salaryRange} • {job.location}
          </p>
          {isPlaceholderMode ? (
            <div className="space-y-4">
              <p className="text-gray-700">
                No job selected for training. Choose an existing job target or
                create a new one to get started.
              </p>
              <div className="flex space-x-3">
                <button
                  onClick={onSelectJob}
                  className="btn-primary px-4 py-2 text-sm"
                >
                  Select Existing Job
                </button>
                <button
                  onClick={onCreateJob}
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
          {job.techStack.map((skill) => (
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
  );
};

export default JobCard;

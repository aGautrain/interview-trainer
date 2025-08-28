import { MapPinIcon, CodeBracketIcon } from "@heroicons/react/24/outline";
import { useNavigate } from "react-router-dom";

import { Job } from "../../types/dashboard";

interface JobCardProps {
  job: Job;
}

const JobCard = ({ job }: JobCardProps) => {
  const navigate = useNavigate();

  const handlePractice = () => {
    navigate("/job-training", { state: { selectedJob: job } });
  };

  return (
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
        <button
          onClick={handlePractice}
          className="btn-primary text-sm px-4 py-2"
        >
          Practice →
        </button>
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
};

export default JobCard;

import { ArrowDownTrayIcon, PlusIcon } from "@heroicons/react/24/outline";
import JobCard from "./JobCard";

import { Job } from "../../types/dashboard";

interface JobTargetsSectionProps {
  jobs: Job[];
}

const JobTargetsSection = ({ jobs }: JobTargetsSectionProps) => {
  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-1">Job Targets</h3>
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
            <span>Target New Job</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {jobs.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
};

export default JobTargetsSection;

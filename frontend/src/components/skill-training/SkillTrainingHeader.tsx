import { ArrowLeftIcon } from "@heroicons/react/24/outline";
import { SkillCard } from "../../types";
import { useNavigate } from "react-router-dom";

interface SkillTrainingHeaderProps {
  skill: SkillCard;
  selectedJob: any;
}

const SkillTrainingHeader = ({
  skill,
  selectedJob,
}: SkillTrainingHeaderProps) => {
  const navigate = useNavigate();

  const handleBackClick = () => {
    navigate("/job-training", {
      state: {
        selectedJob: selectedJob,
      },
    });
  };

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {skill.name}
          </h1>
          <p className="text-lg text-gray-600">
            Master {skill.name} through questions and exercises
          </p>
        </div>
        <button
          onClick={handleBackClick}
          className="btn-secondary flex items-center space-x-2"
        >
          ← Back to Job Training
        </button>
      </div>
    </div>
  );
};

export default SkillTrainingHeader;

interface JobTrainingHeaderProps {
  onBackClick: () => void;
}

const JobTrainingHeader = ({ onBackClick }: JobTrainingHeaderProps) => {
  return (
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
          onClick={onBackClick}
          className="btn-secondary flex items-center space-x-2"
        >
          ← Back to Dashboard
        </button>
      </div>
    </div>
  );
};

export default JobTrainingHeader;

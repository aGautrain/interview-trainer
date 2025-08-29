interface ProgressBarProps {
  currentIndex: number;
  totalCount: number;
  color?: string;
}

const ProgressBar = ({
  currentIndex,
  totalCount,
  color = "bg-primary-600",
}: ProgressBarProps) => {
  const progressPercentage = ((currentIndex + 1) / totalCount) * 100;

  return (
    <div className="mt-4">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700">Progress</span>
        <span className="text-sm text-gray-500">
          {currentIndex + 1}/{totalCount}
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`${color} h-2 rounded-full transition-all duration-300`}
          style={{ width: `${progressPercentage}%` }}
        ></div>
      </div>
    </div>
  );
};

export default ProgressBar;

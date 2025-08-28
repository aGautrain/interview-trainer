import { TagIcon } from "@heroicons/react/24/outline";

interface AnalyzeButtonProps {
  onAnalyze: () => void;
  disabled?: boolean;
}

const AnalyzeButton = ({ onAnalyze, disabled = false }: AnalyzeButtonProps) => {
  return (
    <div className="flex justify-center">
      <button
        onClick={onAnalyze}
        disabled={disabled}
        className="flex items-center space-x-2 px-8 py-4 bg-gray-800 text-white rounded-lg hover:bg-gray-900 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <TagIcon className="w-5 h-5" />
        <span>Analyze Job</span>
      </button>
    </div>
  );
};

export default AnalyzeButton;

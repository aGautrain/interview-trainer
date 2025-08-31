import { TagIcon, ArrowPathIcon } from "@heroicons/react/24/outline";

interface AnalyzeButtonProps {
  onAnalyze: () => void;
  disabled?: boolean;
  isLoading?: boolean;
}

const AnalyzeButton = ({ onAnalyze, disabled = false, isLoading = false }: AnalyzeButtonProps) => {
  return (
    <div className="flex justify-center">
      <button
        onClick={onAnalyze}
        disabled={disabled || isLoading}
        className={`
          flex items-center space-x-2 px-8 py-4 rounded-lg font-medium transition-all duration-200
          ${isLoading 
            ? 'bg-blue-600 text-white cursor-wait' 
            : 'bg-gray-800 text-white hover:bg-gray-900'
          }
          disabled:opacity-50 disabled:cursor-not-allowed
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
        `}
      >
        {isLoading ? (
          <>
            <ArrowPathIcon className="w-5 h-5 animate-spin" />
            <span>Analyzing...</span>
          </>
        ) : (
          <>
            <TagIcon className="w-5 h-5" />
            <span>Analyze Job</span>
          </>
        )}
      </button>
      
      {isLoading && (
        <div className="mt-3 text-center">
          <div className="text-sm text-gray-600 mb-2">
            Processing job description with AI...
          </div>
          <div className="flex justify-center">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalyzeButton;

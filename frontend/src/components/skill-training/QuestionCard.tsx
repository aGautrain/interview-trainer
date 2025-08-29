import { CheckIcon, ArrowLeftIcon } from "@heroicons/react/24/outline";
import { Question } from "../../types/job-training";
import ProgressBar from "./ProgressBar";

interface QuestionCardProps {
  question: Question;
  currentIndex: number;
  totalCount: number;
  onSubmit: () => void;
  onPrevious: () => void;
}

const QuestionCard = ({
  question,
  currentIndex,
  totalCount,
  onSubmit,
  onPrevious,
}: QuestionCardProps) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "easy":
        return "bg-green-100 text-green-800";
      case "medium":
        return "bg-yellow-100 text-yellow-800";
      case "hard":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Theoretical Questions
        </h2>
        <p className="text-gray-600">
          Question {currentIndex + 1} of {totalCount}
        </p>
        <ProgressBar currentIndex={currentIndex} totalCount={totalCount} />
      </div>

      <div className="bg-gray-50 rounded-lg p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Question {currentIndex + 1}
            </h3>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium ${getDifficultyColor(
              question.difficulty
            )}`}
          >
            {question.difficulty.charAt(0).toUpperCase() +
              question.difficulty.slice(1)}
          </span>
        </div>

        <p className="text-gray-900 text-lg mb-6">{question.text}</p>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Answer
          </label>
          <textarea
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 resize-none"
            rows={6}
            placeholder="Type your answer here..."
            defaultValue={question.answer || ""}
          />
        </div>

        <div className="flex space-x-3">
          {currentIndex > 0 && (
            <button
              onClick={onPrevious}
              className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 transition-colors flex items-center justify-center"
            >
              <ArrowLeftIcon className="w-5 h-5" />
            </button>
          )}
          <button
            onClick={onSubmit}
            className="bg-gray-800 text-white px-6 py-2 rounded-md hover:bg-gray-700 transition-colors flex items-center"
          >
            <CheckIcon className="w-5 h-5 mr-2" />
            Submit Answer
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuestionCard;

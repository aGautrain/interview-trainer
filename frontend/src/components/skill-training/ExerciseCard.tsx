import { CheckIcon, ArrowLeftIcon } from "@heroicons/react/24/outline";
import { Exercise } from "../../types";
import ProgressBar from "./ProgressBar";

interface ExerciseCardProps {
  exercise: Exercise;
  currentIndex: number;
  totalCount: number;
  onReset: () => void;
  onSubmit: () => void;
  onPrevious: () => void;
}

const ExerciseCard = ({
  exercise,
  currentIndex,
  totalCount,
  onSubmit,
  onPrevious,
}: ExerciseCardProps) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "beginner":
        return "bg-green-100 text-green-800";
      case "intermediate":
        return "bg-yellow-100 text-yellow-800";
      case "advanced":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Coding Exercises
        </h2>
        <p className="text-gray-600">
          Exercise {currentIndex + 1} of {totalCount}
        </p>
        <ProgressBar
          currentIndex={currentIndex}
          totalCount={totalCount}
          color="bg-green-600"
        />
      </div>

      <div className="bg-gray-50 rounded-lg p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Exercise {currentIndex + 1}
            </h3>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium ${getDifficultyColor(
              exercise.difficulty
            )}`}
          >
            {exercise.difficulty.charAt(0).toUpperCase() +
              exercise.difficulty.slice(1)}
          </span>
        </div>

        <h4 className="text-lg font-medium text-gray-900 mb-3">
          {exercise.title}
        </h4>
        <p className="text-gray-700 mb-6">{exercise.description}</p>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Code
          </label>
          <textarea
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 font-mono text-sm resize-none"
            rows={12}
            placeholder="Write your code here..."
            defaultValue={exercise.code || ""}
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
            className="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 transition-colors flex items-center"
          >
            <CheckIcon className="w-5 h-5 mr-2" />
            Submit Exercise
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExerciseCard;

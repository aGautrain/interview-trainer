import { SkillCard as SkillCardType } from "../../types";

interface SkillCardProps {
  skill: SkillCardType;
  isPlaceholderMode: boolean;
  onClick?: () => void;
}

const SkillCard = ({ skill, isPlaceholderMode, onClick }: SkillCardProps) => {
  const calculateProgress = (completed: number, total: number) => {
    if (total === 0) return 0;
    return Math.round((completed / total) * 100);
  };

  return (
    <div
      className={`bg-white rounded-lg shadow-sm border border-gray-200 p-6 transition-shadow ${
        isPlaceholderMode
          ? "opacity-60 cursor-not-allowed"
          : "hover:shadow-md cursor-pointer"
      }`}
      onClick={!isPlaceholderMode ? onClick : undefined}
    >
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{skill.name}</h3>
      </div>

      {/* Questions Progress */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Questions</span>
          <span className="text-sm text-gray-500">
            {skill.questionsCompleted}/{skill.questionsTotal}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{
              width: `${calculateProgress(
                skill.questionsCompleted,
                skill.questionsTotal
              )}%`,
            }}
          ></div>
        </div>
        <span className="text-xs text-gray-500 mt-1 block">
          {calculateProgress(skill.questionsCompleted, skill.questionsTotal)}%
          complete
        </span>
      </div>

      {/* Coding Exercises Progress */}
      <div>
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            Coding Exercises
          </span>
          {skill.exercisesTotal > 0 ? (
            <span className="text-sm text-gray-500">
              {skill.exercisesCompleted}/{skill.exercisesTotal}
            </span>
          ) : (
            <span className="text-sm text-gray-400">No coding exercises</span>
          )}
        </div>
        {skill.exercisesTotal > 0 ? (
          <>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-green-600 h-2 rounded-full transition-all duration-300"
                style={{
                  width: `${calculateProgress(
                    skill.exercisesCompleted,
                    skill.exercisesTotal
                  )}%`,
                }}
              ></div>
            </div>
            <span className="text-xs text-gray-500 mt-1 block">
              {calculateProgress(
                skill.exercisesCompleted,
                skill.exercisesTotal
              )}
              % complete
            </span>
          </>
        ) : (
          <p className="text-sm text-gray-400 italic">
            No coding exercises for this skill
          </p>
        )}
      </div>
    </div>
  );
};

export default SkillCard;

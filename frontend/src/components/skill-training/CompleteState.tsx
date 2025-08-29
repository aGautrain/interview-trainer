interface CompleteStateProps {
  activeTab: "questions" | "exercises";
  questionsCompleted: boolean;
  exercisesCompleted: boolean;
  availableQuestions: number;
  availableExercises: number;
  onSwitchTab: (tab: "questions" | "exercises") => void;
  onTrainAnotherSkill: () => void;
}

const CompleteState = ({
  activeTab,
  questionsCompleted,
  exercisesCompleted,
  availableQuestions,
  availableExercises,
  onSwitchTab,
  onTrainAnotherSkill,
}: CompleteStateProps) => {
  const bothCompleted = questionsCompleted && exercisesCompleted;
  const hasQuestions = availableQuestions > 0;
  const hasExercises = availableExercises > 0;

  const getCompletionMessage = () => {
    if (bothCompleted) {
      return {
        title: "Skill Mastered! 🎯",
        subtitle:
          "You've completed all questions and exercises for this skill!",
        description:
          "You're now proficient in this skill. Ready to tackle another one?",
        primaryAction: {
          text: "Train Another Skill",
          onClick: onTrainAnotherSkill,
          variant: "primary",
        },
      };
    }

    if (activeTab === "questions" && questionsCompleted) {
      if (hasExercises) {
        return {
          title: "Questions Complete! 📚",
          subtitle: "You've mastered the theoretical concepts!",
          description: `Great job! Now put your knowledge to the test with ${availableExercises} practical coding exercise${
            availableExercises > 1 ? "s" : ""
          }.`,
          primaryAction: {
            text: "Go to Exercises",
            onClick: () => onSwitchTab("exercises"),
            variant: "primary",
          },
        };
      } else {
        return {
          title: "Questions Complete! 📚",
          subtitle: "You've mastered the theoretical concepts!",
          description:
            "Excellent work! No coding exercises are available for this skill yet, but you've built a solid foundation.",
          primaryAction: {
            text: "Train Another Skill",
            onClick: onTrainAnotherSkill,
            variant: "primary",
          },
        };
      }
    }

    if (activeTab === "exercises" && exercisesCompleted) {
      if (hasQuestions) {
        return {
          title: "Exercises Complete! 💻",
          subtitle: "You've conquered the practical challenges!",
          description: `Excellent work! Consider reviewing ${availableQuestions} theoretical question${
            availableQuestions > 1 ? "s" : ""
          } to reinforce your understanding.`,
          primaryAction: {
            text: "Review Questions",
            onClick: () => onSwitchTab("questions"),
            variant: "primary",
          },
        };
      } else {
        return {
          title: "Exercises Complete! 💻",
          subtitle: "You've conquered the practical challenges!",
          description:
            "Great job! No theoretical questions are available for this skill yet, but you've mastered the practical aspects.",
          primaryAction: {
            text: "Train Another Skill",
            onClick: onTrainAnotherSkill,
            variant: "primary",
          },
        };
      }
    }

    return {
      title: "Congratulations! 🎉",
      subtitle: "You've completed this section!",
      description: "Keep up the great work!",
      primaryAction: {
        text: "Continue Learning",
        onClick: () =>
          onSwitchTab(activeTab === "questions" ? "exercises" : "questions"),
        variant: "secondary",
      },
    };
  };

  const message = getCompletionMessage();

  return (
    <div className="text-center py-12">
      <div className="text-green-500 mb-4">
        <svg
          className="mx-auto h-16 w-16"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </div>

      <h3 className="text-xl font-semibold text-gray-900 mb-3">
        {message.title}
      </h3>

      <p className="text-lg text-gray-700 mb-2">{message.subtitle}</p>

      <p className="text-gray-500 mb-6">{message.description}</p>

      {/* Progress Indicators */}
      <div className="flex justify-center space-x-8 mb-6">
        <div className="flex items-center">
          <div
            className={`w-3 h-3 rounded-full mr-2 ${
              questionsCompleted ? "bg-green-500" : "bg-gray-300"
            }`}
          ></div>
          <span
            className={`text-sm ${
              questionsCompleted
                ? "text-green-700 font-medium"
                : "text-gray-500"
            }`}
          >
            Questions {questionsCompleted ? "✓" : "○"} ({availableQuestions})
          </span>
        </div>
        <div className="flex items-center">
          <div
            className={`w-3 h-3 rounded-full mr-2 ${
              exercisesCompleted ? "bg-green-500" : "bg-gray-300"
            }`}
          ></div>
          <span
            className={`text-sm ${
              exercisesCompleted
                ? "text-green-700 font-medium"
                : "text-gray-500"
            }`}
          >
            Exercises {exercisesCompleted ? "✓" : "○"} ({availableExercises})
          </span>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3 justify-center">
        <button
          onClick={message.primaryAction.onClick}
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            message.primaryAction.variant === "primary"
              ? "bg-blue-600 text-white hover:bg-blue-700"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          {message.primaryAction.text}
        </button>
      </div>
    </div>
  );
};

export default CompleteState;

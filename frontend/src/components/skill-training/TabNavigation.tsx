interface TabNavigationProps {
  activeTab: "questions" | "exercises";
  setActiveTab: (tab: "questions" | "exercises") => void;
  questionsCount: number;
  exercisesCount: number;
}

const TabNavigation = ({
  activeTab,
  setActiveTab,
  questionsCount,
  exercisesCount,
}: TabNavigationProps) => {
  return (
    <div className="mb-6">
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab("questions")}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === "questions"
                ? "border-primary-600 text-primary-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            Theoretical Questions ({questionsCount})
          </button>
          <button
            onClick={() => setActiveTab("exercises")}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === "exercises"
                ? "border-primary-600 text-primary-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            Coding Exercises ({exercisesCount})
          </button>
        </nav>
      </div>
    </div>
  );
};

export default TabNavigation;

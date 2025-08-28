import {
  CheckCircleIcon,
  CodeBracketIcon,
  ChartBarIcon,
  AcademicCapIcon,
} from "@heroicons/react/24/outline";
import StatCard from "./StatCard";

interface ProgressSectionProps {
  questionsCompleted: number;
  questionsTotal: number;
  exercisesCompleted: number;
  exercisesTotal: number;
  skillsCompleted: number;
  skillsTotal: number;
}

const ProgressSection = ({
  questionsCompleted,
  questionsTotal,
  exercisesCompleted,
  exercisesTotal,
  skillsCompleted,
  skillsTotal,
}: ProgressSectionProps) => {
  const calculateOverallProgress = () => {
    const totalItems = questionsTotal + exercisesTotal;
    if (totalItems === 0) return 0;
    const completedItems = questionsCompleted + exercisesCompleted;
    return Math.round((completedItems / totalItems) * 100);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 mt-8">
      <StatCard
        icon={CheckCircleIcon}
        title="Questions Completed"
        value={`${questionsCompleted}/${questionsTotal}`}
        color="#10b981"
      />
      <StatCard
        icon={CodeBracketIcon}
        title="Coding Exercises"
        value={`${exercisesCompleted}/${exercisesTotal}`}
        color="#3b82f6"
      />
      <StatCard
        icon={AcademicCapIcon}
        title="Skills Completed"
        value={`${skillsCompleted}/${skillsTotal}`}
        color="#f59e0b"
      />
      <StatCard
        icon={ChartBarIcon}
        title="Overall Progress"
        value={`${calculateOverallProgress()}%`}
        color="#8b5cf6"
      />
    </div>
  );
};

export default ProgressSection;

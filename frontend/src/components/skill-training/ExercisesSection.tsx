import { Exercise } from "../../types/job-training";
import ExerciseCard from "./ExerciseCard";

interface ExercisesSectionProps {
  exercises: Exercise[];
  currentExerciseIndex: number;
  onSubmitExercise: () => void;
  onPreviousExercise: () => void;
}

const ExercisesSection = ({
  exercises,
  currentExerciseIndex,
  onSubmitExercise,
  onPreviousExercise,
}: ExercisesSectionProps) => {
  if (exercises.length === 0) {
    return null;
  }

  const currentExercise = exercises[currentExerciseIndex];

  return (
    <ExerciseCard
      exercise={currentExercise}
      currentIndex={currentExerciseIndex}
      totalCount={exercises.length}
      onSubmit={onSubmitExercise}
      onPrevious={onPreviousExercise}
    />
  );
};

export default ExercisesSection;

import { Exercise } from "../../types";
import ExerciseCard from "./ExerciseCard";

interface ExercisesSectionProps {
  exercises: Exercise[];
  currentExerciseIndex: number;
  onResetExercise: () => void;
  onSubmitExercise: () => void;
  onPreviousExercise: () => void;
}

const ExercisesSection = ({
  exercises,
  currentExerciseIndex,
  onResetExercise,
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
      onReset={onResetExercise}
      onSubmit={onSubmitExercise}
      onPrevious={onPreviousExercise}
    />
  );
};

export default ExercisesSection;

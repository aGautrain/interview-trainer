import { Question } from "../../types";
import QuestionCard from "./QuestionCard";

interface QuestionsSectionProps {
  questions: Question[];
  currentQuestionIndex: number;
  onSubmitAnswer: () => void;
  onPreviousQuestion: () => void;
}

const QuestionsSection = ({
  questions,
  currentQuestionIndex,
  onSubmitAnswer,
  onPreviousQuestion,
}: QuestionsSectionProps) => {
  if (questions.length === 0) {
    return null;
  }

  const currentQuestion = questions[currentQuestionIndex];

  return (
    <QuestionCard
      question={currentQuestion}
      currentIndex={currentQuestionIndex}
      totalCount={questions.length}
      onSubmit={onSubmitAnswer}
      onPrevious={onPreviousQuestion}
    />
  );
};

export default QuestionsSection;

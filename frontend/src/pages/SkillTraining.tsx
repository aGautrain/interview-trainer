import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layouts/DashboardLayout";
import {
  SkillTrainingHeader,
  TabNavigation,
  QuestionsSection,
  ExercisesSection,
  EmptyState,
  CompleteState,
} from "../components/skill-training";
import {
  Question,
  Exercise,
  SkillCard as SkillCardType,
} from "../types/job-training";

const SkillTraining = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [activeTab, setActiveTab] = useState<"questions" | "exercises">(
    "questions"
  );
  const [skillData, setSkillData] = useState<{
    skill: SkillCardType;
    questions: Question[];
    exercises: Exercise[];
  } | null>(null);
  const [selectedJob, setSelectedJob] = useState<any>(null);

  useEffect(() => {
    const dataFromState = location.state?.skillData;
    const jobFromState = location.state?.selectedJob;

    if (dataFromState) {
      setSkillData(dataFromState);
      setSelectedJob(jobFromState);
    } else {
      // Fallback to sample data if no state
      navigate("/job-training");
    }
  }, [location.state, navigate]);

  if (!skillData) {
    return (
      <DashboardLayout>
        <div className="text-center py-8">
          <p>Loading skill data...</p>
        </div>
      </DashboardLayout>
    );
  }

  const { skill, questions, exercises } = skillData;

  const handleResetQuestion = () => {
    // Reset current question progress
    console.log("Reset question:", questions[currentQuestionIndex].id);
  };

  const handleSubmitAnswer = () => {
    // Handle answer submission
    console.log(
      "Submit answer for question:",
      questions[currentQuestionIndex].id
    );

    if (currentQuestionIndex <= questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePreviousQuestion = () => {
    // Navigate to previous question
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleResetExercise = () => {
    // Reset current exercise progress
    console.log("Reset exercise:", exercises[currentExerciseIndex].id);
  };

  const handleSubmitExercise = () => {
    // Handle exercise submission
    console.log("Submit exercise:", exercises[currentExerciseIndex].id);

    if (currentExerciseIndex <= exercises.length - 1) {
      setCurrentExerciseIndex(currentExerciseIndex + 1);
    }
  };

  const handlePreviousExercise = () => {
    // Navigate to previous exercise
    if (currentExerciseIndex > 0) {
      setCurrentExerciseIndex(currentExerciseIndex - 1);
    }
  };

  const handleTrainAnotherSkill = () => {
    // Navigate to job training page while preserving the current job context
    // This allows the user to select another skill for the same job
    navigate("/job-training", {
      state: {
        selectedJob: selectedJob, // Preserve the current job
        fromSkillTraining: true, // Indicate we're coming from skill training
      },
    });
  };

  return (
    <DashboardLayout>
      <SkillTrainingHeader skill={skill} selectedJob={selectedJob} />

      <TabNavigation
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        questionsCount={questions.length}
        exercisesCount={exercises.length}
      />

      {/* Questions Section */}
      {activeTab === "questions" &&
        questions.length > 0 &&
        (currentQuestionIndex >= questions.length ? (
          <CompleteState
            activeTab={activeTab}
            questionsCompleted={currentQuestionIndex >= questions.length}
            exercisesCompleted={currentExerciseIndex >= exercises.length}
            availableQuestions={questions.length}
            availableExercises={exercises.length}
            onSwitchTab={setActiveTab}
            onTrainAnotherSkill={handleTrainAnotherSkill}
          />
        ) : (
          <QuestionsSection
            questions={questions}
            currentQuestionIndex={currentQuestionIndex}
            onSubmitAnswer={handleSubmitAnswer}
            onPreviousQuestion={handlePreviousQuestion}
          />
        ))}

      {/* Exercises Section */}
      {activeTab === "exercises" &&
        exercises.length > 0 &&
        (currentExerciseIndex >= exercises.length ? (
          <CompleteState
            activeTab={activeTab}
            questionsCompleted={currentQuestionIndex >= questions.length}
            exercisesCompleted={currentExerciseIndex >= exercises.length}
            availableQuestions={questions.length}
            availableExercises={exercises.length}
            onSwitchTab={setActiveTab}
            onTrainAnotherSkill={handleTrainAnotherSkill}
          />
        ) : (
          <ExercisesSection
            exercises={exercises}
            currentExerciseIndex={currentExerciseIndex}
            onResetExercise={handleResetExercise}
            onSubmitExercise={handleSubmitExercise}
            onPreviousExercise={handlePreviousExercise}
          />
        ))}

      {/* Empty State */}
      {((activeTab === "questions" && questions.length === 0) ||
        (activeTab === "exercises" && exercises.length === 0)) && (
        <EmptyState activeTab={activeTab} />
      )}
    </DashboardLayout>
  );
};

export default SkillTraining;

# Skill Training Components

This directory contains the components used by the SkillTraining page to provide a modular and maintainable structure.

## Components

### SkillTrainingHeader

Displays the skill name, description, and back button to return to job training.

**Props:**

- `skill: SkillCard` - The skill being trained
- `selectedJob: any` - The currently selected job

### TabNavigation

Handles switching between questions and exercises tabs.

**Props:**

- `activeTab: "questions" | "exercises"` - Currently active tab
- `setActiveTab: (tab: "questions" | "exercises") => void` - Function to change active tab
- `questionsCount: number` - Number of questions available
- `exercisesCount: number` - Number of exercises available

### ProgressBar

Reusable progress bar component showing current progress through questions or exercises.

**Props:**

- `currentIndex: number` - Current question/exercise index
- `totalCount: number` - Total number of questions/exercises
- `color?: string` - Optional color class for the progress bar (defaults to primary-600)

### QuestionCard

Displays individual questions with difficulty, category, and answer input.

**Props:**

- `question: Question` - The question to display
- `currentIndex: number` - Current question index
- `totalCount: number` - Total number of questions
- `onReset: () => void` - Function called when reset button is clicked
- `onSubmit: () => void` - Function called when submit button is clicked

### ExerciseCard

Displays individual exercises with difficulty, category, and code input.

**Props:**

- `question: Exercise` - The exercise to display
- `currentIndex: number` - Current exercise index
- `totalCount: number` - Total number of exercises
- `onReset: () => void` - Function called when reset button is clicked
- `onSubmit: () => void` - Function called when submit button is clicked

### QuestionsSection

Renders the questions tab content, conditionally showing QuestionCard or nothing.

**Props:**

- `questions: Question[]` - Array of questions
- `currentQuestionIndex: number` - Current question index
- `onResetQuestion: () => void` - Function to reset current question
- `onSubmitAnswer: () => void` - Function to submit answer

### ExercisesSection

Renders the exercises tab content, conditionally showing ExerciseCard or nothing.

**Props:**

- `exercises: Exercise[]` - Array of exercises
- `currentExerciseIndex: number` - Current exercise index
- `onResetExercise: () => void` - Function to reset current exercise
- `onSubmitExercise: () => void` - Function to submit exercise

### EmptyState

Displays when there are no questions or exercises available.

**Props:**

- `activeTab: "questions" | "exercises"` - Currently active tab to show appropriate message

## Usage

The main SkillTraining page imports and uses these components to create a clean, modular structure. Each component handles its own rendering logic while the main page manages state and coordinates between components.

## Benefits

- **Modularity**: Each component has a single responsibility
- **Reusability**: Components can be reused in other parts of the application
- **Maintainability**: Easier to update and debug individual components
- **Testing**: Components can be tested in isolation
- **Readability**: Main page is much cleaner and easier to understand

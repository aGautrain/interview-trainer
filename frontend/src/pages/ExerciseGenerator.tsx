import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import {
  CodeBracketIcon,
  LightBulbIcon,
  ClockIcon,
  DocumentDuplicateIcon,
  EyeIcon,
  EyeSlashIcon,
} from "@heroicons/react/24/outline";
import { mockApi } from "@/services/mockApi";
import { ExerciseForm, CodingExercise, Skill } from "@/types";
import Layout from "@/components/Layout";

export default function ExerciseGenerator() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [exercises, setExercises] = useState<CodingExercise[]>([]);
  const [availableSkills, setAvailableSkills] = useState<Skill[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [showSolutions, setShowSolutions] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ExerciseForm>({
    defaultValues: {
      skills: [],
      language: "JavaScript",
      difficulty: "intermediate",
      count: 3,
      focus: "",
    },
  });

  useEffect(() => {
    loadSkills();
  }, []);

  const loadSkills = async () => {
    try {
      const response = await mockApi.getSkills();
      if (response.success && response.data) {
        setAvailableSkills(response.data);
      }
    } catch (err) {
      console.error("Failed to load skills:", err);
    }
  };

  const onSubmit = async (data: ExerciseForm) => {
    setIsGenerating(true);
    setError(null);

    try {
      const response = await mockApi.generateExercises({
        ...data,
        skills: data.skills.map(
          (skillName) => availableSkills.find((s) => s.name === skillName)!
        ),
      });

      if (response.success && response.data) {
        setExercises(response.data);
      } else {
        setError(response.error || "Failed to generate exercises");
      }
    } catch (err) {
      setError("An unexpected error occurred");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    reset();
    setExercises([]);
    setError(null);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

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

  const programmingLanguages = [
    "JavaScript",
    "Python",
    "Java",
    "C++",
    "Go",
    "Rust",
    "TypeScript",
    "C#",
    "PHP",
    "Ruby",
  ];

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Exercise Generator
          </h1>
          <p className="text-gray-600">
            Generate personalized coding exercises and challenges based on your
            skills and preferences.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="card">
            <div className="flex items-center space-x-3 mb-6">
              <CodeBracketIcon className="w-6 h-6 text-primary-600" />
              <h2 className="text-xl font-semibold text-gray-900">
                Generate Exercises
              </h2>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Skills
                </label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3 max-h-48 overflow-y-auto border border-gray-200 rounded-lg p-3">
                  {availableSkills.map((skill) => (
                    <label
                      key={skill.id}
                      className="flex items-center space-x-2"
                    >
                      <input
                        type="checkbox"
                        value={skill.name}
                        {...register("skills", {
                          required: "At least one skill is required",
                        })}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="text-sm text-gray-700">
                        {skill.name}
                      </span>
                    </label>
                  ))}
                </div>
                {errors.skills && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.skills.message}
                  </p>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Programming Language
                  </label>
                  <select
                    {...register("language", {
                      required: "Programming language is required",
                    })}
                    className="input-field"
                  >
                    {programmingLanguages.map((lang) => (
                      <option key={lang} value={lang}>
                        {lang}
                      </option>
                    ))}
                  </select>
                  {errors.language && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.language.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Difficulty
                  </label>
                  <select
                    {...register("difficulty", {
                      required: "Difficulty is required",
                    })}
                    className="input-field"
                  >
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                  {errors.difficulty && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.difficulty.message}
                    </p>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Exercises
                </label>
                <input
                  type="number"
                  {...register("count", {
                    required: "Count is required",
                    min: { value: 1, message: "Minimum 1 exercise" },
                    max: { value: 10, message: "Maximum 10 exercises" },
                  })}
                  className="input-field max-w-xs"
                  min="1"
                  max="10"
                />
                {errors.count && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.count.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Focus Area (Optional)
                </label>
                <textarea
                  {...register("focus")}
                  rows={3}
                  className="input-field"
                  placeholder="e.g., algorithms, data structures, system design, web development..."
                />
              </div>

              <div className="flex space-x-4">
                <button
                  type="submit"
                  disabled={isGenerating}
                  className="btn-primary flex-1 flex items-center justify-center space-x-2"
                >
                  {isGenerating ? (
                    <>
                      <ClockIcon className="w-5 h-5 animate-spin" />
                      <span>Generating...</span>
                    </>
                  ) : (
                    <>
                      <LightBulbIcon className="w-5 h-5" />
                      <span>Generate Exercises</span>
                    </>
                  )}
                </button>

                <button
                  type="button"
                  onClick={handleReset}
                  className="btn-secondary px-6"
                >
                  Reset
                </button>
              </div>
            </form>
          </div>

          {/* Results */}
          <div className="space-y-6">
            {error && (
              <div className="card border-red-200 bg-red-50">
                <div className="flex items-center space-x-3">
                  <div className="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-xs">!</span>
                  </div>
                  <p className="text-red-800">{error}</p>
                </div>
              </div>
            )}

            {isGenerating && (
              <div className="card">
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <ClockIcon className="w-8 h-8 text-primary-600 animate-spin" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Generating Exercises
                  </h3>
                  <p className="text-gray-600">
                    Creating personalized coding challenges for you...
                  </p>
                </div>
              </div>
            )}

            {exercises.length > 0 && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Generated Exercises ({exercises.length})
                  </h3>
                  <button
                    onClick={() => setShowSolutions(!showSolutions)}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    {showSolutions ? (
                      <>
                        <EyeSlashIcon className="w-4 h-4" />
                        <span>Hide Solutions</span>
                      </>
                    ) : (
                      <>
                        <EyeIcon className="w-4 h-4" />
                        <span>Show Solutions</span>
                      </>
                    )}
                  </button>
                </div>

                {exercises.map((exercise, index) => (
                  <div key={exercise.id} className="card">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <span className="w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-sm font-medium">
                          {index + 1}
                        </span>
                        <div className="flex space-x-2">
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(
                              exercise.difficulty
                            )}`}
                          >
                            {exercise.difficulty.charAt(0).toUpperCase() +
                              exercise.difficulty.slice(1)}
                          </span>
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {exercise.programmingLanguage}
                          </span>
                        </div>
                      </div>
                      <button
                        onClick={() => copyToClipboard(exercise.description)}
                        className="text-gray-400 hover:text-gray-600"
                        title="Copy exercise"
                      >
                        <DocumentDuplicateIcon className="w-5 h-5" />
                      </button>
                    </div>

                    <div className="space-y-4">
                      <h4 className="text-lg font-semibold text-gray-900">
                        {exercise.title}
                      </h4>
                      <p className="text-gray-700">{exercise.description}</p>

                      {exercise.timeLimit && (
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <ClockIcon className="w-4 h-4" />
                          <span>Time limit: {exercise.timeLimit} minutes</span>
                        </div>
                      )}

                      {exercise.requirements &&
                        exercise.requirements.length > 0 && (
                          <div className="bg-gray-50 rounded-lg p-4">
                            <h5 className="font-medium text-gray-900 mb-2">
                              Requirements:
                            </h5>
                            <ul className="space-y-1">
                              {exercise.requirements.map((req, reqIndex) => (
                                <li
                                  key={reqIndex}
                                  className="text-gray-700 text-sm flex items-start space-x-2"
                                >
                                  <div className="w-1.5 h-1.5 bg-primary-600 rounded-full mt-2 flex-shrink-0"></div>
                                  <span>{req}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                      {exercise.testCases && exercise.testCases.length > 0 && (
                        <div className="bg-blue-50 rounded-lg p-4">
                          <h5 className="font-medium text-blue-900 mb-2">
                            Test Cases:
                          </h5>
                          <div className="space-y-3">
                            {exercise.testCases.map((testCase, testIndex) => (
                              <div
                                key={testIndex}
                                className="bg-white rounded p-3"
                              >
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                                  <div>
                                    <span className="font-medium text-blue-900">
                                      Input:
                                    </span>
                                    <code className="block mt-1 bg-gray-100 p-2 rounded font-mono text-xs">
                                      {testCase.input}
                                    </code>
                                  </div>
                                  <div>
                                    <span className="font-medium text-blue-900">
                                      Expected Output:
                                    </span>
                                    <code className="block mt-1 bg-gray-100 p-2 rounded font-mono text-xs">
                                      {testCase.expectedOutput}
                                    </code>
                                  </div>
                                </div>
                                {testCase.description && (
                                  <p className="text-blue-800 text-xs mt-2">
                                    {testCase.description}
                                  </p>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {showSolutions && exercise.solution && (
                        <div className="bg-green-50 rounded-lg p-4">
                          <h5 className="font-medium text-green-900 mb-2">
                            Solution:
                          </h5>
                          <pre className="bg-white rounded p-3 overflow-x-auto">
                            <code className="text-sm font-mono text-green-800">
                              {exercise.solution}
                            </code>
                          </pre>
                        </div>
                      )}

                      {showSolutions &&
                        exercise.hints &&
                        exercise.hints.length > 0 && (
                          <div className="bg-yellow-50 rounded-lg p-4">
                            <h5 className="font-medium text-yellow-900 mb-2">
                              Hints:
                            </h5>
                            <ul className="space-y-1">
                              {exercise.hints.map((hint, hintIndex) => (
                                <li
                                  key={hintIndex}
                                  className="text-yellow-800 text-sm flex items-start space-x-2"
                                >
                                  <div className="w-1.5 h-1.5 bg-yellow-600 rounded-full mt-2 flex-shrink-0"></div>
                                  <span>{hint}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                      <div className="flex space-x-3 pt-4 border-t border-gray-200">
                        <button
                          onClick={() => copyToClipboard(exercise.description)}
                          className="btn-secondary flex items-center space-x-2 text-sm"
                        >
                          <DocumentDuplicateIcon className="w-4 h-4" />
                          <span>Copy Exercise</span>
                        </button>

                        {showSolutions && exercise.solution && (
                          <button
                            onClick={() => copyToClipboard(exercise.solution!)}
                            className="btn-secondary flex items-center space-x-2 text-sm"
                          >
                            <DocumentDuplicateIcon className="w-4 h-4" />
                            <span>Copy Solution</span>
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}

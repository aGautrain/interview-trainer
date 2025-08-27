import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import {
  QuestionMarkCircleIcon,
  LightBulbIcon,
  ClockIcon,
  DocumentDuplicateIcon,
  EyeIcon,
  EyeSlashIcon,
} from "@heroicons/react/24/outline";
import { mockApi } from "@/services/mockApi";
import { QuestionForm, Question, Skill } from "@/types";
import Layout from "@/components/Layout";

export default function QuestionGenerator() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [availableSkills, setAvailableSkills] = useState<Skill[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [showAnswers, setShowAnswers] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<QuestionForm>({
    defaultValues: {
      skills: [],
      type: "technical",
      difficulty: "intermediate",
      count: 5,
      context: "",
    },
  });

  // const watchedSkills = watch('skills') // Unused for now

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

  const onSubmit = async (data: QuestionForm) => {
    setIsGenerating(true);
    setError(null);

    try {
      const response = await mockApi.generateQuestions({
        ...data,
        skills: data.skills.map(
          (skillName) => availableSkills.find((s) => s.name === skillName)!
        ),
      });

      if (response.success && response.data) {
        setQuestions(response.data);
      } else {
        setError(response.error || "Failed to generate questions");
      }
    } catch (err) {
      setError("An unexpected error occurred");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    reset();
    setQuestions([]);
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

  const getTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      technical: "bg-blue-100 text-blue-800",
      behavioral: "bg-purple-100 text-purple-800",
      situational: "bg-indigo-100 text-indigo-800",
      coding: "bg-green-100 text-green-800",
      "system-design": "bg-orange-100 text-orange-800",
    };
    return colors[type] || "bg-gray-100 text-gray-800";
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Question Generator
          </h1>
          <p className="text-gray-600">
            Generate personalized interview questions based on your skills and
            preferences.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="card">
            <div className="flex items-center space-x-3 mb-6">
              <QuestionMarkCircleIcon className="w-6 h-6 text-primary-600" />
              <h2 className="text-xl font-semibold text-gray-900">
                Generate Questions
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
                    Question Type
                  </label>
                  <select
                    {...register("type", {
                      required: "Question type is required",
                    })}
                    className="input-field"
                  >
                    <option value="technical">Technical</option>
                    <option value="behavioral">Behavioral</option>
                    <option value="situational">Situational</option>
                    <option value="coding">Coding</option>
                    <option value="system-design">System Design</option>
                  </select>
                  {errors.type && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.type.message}
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
                  Number of Questions
                </label>
                <input
                  type="number"
                  {...register("count", {
                    required: "Count is required",
                    min: { value: 1, message: "Minimum 1 question" },
                    max: { value: 20, message: "Maximum 20 questions" },
                  })}
                  className="input-field max-w-xs"
                  min="1"
                  max="20"
                />
                {errors.count && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.count.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Context (Optional)
                </label>
                <textarea
                  {...register("context")}
                  rows={3}
                  className="input-field"
                  placeholder="Add any specific context or focus areas..."
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
                      <span>Generate Questions</span>
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
                    Generating Questions
                  </h3>
                  <p className="text-gray-600">
                    Creating personalized questions for you...
                  </p>
                </div>
              </div>
            )}

            {questions.length > 0 && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Generated Questions ({questions.length})
                  </h3>
                  <button
                    onClick={() => setShowAnswers(!showAnswers)}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    {showAnswers ? (
                      <>
                        <EyeSlashIcon className="w-4 h-4" />
                        <span>Hide Answers</span>
                      </>
                    ) : (
                      <>
                        <EyeIcon className="w-4 h-4" />
                        <span>Show Answers</span>
                      </>
                    )}
                  </button>
                </div>

                {questions.map((question, index) => (
                  <div key={question.id} className="card">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <span className="w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-sm font-medium">
                          {index + 1}
                        </span>
                        <div className="flex space-x-2">
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(
                              question.type
                            )}`}
                          >
                            {question.type.charAt(0).toUpperCase() +
                              question.type.slice(1)}
                          </span>
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(
                              question.difficulty
                            )}`}
                          >
                            {question.difficulty.charAt(0).toUpperCase() +
                              question.difficulty.slice(1)}
                          </span>
                        </div>
                      </div>
                      <button
                        onClick={() => copyToClipboard(question.text)}
                        className="text-gray-400 hover:text-gray-600"
                        title="Copy question"
                      >
                        <DocumentDuplicateIcon className="w-5 h-5" />
                      </button>
                    </div>

                    <div className="space-y-4">
                      <p className="text-gray-900 text-lg">{question.text}</p>

                      {question.category && (
                        <div className="text-sm text-gray-600">
                          <span className="font-medium">Category:</span>{" "}
                          {question.category}
                        </div>
                      )}

                      {showAnswers && question.sampleAnswer && (
                        <div className="bg-gray-50 rounded-lg p-4">
                          <h4 className="font-medium text-gray-900 mb-2">
                            Sample Answer:
                          </h4>
                          <p className="text-gray-700">
                            {question.sampleAnswer}
                          </p>
                        </div>
                      )}

                      {showAnswers &&
                        question.tips &&
                        question.tips.length > 0 && (
                          <div className="bg-blue-50 rounded-lg p-4">
                            <h4 className="font-medium text-blue-900 mb-2">
                              Tips:
                            </h4>
                            <ul className="space-y-1">
                              {question.tips.map((tip, tipIndex) => (
                                <li
                                  key={tipIndex}
                                  className="text-blue-800 text-sm flex items-start space-x-2"
                                >
                                  <div className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-2 flex-shrink-0"></div>
                                  <span>{tip}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
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

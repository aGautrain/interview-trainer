import { useState } from "react";
import { useForm } from "react-hook-form";
import {
  DocumentTextIcon,
  LightBulbIcon,
  CheckCircleIcon,
  ClockIcon,
} from "@heroicons/react/24/outline";
import { mockApi } from "@/services/mockApi";
import { JobAnalysisForm, JobAnalysisResult } from "@/types";
import Layout from "@/components/Layout";

export default function JobAnalyzer() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] =
    useState<JobAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<JobAnalysisForm>();

  const onSubmit = async (data: JobAnalysisForm) => {
    setIsAnalyzing(true);
    setError(null);

    try {
      const response = await mockApi.analyzeJob({
        ...data,
        requirements: data.requirements ? [data.requirements] : [],
      });
      if (response.success && response.data) {
        setAnalysisResult(response.data);
      } else {
        setError(response.error || "Failed to analyze job posting");
      }
    } catch (err) {
      setError("An unexpected error occurred");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    reset();
    setAnalysisResult(null);
    setError(null);
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

  const getSkillCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      programming: "bg-blue-100 text-blue-800",
      framework: "bg-purple-100 text-purple-800",
      database: "bg-green-100 text-green-800",
      cloud: "bg-orange-100 text-orange-800",
      tool: "bg-indigo-100 text-indigo-800",
      "soft-skill": "bg-pink-100 text-pink-800",
      other: "bg-gray-100 text-gray-800",
    };
    return colors[category] || colors.other;
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Job Analysis
          </h1>
          <p className="text-gray-600">
            Paste a job description and get AI-powered insights about required
            skills and preparation recommendations.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="card">
            <div className="flex items-center space-x-3 mb-6">
              <DocumentTextIcon className="w-6 h-6 text-primary-600" />
              <h2 className="text-xl font-semibold text-gray-900">
                Job Description
              </h2>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Job Title
                </label>
                <input
                  {...register("title", { required: "Job title is required" })}
                  className="input-field"
                  placeholder="e.g., Senior Frontend Developer"
                />
                {errors.title && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.title.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Company
                </label>
                <input
                  {...register("company", {
                    required: "Company name is required",
                  })}
                  className="input-field"
                  placeholder="e.g., Tech Corp Inc."
                />
                {errors.company && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.company.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Job Description
                </label>
                <textarea
                  {...register("description", {
                    required: "Job description is required",
                  })}
                  rows={6}
                  className="input-field"
                  placeholder="Paste the full job description here..."
                />
                {errors.description && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.description.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Requirements (Optional)
                </label>
                <textarea
                  {...register("requirements")}
                  rows={3}
                  className="input-field"
                  placeholder="List specific requirements or qualifications..."
                />
              </div>

              <div className="flex space-x-4">
                <button
                  type="submit"
                  disabled={isAnalyzing}
                  className="btn-primary flex-1 flex items-center justify-center space-x-2"
                >
                  {isAnalyzing ? (
                    <>
                      <ClockIcon className="w-5 h-5 animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <LightBulbIcon className="w-5 h-5" />
                      <span>Analyze Job</span>
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

            {isAnalyzing && (
              <div className="card">
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <ClockIcon className="w-8 h-8 text-primary-600 animate-spin" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Analyzing Job Posting
                  </h3>
                  <p className="text-gray-600">
                    This may take a few moments...
                  </p>
                </div>
              </div>
            )}

            {analysisResult && (
              <div className="space-y-6">
                {/* Summary Card */}
                <div className="card">
                  <div className="flex items-center space-x-3 mb-4">
                    <CheckCircleIcon className="w-6 h-6 text-green-600" />
                    <h3 className="text-lg font-semibold text-gray-900">
                      Analysis Summary
                    </h3>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <p className="text-gray-600 mb-2">
                        {analysisResult.summary}
                      </p>
                    </div>

                    <div className="flex items-center space-x-4">
                      <span
                        className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(
                          analysisResult.difficulty
                        )}`}
                      >
                        {analysisResult.difficulty.charAt(0).toUpperCase() +
                          analysisResult.difficulty.slice(1)}{" "}
                        Level
                      </span>
                      <span className="text-sm text-gray-600">
                        Est. Experience: {analysisResult.estimatedExperience}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Skills Card */}
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Required Skills
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {analysisResult.skills.map((skill) => (
                      <div
                        key={skill.id}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      >
                        <span className="font-medium text-gray-900">
                          {skill.name}
                        </span>
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${getSkillCategoryColor(
                            skill.category
                          )}`}
                        >
                          {skill.category}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Requirements Card */}
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Key Requirements
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.requirements.map((req, index) => (
                      <li key={index} className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-primary-600 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-gray-700">{req}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Recommendations Card */}
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Preparation Recommendations
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.recommendations.map((rec, index) => (
                      <li key={index} className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}

import { useState, useEffect } from "react";
import {
  ClockIcon,
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  CodeBracketIcon,
  TrashIcon,
  EyeIcon,
  CalendarIcon,
} from "@heroicons/react/24/outline";
import { mockApi } from "@/services/mockApi";
import Layout from "@/components/Layout";

interface HistoryItem {
  id: string;
  type: "job-analysis" | "question-generation" | "exercise-generation";
  input: any;
  output: any;
  model: string;
  tokensUsed: number;
  duration: number;
  createdAt: string;
}

export default function History() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedItem, setSelectedItem] = useState<HistoryItem | null>(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await mockApi.getHistory();
      if (response.success && response.data) {
        setHistory(response.data);
      } else {
        setError(response.error || "Failed to load history");
      }
    } catch (err) {
      setError("An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "job-analysis":
        return <DocumentTextIcon className="w-5 h-5" />;
      case "question-generation":
        return <QuestionMarkCircleIcon className="w-5 h-5" />;
      case "exercise-generation":
        return <CodeBracketIcon className="w-5 h-5" />;
      default:
        return <DocumentTextIcon className="w-5 h-5" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case "job-analysis":
        return "bg-blue-100 text-blue-800";
      case "question-generation":
        return "bg-purple-100 text-purple-800";
      case "exercise-generation":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case "job-analysis":
        return "Job Analysis";
      case "question-generation":
        return "Question Generation";
      case "exercise-generation":
        return "Exercise Generation";
      default:
        return type;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor(
      (now.getTime() - date.getTime()) / (1000 * 60 * 60)
    );

    if (diffInHours < 1) {
      return "Just now";
    } else if (diffInHours < 24) {
      return `${diffInHours} hour${diffInHours > 1 ? "s" : ""} ago`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays} day${diffInDays > 1 ? "s" : ""} ago`;
    }
  };

  const formatDuration = (seconds: number) => {
    if (seconds < 60) {
      return `${seconds.toFixed(1)}s`;
    } else {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}m ${remainingSeconds.toFixed(0)}s`;
    }
  };

  const formatTokens = (tokens: number) => {
    if (tokens >= 1000) {
      return `${(tokens / 1000).toFixed(1)}k`;
    }
    return tokens.toString();
  };

  const clearHistory = () => {
    setHistory([]);
    setSelectedItem(null);
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="max-w-6xl mx-auto">
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <ClockIcon className="w-8 h-8 text-primary-600 animate-spin" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Loading History
            </h3>
            <p className="text-gray-600">Please wait...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Generation History
              </h1>
              <p className="text-gray-600">
                View your previous job analyses, generated questions, and coding
                exercises.
              </p>
            </div>
            {history.length > 0 && (
              <button
                onClick={clearHistory}
                className="btn-secondary flex items-center space-x-2"
              >
                <TrashIcon className="w-4 h-4" />
                <span>Clear History</span>
              </button>
            )}
          </div>
        </div>

        {error && (
          <div className="card border-red-200 bg-red-50 mb-8">
            <div className="flex items-center space-x-3">
              <div className="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                <span className="text-white text-xs">!</span>
              </div>
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        {history.length === 0 ? (
          <div className="card text-center py-12">
            <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <ClockIcon className="w-10 h-10 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No History Yet
            </h3>
            <p className="text-gray-600 mb-6">
              Start by analyzing a job posting or generating questions to see
              your history here.
            </p>
            <div className="flex justify-center space-x-4">
              <button
                onClick={() => (window.location.href = "/analyze")}
                className="btn-primary flex items-center space-x-2"
              >
                <DocumentTextIcon className="w-4 h-4" />
                <span>Analyze Job</span>
              </button>
              <button
                onClick={() => (window.location.href = "/questions")}
                className="btn-secondary flex items-center space-x-2"
              >
                <QuestionMarkCircleIcon className="w-4 h-4" />
                <span>Generate Questions</span>
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* History List */}
            <div className="lg:col-span-2">
              <div className="space-y-4">
                {history.map((item) => (
                  <div
                    key={item.id}
                    className={`card cursor-pointer transition-all duration-200 hover:shadow-md ${
                      selectedItem?.id === item.id
                        ? "ring-2 ring-primary-500"
                        : ""
                    }`}
                    onClick={() => setSelectedItem(item)}
                  >
                    <div className="flex items-start space-x-4">
                      <div
                        className={`p-2 rounded-lg ${getTypeColor(item.type)}`}
                      >
                        {getTypeIcon(item.type)}
                      </div>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-medium text-gray-900">
                            {getTypeLabel(item.type)}
                          </h3>
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(
                              item.type
                            )}`}
                          >
                            {item.model}
                          </span>
                        </div>

                        <div className="text-sm text-gray-600 mb-3">
                          {item.type === "job-analysis" && (
                            <span>
                              {item.input.title} at {item.input.company}
                            </span>
                          )}
                          {item.type === "question-generation" && (
                            <span>
                              {item.output.questions} questions for{" "}
                              {item.input.skills?.join(", ") ||
                                "selected skills"}
                            </span>
                          )}
                          {item.type === "exercise-generation" && (
                            <span>
                              {item.output.exercises ||
                                item.output.exercises?.length ||
                                0}{" "}
                              exercises in {item.input.language}
                            </span>
                          )}
                        </div>

                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                          <div className="flex items-center space-x-1">
                            <CalendarIcon className="w-3 h-3" />
                            <span>{formatDate(item.createdAt)}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <ClockIcon className="w-3 h-3" />
                            <span>{formatDuration(item.duration)}</span>
                          </div>
                          <span>{formatTokens(item.tokensUsed)} tokens</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Detail Panel */}
            <div className="lg:col-span-1">
              {selectedItem ? (
                <div className="card sticky top-8">
                  <div className="flex items-center space-x-3 mb-4">
                    <div
                      className={`p-2 rounded-lg ${getTypeColor(
                        selectedItem.type
                      )}`}
                    >
                      {getTypeIcon(selectedItem.type)}
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {getTypeLabel(selectedItem.type)}
                    </h3>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Input</h4>
                      <div className="bg-gray-50 rounded-lg p-3">
                        <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                          {JSON.stringify(selectedItem.input, null, 2)}
                        </pre>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">
                        Output Summary
                      </h4>
                      <div className="bg-gray-50 rounded-lg p-3">
                        <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                          {JSON.stringify(selectedItem.output, null, 2)}
                        </pre>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                      <div>
                        <span className="text-sm font-medium text-gray-700">
                          Model
                        </span>
                        <p className="text-sm text-gray-900">
                          {selectedItem.model}
                        </p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-700">
                          Duration
                        </span>
                        <p className="text-sm text-gray-900">
                          {formatDuration(selectedItem.duration)}
                        </p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-700">
                          Tokens Used
                        </span>
                        <p className="text-sm text-gray-900">
                          {formatTokens(selectedItem.tokensUsed)}
                        </p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-700">
                          Created
                        </span>
                        <p className="text-sm text-gray-900">
                          {formatDate(selectedItem.createdAt)}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="card text-center py-8">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <EyeIcon className="w-8 h-8 text-gray-400" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Select an Item
                  </h3>
                  <p className="text-gray-600">
                    Click on any history item to view its details here.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}

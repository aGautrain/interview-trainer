import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  SparklesIcon,
  RocketLaunchIcon,
  Cog6ToothIcon,
  CheckCircleIcon,
  DocumentTextIcon,
  QuestionMarkCircleIcon,
} from "@heroicons/react/24/outline";
import { UserPreferences } from "@/types";

interface LandingPageProps {
  preferences: UserPreferences;
  onPreferencesUpdate: (prefs: Partial<UserPreferences>) => void;
  onConfigurationComplete: () => void;
}

export default function LandingPage({
  preferences,
  onPreferencesUpdate,
  onConfigurationComplete,
}: LandingPageProps) {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [llmConfig, setLlmConfig] = useState({
    apiKey: "",
    model: "gpt-4",
    temperature: 0.7,
    maxTokens: 2000,
  });

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      onConfigurationComplete();
      navigate("/analyze");
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return llmConfig.apiKey.trim().length > 0;
      case 2:
        return (
          preferences.preferredLanguages.length > 0 &&
          preferences.questionTypes.length > 0
        );
      case 3:
        return true;
      default:
        return false;
    }
  };

  const steps = [
    {
      id: 1,
      title: "LLM Configuration",
      description: "Set up your AI model preferences",
      icon: Cog6ToothIcon,
    },
    {
      id: 2,
      title: "User Preferences",
      description: "Customize your learning experience",
      icon: Cog6ToothIcon,
    },
    {
      id: 3,
      title: "Ready to Start",
      description: "Begin your interview preparation journey",
      icon: RocketLaunchIcon,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-gradient-to-r from-primary-600 to-primary-800 rounded-full flex items-center justify-center">
              <SparklesIcon className="w-10 h-10 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to Interview Trainer
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered interview preparation with personalized questions and
            coding exercises
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-12">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div
                  className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                    currentStep >= step.id
                      ? "bg-primary-600 border-primary-600 text-white"
                      : "border-gray-300 text-gray-500"
                  }`}
                >
                  {currentStep > step.id ? (
                    <CheckCircleIcon className="w-6 h-6" />
                  ) : (
                    <span className="font-medium">{step.id}</span>
                  )}
                </div>
                {index < steps.length - 1 && (
                  <div
                    className={`w-16 h-0.5 mx-4 ${
                      currentStep > step.id ? "bg-primary-600" : "bg-gray-300"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
          <div className="mt-4 text-center">
            <h3 className="text-lg font-medium text-gray-900">
              {steps[currentStep - 1].title}
            </h3>
            <p className="text-gray-600">
              {steps[currentStep - 1].description}
            </p>
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          {currentStep === 1 && (
            <div className="space-y-6">
              <h3 className="text-2xl font-semibold text-gray-900 mb-6">
                Configure AI Model
              </h3>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  OpenAI API Key
                </label>
                <input
                  type="password"
                  value={llmConfig.apiKey}
                  onChange={(e) =>
                    setLlmConfig((prev) => ({
                      ...prev,
                      apiKey: e.target.value,
                    }))
                  }
                  placeholder="sk-..."
                  className="input-field"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Your API key is stored locally and never sent to our servers
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Model
                  </label>
                  <select
                    value={llmConfig.model}
                    onChange={(e) =>
                      setLlmConfig((prev) => ({
                        ...prev,
                        model: e.target.value,
                      }))
                    }
                    className="input-field"
                  >
                    <option value="gpt-4">GPT-4</option>
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                    <option value="gpt-4-turbo">GPT-4 Turbo</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Temperature
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={llmConfig.temperature}
                    onChange={(e) =>
                      setLlmConfig((prev) => ({
                        ...prev,
                        temperature: parseFloat(e.target.value),
                      }))
                    }
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Focused</span>
                    <span>Creative</span>
                  </div>
                  <p className="text-center text-sm font-medium">
                    {llmConfig.temperature}
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Max Tokens
                  </label>
                  <input
                    type="number"
                    value={llmConfig.maxTokens}
                    onChange={(e) =>
                      setLlmConfig((prev) => ({
                        ...prev,
                        maxTokens: parseInt(e.target.value),
                      }))
                    }
                    className="input-field"
                    min="500"
                    max="4000"
                  />
                </div>
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="space-y-6">
              <h3 className="text-2xl font-semibold text-gray-900 mb-6">
                Customize Your Experience
              </h3>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Preferred Programming Languages
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[
                    "JavaScript",
                    "Python",
                    "Java",
                    "C++",
                    "Go",
                    "Rust",
                    "TypeScript",
                    "C#",
                  ].map((lang) => (
                    <label key={lang} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={preferences.preferredLanguages.includes(lang)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            onPreferencesUpdate({
                              preferredLanguages: [
                                ...preferences.preferredLanguages,
                                lang,
                              ],
                            });
                          } else {
                            onPreferencesUpdate({
                              preferredLanguages:
                                preferences.preferredLanguages.filter(
                                  (l) => l !== lang
                                ),
                            });
                          }
                        }}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="text-sm text-gray-700">{lang}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Question Types
                </label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {[
                    "technical",
                    "behavioral",
                    "situational",
                    "coding",
                    "system-design",
                  ].map((type) => (
                    <label key={type} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={preferences.questionTypes.includes(type)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            onPreferencesUpdate({
                              questionTypes: [
                                ...preferences.questionTypes,
                                type,
                              ],
                            });
                          } else {
                            onPreferencesUpdate({
                              questionTypes: preferences.questionTypes.filter(
                                (t) => t !== type
                              ),
                            });
                          }
                        }}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="text-sm text-gray-700 capitalize">
                        {type}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Default Difficulty Level
                </label>
                <select
                  value={preferences.defaultDifficulty}
                  onChange={(e) =>
                    onPreferencesUpdate({
                      defaultDifficulty: e.target.value as any,
                    })
                  }
                  className="input-field max-w-xs"
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="text-center space-y-6">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                <CheckCircleIcon className="w-10 h-10 text-green-600" />
              </div>

              <h3 className="text-2xl font-semibold text-gray-900">
                You're All Set!
              </h3>

              <p className="text-gray-600 max-w-md mx-auto">
                Your Interview Trainer is configured and ready to help you
                prepare for your next interview. Start by analyzing a job
                posting or generating practice questions.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-lg mx-auto">
                <button
                  onClick={() => navigate("/analyze")}
                  className="btn-primary flex items-center justify-center space-x-2"
                >
                  <DocumentTextIcon className="w-5 h-5" />
                  <span>Analyze Job</span>
                </button>

                <button
                  onClick={() => navigate("/questions")}
                  className="btn-secondary flex items-center justify-center space-x-2"
                >
                  <QuestionMarkCircleIcon className="w-5 h-5" />
                  <span>Generate Questions</span>
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between">
          <button
            onClick={handleBack}
            disabled={currentStep === 1}
            className={`px-6 py-3 rounded-lg font-medium transition-colors duration-200 ${
              currentStep === 1
                ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-300"
            }`}
          >
            Back
          </button>

          <button
            onClick={handleNext}
            disabled={!isStepValid()}
            className={`px-6 py-3 rounded-lg font-medium transition-colors duration-200 ${
              isStepValid()
                ? "btn-primary"
                : "bg-gray-100 text-gray-400 cursor-not-allowed"
            }`}
          >
            {currentStep === 3 ? "Get Started" : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}

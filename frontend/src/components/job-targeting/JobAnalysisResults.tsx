/**
 * JobAnalysisResults Component
 * 
 * Main container for displaying job analysis results, including skills, requirements,
 * training recommendations, and analysis insights with comprehensive error handling.
 */

import React from 'react';
import { 
  ExclamationTriangleIcon, 
  XMarkIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import { 
  type JobAnalysisState
} from '../../services/jobAnalysisService';
import { SkillsDisplay } from './SkillsDisplay';
import { RequirementsDisplay } from './RequirementsDisplay';
import { TrainingRecommendations } from './TrainingRecommendations';
import { AnalysisMetrics } from './AnalysisMetrics';

interface JobAnalysisResultsProps {
  state: JobAnalysisState;
  onRetry: () => void;
  onClear: () => void;
}

export const JobAnalysisResults: React.FC<JobAnalysisResultsProps> = ({
  state,
  onRetry,
  onClear
}) => {
  const { isLoading, error, result, analysisId } = state;

  // Loading state
  if (isLoading) {
    return (
      <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-6">
          <div className="flex items-center justify-center">
            <div className="flex items-center space-x-3">
              <div className="animate-spin h-6 w-6 border-2 border-blue-600 border-t-transparent rounded-full" />
              <div className="text-lg font-medium text-gray-900">
                Analyzing job description...
              </div>
            </div>
          </div>
          
          <div className="mt-4 max-w-2xl mx-auto">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="space-y-2 text-sm text-blue-700">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" />
                  <span>Extracting skills and requirements...</span>
                </div>
                <div className="flex items-center space-x-2 opacity-60">
                  <div className="w-2 h-2 bg-blue-300 rounded-full" />
                  <span>Analyzing experience level and difficulty...</span>
                </div>
                <div className="flex items-center space-x-2 opacity-40">
                  <div className="w-2 h-2 bg-blue-200 rounded-full" />
                  <span>Generating training recommendations...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error && !result) {
    return (
      <div className="mt-8 bg-white rounded-lg shadow-sm border border-red-200">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <ExclamationTriangleIcon className="h-6 w-6 text-red-500" />
              <h3 className="text-lg font-semibold text-red-900">
                Analysis Failed
              </h3>
            </div>
            <button
              onClick={onClear}
              className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Close error message"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
          
          <div className="bg-red-50 rounded-lg p-4 mb-4">
            <p className="text-red-800 font-medium mb-2">
              {error.message}
            </p>
            {error.status && (
              <p className="text-red-600 text-sm">
                Status Code: {error.status}
              </p>
            )}
          </div>
          
          <div className="flex items-center space-x-3">
            <button
              onClick={onRetry}
              className="inline-flex items-center px-4 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
            >
              <ArrowPathIcon className="h-4 w-4 mr-2" />
              Try Again
            </button>
            <button
              onClick={onClear}
              className="inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Success state - show results
  if (result) {
    return (
      <div className="mt-8 space-y-6">

        {/* Analysis Overview */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {result.job_title || "Job Overview"}
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {result.company_name && (
              <div>
                <label className="block text-sm font-medium text-gray-500">
                  Company
                </label>
                <p className="text-lg font-medium text-gray-900">
                  {result.company_name}
                </p>
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium text-gray-500">
                Industry
              </label>
              <p className="text-lg font-medium text-gray-900">
                {result.industry}
              </p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-500">
                Experience Level
              </label>
              <p className="text-lg font-medium text-gray-900 capitalize">
                {result.experience_level.replace(/_/g, ' ')}
              </p>
            </div>
            
          </div>
          
          {result.role_summary && (
            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-500 mb-2">
                Role Summary
              </label>
              <p className="text-gray-700 leading-relaxed">
                {result.role_summary}
              </p>
            </div>
          )}
        </div>

        {/* Analysis Components */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            <SkillsDisplay 
              skills={result.skill_recommendations}
            />
            
            <RequirementsDisplay 
              requirements={result.key_requirements}
              experienceLevel={result.experience_level}
              difficultyLevel={result.difficulty_assessment}
            />
          </div>
          
          {/* Right Column */}
          <div className="space-y-6">
            <TrainingRecommendations 
              recommendations={result.skill_recommendations}
            />
            
            <AnalysisMetrics 
              result={result}
              analysisId={analysisId}
            />
          </div>
        </div>

        {/* Compensation Insights (if available) */}
        {result.compensation_insights && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Compensation Insights
            </h3>
            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-blue-800">
                {result.compensation_insights}
              </p>
            </div>
          </div>
        )}
      </div>
    );
  }

  // Fallback - should not reach here
  return null;
};
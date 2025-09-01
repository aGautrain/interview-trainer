/**
 * TrainingRecommendations Component
 * 
 * Displays personalized training recommendations based on job analysis,
 * including skill gaps, learning priorities, and actionable steps.
 */

import React, { useState, useMemo } from 'react';
import {
  AcademicCapIcon,
  ClockIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  PlayIcon,
  BookOpenIcon,
  LightBulbIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline';
import {
  type SkillRecommendation,
  TrainingPriority,
  DifficultyLevel,
  analysisUtils
} from '../../services/jobAnalysisService';

interface TrainingRecommendationsProps {
  recommendations: SkillRecommendation[];
}

type FilterPriority = TrainingPriority | 'all';

export const TrainingRecommendations: React.FC<TrainingRecommendationsProps> = ({
  recommendations
}) => {
  const [filterPriority, setFilterPriority] = useState<FilterPriority>('all');
  const [expandedRecommendations, setExpandedRecommendations] = useState<Set<number>>(new Set());

  // Filter recommendations by priority
  const filteredRecommendations = useMemo(() => {
    if (filterPriority === 'all') return recommendations;
    return recommendations.filter(rec => rec.priority === filterPriority);
  }, [recommendations, filterPriority]);

  // Get high priority recommendations
  const highPriorityRecommendations = analysisUtils.getHighPriorityRecommendations(recommendations);

  // Toggle expanded state for a recommendation
  const toggleExpanded = (index: number) => {
    const newExpanded = new Set(expandedRecommendations);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedRecommendations(newExpanded);
  };

  // Get priority display info
  const getPriorityInfo = (priority: TrainingPriority) => {
    switch (priority) {
      case TrainingPriority.HIGH:
        return { 
          label: 'High Priority', 
          color: 'text-red-700 bg-red-50 border-red-200',
          icon: ExclamationTriangleIcon,
          textColor: 'text-red-600'
        };
      case TrainingPriority.MEDIUM:
        return { 
          label: 'Medium Priority', 
          color: 'text-yellow-700 bg-yellow-50 border-yellow-200',
          icon: ChartBarIcon,
          textColor: 'text-yellow-600'
        };
      case TrainingPriority.LOW:
        return { 
          label: 'Low Priority', 
          color: 'text-green-700 bg-green-50 border-green-200',
          icon: CheckCircleIcon,
          textColor: 'text-green-600'
        };
      default:
        return { 
          label: 'Unknown Priority', 
          color: 'text-gray-700 bg-gray-50 border-gray-200',
          icon: CheckCircleIcon,
          textColor: 'text-gray-600'
        };
    }
  };

  // Get difficulty display info
  const getDifficultyInfo = (difficulty: DifficultyLevel) => {
    const colorClass = analysisUtils.getDifficultyColorClass(difficulty);
    return {
      label: difficulty.replace('_', ' ').toUpperCase(),
      colorClass
    };
  };

  if (recommendations.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <AcademicCapIcon className="h-5 w-5 mr-2" />
          Training Recommendations
        </h3>
        <div className="text-center py-8">
          <AcademicCapIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h4 className="mt-4 text-lg font-medium text-gray-900">No recommendations available</h4>
          <p className="mt-2 text-gray-500">
            Training recommendations will appear here based on job analysis.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <AcademicCapIcon className="h-5 w-5 mr-2" />
            Training Recommendations ({filteredRecommendations.length})
          </h3>
          
          {highPriorityRecommendations.length > 0 && (
            <span className="inline-flex items-center px-2 py-1 text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded">
              <ExclamationTriangleIcon className="h-3 w-3 mr-1" />
              {highPriorityRecommendations.length} High Priority
            </span>
          )}
        </div>

        {/* Priority Filter */}
        {recommendations.length > 0 && (
          <div className="flex items-center space-x-4">
            <label className="text-sm font-medium text-gray-700">Filter by Priority:</label>
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value as FilterPriority)}
              className="px-3 py-1 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Priorities</option>
              <option value={TrainingPriority.HIGH}>High Priority</option>
              <option value={TrainingPriority.MEDIUM}>Medium Priority</option>
              <option value={TrainingPriority.LOW}>Low Priority</option>
            </select>
          </div>
        )}

        {/* Quick Stats */}
        {recommendations.length > 0 && (
          <div className="mt-4 grid grid-cols-3 gap-4 text-center text-sm">
            <div className="bg-red-50 rounded-lg p-3">
              <div className="text-lg font-semibold text-red-600">
                {recommendations.filter(r => r.priority === TrainingPriority.HIGH).length}
              </div>
              <div className="text-red-700">High Priority</div>
            </div>
            <div className="bg-yellow-50 rounded-lg p-3">
              <div className="text-lg font-semibold text-yellow-600">
                {recommendations.filter(r => r.priority === TrainingPriority.MEDIUM).length}
              </div>
              <div className="text-yellow-700">Medium Priority</div>
            </div>
            <div className="bg-green-50 rounded-lg p-3">
              <div className="text-lg font-semibold text-green-600">
                {recommendations.filter(r => r.priority === TrainingPriority.LOW).length}
              </div>
              <div className="text-green-700">Low Priority</div>
            </div>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-6">

        {/* Training Recommendations */}
        {filteredRecommendations.length > 0 && (
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-4 flex items-center">
              <LightBulbIcon className="h-4 w-4 mr-2 text-blue-500" />
              Recommended Training Plan
            </h4>
            
            <div className="space-y-4">
              {filteredRecommendations.map((recommendation, index) => {
                const priorityInfo = getPriorityInfo(recommendation.priority);
                const PriorityIcon = priorityInfo.icon;
                const difficultyInfo = getDifficultyInfo(recommendation.difficulty_level);
                const isExpanded = expandedRecommendations.has(index);
                
                return (
                  <div
                    key={index}
                    className="border border-gray-200 rounded-lg overflow-hidden hover:border-gray-300 transition-colors"
                  >
                    {/* Header - always visible */}
                    <div 
                      className="p-4 cursor-pointer hover:bg-gray-50"
                      onClick={() => toggleExpanded(index)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className="flex-shrink-0">
                            <PriorityIcon className={`h-5 w-5 ${priorityInfo.textColor}`} />
                          </div>
                          <div>
                            <h5 className="font-semibold text-gray-900">
                              {recommendation.name}
                            </h5>
                            <p className="text-sm text-gray-600">
                              {recommendation.category}
                            </p>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-3">
                          <span className={`inline-flex items-center px-2 py-1 text-xs font-medium rounded border ${priorityInfo.color}`}>
                            {priorityInfo.label}
                          </span>
                          <span className={`inline-flex items-center px-2 py-1 text-xs font-medium rounded ${difficultyInfo.colorClass}`}>
                            {difficultyInfo.label}
                          </span>
                          <ArrowRightIcon 
                            className={`h-4 w-4 text-gray-400 transition-transform ${isExpanded ? 'rotate-90' : ''}`} 
                          />
                        </div>
                      </div>
                      
                      {recommendation.estimated_duration && (
                        <div className="mt-2 flex items-center text-sm text-gray-500">
                          <ClockIcon className="h-4 w-4 mr-1" />
                          Estimated Duration: {recommendation.estimated_duration}
                        </div>
                      )}
                    </div>

                    {/* Expanded Content */}
                    {isExpanded && (
                      <div className="border-t border-gray-200 bg-gray-50 p-4">
                        <div className="space-y-4">
                          {/* Recommended Actions */}
                          {recommendation.recommended_actions.length > 0 && (
                            <div>
                              <h6 className="font-medium text-gray-900 mb-2 flex items-center">
                                <PlayIcon className="h-4 w-4 mr-2 text-green-500" />
                                Action Plan
                              </h6>
                              <ul className="space-y-1">
                                {recommendation.recommended_actions.map((action, actionIndex) => (
                                  <li key={actionIndex} className="flex items-start text-sm">
                                    <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                                    <span className="text-gray-700">{action}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Prerequisites */}
                          {recommendation.prerequisite_skills.length > 0 && (
                            <div>
                              <h6 className="font-medium text-gray-900 mb-2 flex items-center">
                                <ExclamationTriangleIcon className="h-4 w-4 mr-2 text-amber-500" />
                                Prerequisites
                              </h6>
                              <div className="flex flex-wrap gap-2">
                                {recommendation.prerequisite_skills.map((skill, skillIndex) => (
                                  <span 
                                    key={skillIndex}
                                    className="inline-flex items-center px-2 py-1 text-xs bg-amber-100 text-amber-800 rounded"
                                  >
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Learning Resources */}
                          {recommendation.learning_resources.length > 0 && (
                            <div>
                              <h6 className="font-medium text-gray-900 mb-2 flex items-center">
                                <BookOpenIcon className="h-4 w-4 mr-2 text-blue-500" />
                                Learning Resources
                              </h6>
                              <ul className="space-y-1">
                                {recommendation.learning_resources.map((resource, resourceIndex) => (
                                  <li key={resourceIndex} className="text-sm text-blue-600 hover:text-blue-800">
                                    • {resource}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Success Metrics */}
                          {recommendation.success_metrics.length > 0 && (
                            <div>
                              <h6 className="font-medium text-gray-900 mb-2 flex items-center">
                                <ChartBarIcon className="h-4 w-4 mr-2 text-purple-500" />
                                Success Metrics
                              </h6>
                              <ul className="space-y-1">
                                {recommendation.success_metrics.map((metric, metricIndex) => (
                                  <li key={metricIndex} className="flex items-start text-sm">
                                    <div className="w-2 h-2 bg-purple-500 rounded-full mt-2 mr-2 flex-shrink-0" />
                                    <span className="text-gray-700">{metric}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {filteredRecommendations.length === 0 && recommendations.length > 0 && (
          <div className="text-center py-8">
            <AcademicCapIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h4 className="mt-4 text-lg font-medium text-gray-900">No recommendations match filter</h4>
            <p className="mt-2 text-gray-500">
              Try adjusting the priority filter to see more recommendations.
            </p>
          </div>
        )}
      </div>

      {/* Action Footer */}
      {recommendations.length > 0 && (
        <div className="px-6 py-4 bg-blue-50 border-t border-gray-200 rounded-b-lg">
          <div className="flex items-center justify-between">
            <div className="text-sm text-blue-700">
              <strong>Next Steps:</strong> Start with high-priority recommendations and prerequisite skills.
            </div>
            <button className="inline-flex items-center px-3 py-1 text-sm font-medium text-blue-700 bg-blue-100 rounded hover:bg-blue-200 transition-colors">
              <PlayIcon className="h-4 w-4 mr-1" />
              Start Training
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
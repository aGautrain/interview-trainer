/**
 * AnalysisMetrics Component
 * 
 * Displays analysis insights, statistics, and metadata about the job analysis
 * including processing details, confidence metrics, and performance indicators.
 */

import React, { useMemo } from 'react';
import {
  ChartBarIcon,
  ClockIcon,
  CpuChipIcon,
  InformationCircleIcon,
  CheckBadgeIcon,
  SparklesIcon,
  TagIcon
} from '@heroicons/react/24/outline';
import {
  type JobAnalysisResult,
  analysisUtils
} from '../../services/jobAnalysisService';

interface AnalysisMetricsProps {
  result: JobAnalysisResult;
  analysisId?: string;
}

export const AnalysisMetrics: React.FC<AnalysisMetricsProps> = ({
  result,
  analysisId
}) => {
  // Calculate various metrics
  const metrics = useMemo(() => {
    const skills = result.extracted_skills;
    const avgConfidence = analysisUtils.getAverageConfidence(skills);
    const skillsByImportance = analysisUtils.getSkillsByImportance(skills);
    const skillsByCategory = analysisUtils.getSkillsByCategory(skills);
    
    // Calculate distribution percentages
    const totalSkills = skills.length;
    const criticalPercentage = totalSkills > 0 ? 
      (skillsByImportance.critical?.length || 0) / totalSkills * 100 : 0;
    const importantPercentage = totalSkills > 0 ? 
      (skillsByImportance.important?.length || 0) / totalSkills * 100 : 0;
    
    // Get top categories
    const topCategories = Object.entries(skillsByCategory)
      .sort(([,a], [,b]) => b.length - a.length)
      .slice(0, 5)
      .map(([category, skillList]) => ({
        name: category,
        count: skillList.length,
        percentage: totalSkills > 0 ? (skillList.length / totalSkills * 100) : 0
      }));

    // Analysis completeness score
    const completenessFactors = [
      result.role_summary ? 1 : 0,
      result.extracted_skills.length > 0 ? 1 : 0,
      result.key_requirements.length > 0 ? 1 : 0,
      result.training_recommendations.length > 0 ? 1 : 0,
      result.experience_level ? 1 : 0,
      result.industry ? 1 : 0
    ];
    const completenessScore = completenessFactors.reduce((a, b) => a + b, 0) / completenessFactors.length * 100;

    return {
      avgConfidence,
      totalSkills,
      criticalPercentage,
      importantPercentage,
      topCategories,
      completenessScore
    };
  }, [result]);

  // Get analysis metadata insights
  const metadataInsights = useMemo(() => {
    const metadata = result.analysis_metadata || {};
    const insights = [];

    // Processing insights
    if (metadata.processing_time_ms) {
      insights.push({
        label: 'Processing Time',
        value: `${metadata.processing_time_ms}ms`,
        icon: ClockIcon,
        type: 'info'
      });
    }

    if (metadata.tokens_used) {
      insights.push({
        label: 'Tokens Processed',
        value: metadata.tokens_used.toLocaleString(),
        icon: CpuChipIcon,
        type: 'info'
      });
    }

    if (metadata.llm_provider) {
      insights.push({
        label: 'AI Provider',
        value: metadata.llm_provider,
        icon: SparklesIcon,
        type: 'info'
      });
    }

    if (metadata.cache_hit !== undefined) {
      insights.push({
        label: 'Cache Status',
        value: metadata.cache_hit ? 'Hit' : 'Miss',
        icon: metadata.cache_hit ? CheckBadgeIcon : InformationCircleIcon,
        type: metadata.cache_hit ? 'success' : 'info'
      });
    }

    return insights;
  }, [result.analysis_metadata]);

  // Get confidence level classification
  const getConfidenceLevel = (confidence: number) => {
    if (confidence >= 0.9) return { label: 'Excellent', color: 'text-green-600', bgColor: 'bg-green-50' };
    if (confidence >= 0.8) return { label: 'Very Good', color: 'text-blue-600', bgColor: 'bg-blue-50' };
    if (confidence >= 0.7) return { label: 'Good', color: 'text-yellow-600', bgColor: 'bg-yellow-50' };
    if (confidence >= 0.6) return { label: 'Moderate', color: 'text-orange-600', bgColor: 'bg-orange-50' };
    return { label: 'Needs Review', color: 'text-red-600', bgColor: 'bg-red-50' };
  };

  const confidenceLevel = getConfidenceLevel(metrics.avgConfidence);

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center">
          <ChartBarIcon className="h-5 w-5 mr-2" />
          Analysis Insights
        </h3>
        {analysisId && (
          <p className="text-sm text-gray-500 mt-1">
            Analysis ID: <code className="bg-gray-100 px-1 rounded text-xs">{analysisId}</code>
          </p>
        )}
      </div>

      {/* Content */}
      <div className="p-6 space-y-6">
        {/* Quality Metrics */}
        <div>
          <h4 className="text-md font-semibold text-gray-900 mb-4">Quality Metrics</h4>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Average Confidence */}
            <div className={`rounded-lg p-4 border ${confidenceLevel.bgColor} ${confidenceLevel.color}`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Average Confidence</p>
                  <p className="text-2xl font-bold">
                    {(metrics.avgConfidence * 100).toFixed(1)}%
                  </p>
                  <p className="text-xs mt-1 opacity-80">
                    {confidenceLevel.label}
                  </p>
                </div>
                <div className="w-12 h-12 rounded-full bg-white bg-opacity-50 flex items-center justify-center">
                  <ChartBarIcon className="h-6 w-6" />
                </div>
              </div>
              
              <div className="mt-3 bg-white bg-opacity-30 rounded-full h-2">
                <div 
                  className="bg-current h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.avgConfidence * 100}%` }}
                />
              </div>
            </div>

            {/* Analysis Completeness */}
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200 text-blue-600">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Analysis Completeness</p>
                  <p className="text-2xl font-bold">
                    {metrics.completenessScore.toFixed(0)}%
                  </p>
                  <p className="text-xs mt-1 opacity-80">
                    {metrics.completenessScore >= 80 ? 'Comprehensive' : 
                     metrics.completenessScore >= 60 ? 'Good Coverage' : 'Basic'}
                  </p>
                </div>
                <div className="w-12 h-12 rounded-full bg-white bg-opacity-50 flex items-center justify-center">
                  <CheckBadgeIcon className="h-6 w-6" />
                </div>
              </div>
              
              <div className="mt-3 bg-white bg-opacity-30 rounded-full h-2">
                <div 
                  className="bg-current h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.completenessScore}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Skills Distribution */}
        {metrics.totalSkills > 0 && (
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-4">Skills Distribution</h4>
            
            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full" />
                  <span>Critical Skills</span>
                </div>
                <span className="font-medium">
                  {metrics.criticalPercentage.toFixed(1)}% ({result.extracted_skills.filter(s => s.importance === 'critical').length})
                </span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-red-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.criticalPercentage}%` }}
                />
              </div>
            </div>
            
            <div className="mt-3 space-y-3">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-orange-500 rounded-full" />
                  <span>Important Skills</span>
                </div>
                <span className="font-medium">
                  {metrics.importantPercentage.toFixed(1)}% ({result.extracted_skills.filter(s => s.importance === 'important').length})
                </span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-orange-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.importantPercentage}%` }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Top Skill Categories */}
        {metrics.topCategories.length > 0 && (
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-4">Top Skill Categories</h4>
            
            <div className="space-y-3">
              {metrics.topCategories.map((category, categoryIndex) => (
                <div key={category.name} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      <TagIcon className="h-4 w-4 text-gray-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900 capitalize">
                        {category.name.replace(/_/g, ' ')}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {category.count} skills
                      </p>
                      <p className="text-xs text-gray-500">
                        {category.percentage.toFixed(1)}%
                      </p>
                    </div>
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${category.percentage}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Technical Metadata */}
        {metadataInsights.length > 0 && (
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-4">Technical Details</h4>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {metadataInsights.map((insight, insightIndex) => {
                const Icon = insight.icon;
                const colorClass = insight.type === 'success' ? 'text-green-600' :
                                 insight.type === 'warning' ? 'text-yellow-600' :
                                 insight.type === 'error' ? 'text-red-600' : 'text-blue-600';
                
                return (
                  <div key={insightIndex} className="bg-gray-50 rounded-lg p-3 border">
                    <div className="flex items-center space-x-2">
                      <Icon className={`h-4 w-4 ${colorClass}`} />
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {insight.label}
                        </p>
                        <p className="text-sm text-gray-600">
                          {insight.value}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Summary Stats */}
        <div className="bg-gray-50 rounded-lg p-4 border">
          <h4 className="text-md font-semibold text-gray-900 mb-3">Analysis Summary</h4>
          
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center text-sm">
            <div>
              <div className="text-lg font-bold text-blue-600">{metrics.totalSkills}</div>
              <div className="text-gray-600">Skills Extracted</div>
            </div>
            <div>
              <div className="text-lg font-bold text-purple-600">{result.key_requirements.length}</div>
              <div className="text-gray-600">Requirements</div>
            </div>
            <div>
              <div className="text-lg font-bold text-green-600">{result.training_recommendations.length}</div>
              <div className="text-gray-600">Recommendations</div>
            </div>
            <div>
              <div className="text-lg font-bold text-orange-600">{result.skill_gaps.length}</div>
              <div className="text-gray-600">Skill Gaps</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
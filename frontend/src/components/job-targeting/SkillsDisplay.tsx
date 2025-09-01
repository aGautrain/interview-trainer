/**
 * SkillsDisplay Component
 * 
 * Displays extracted skills from job analysis with importance levels,
 * categories, and matching information. Provides filtering and grouping options.
 */

import React, { useState, useMemo } from 'react';
import { 
  FunnelIcon,
  TagIcon,
  CheckBadgeIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { 
  type SkillRecommendation, 
  SkillImportance,
  analysisUtils
} from '../../services/jobAnalysisService';

interface SkillsDisplayProps {
  skills: SkillRecommendation[];
}

type ViewMode = 'importance' | 'category' | 'experience';
type FilterImportance = SkillImportance | 'all';

export const SkillsDisplay: React.FC<SkillsDisplayProps> = ({
  skills
}) => {
  const [viewMode, setViewMode] = useState<ViewMode>('importance');
  const [filterImportance, setFilterImportance] = useState<FilterImportance>('all');

  // Filter skills based on selected filters
  const filteredSkills = useMemo(() => {
    let filtered = skills;

    // Filter by importance
    if (filterImportance !== 'all') {
      filtered = filtered.filter(skill => skill.importance === filterImportance);
    }

    return filtered;
  }, [skills, filterImportance]);

  // Group skills by selected view mode
  const groupedSkills = useMemo(() => {
    switch (viewMode) {
      case 'importance':
        return analysisUtils.getSkillsByImportance(filteredSkills);
      case 'category':
        return analysisUtils.getSkillsByCategory(filteredSkills);
      case 'experience':
        return {
          'Senior (5+ years)': filteredSkills.filter(s => s.years_required && s.years_required >= 5),
          'Mid-level (2-5 years)': filteredSkills.filter(s => s.years_required && s.years_required >= 2 && s.years_required < 5),
          'Junior (<2 years)': filteredSkills.filter(s => s.years_required && s.years_required < 2),
          'Not specified': filteredSkills.filter(s => !s.years_required)
        };
      default:
        return { 'All Skills': filteredSkills };
    }
  }, [filteredSkills, viewMode]);


  // Get importance display info
  const getImportanceInfo = (importance: SkillImportance) => {
    switch (importance) {
      case SkillImportance.CRITICAL:
        return { label: 'Critical', color: 'text-red-700 bg-red-50 border-red-200' };
      case SkillImportance.IMPORTANT:
        return { label: 'Important', color: 'text-orange-700 bg-orange-50 border-orange-200' };
      case SkillImportance.PREFERRED:
        return { label: 'Preferred', color: 'text-blue-700 bg-blue-50 border-blue-200' };
      case SkillImportance.NICE_TO_HAVE:
        return { label: 'Nice to Have', color: 'text-gray-700 bg-gray-50 border-gray-200' };
      default:
        return { label: 'Unknown', color: 'text-gray-700 bg-gray-50 border-gray-200' };
    }
  };


  if (skills.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <TagIcon className="h-5 w-5 mr-2" />
          Extracted Skills
        </h3>
        <div className="text-center py-8">
          <TagIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h4 className="mt-4 text-lg font-medium text-gray-900">No skills extracted</h4>
          <p className="mt-2 text-gray-500">
            No skills were identified in the job description.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header with filters */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <TagIcon className="h-5 w-5 mr-2" />
            Extracted Skills ({filteredSkills.length})
          </h3>
        </div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-4">
          {/* View Mode Selector */}
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Group by
            </label>
            <select
              value={viewMode}
              onChange={(e) => setViewMode(e.target.value as ViewMode)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              <option value="importance">Importance Level</option>
              <option value="category">Category</option>
              <option value="experience">Experience Required</option>
            </select>
          </div>

          {/* Importance Filter */}
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filter by Importance
            </label>
            <select
              value={filterImportance}
              onChange={(e) => setFilterImportance(e.target.value as FilterImportance)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              <option value="all">All Levels</option>
              <option value={SkillImportance.CRITICAL}>Critical Only</option>
              <option value={SkillImportance.IMPORTANT}>Important Only</option>
              <option value={SkillImportance.PREFERRED}>Preferred Only</option>
              <option value={SkillImportance.NICE_TO_HAVE}>Nice to Have Only</option>
            </select>
          </div>

        </div>
      </div>

      {/* Skills Content */}
      <div className="p-6">
        {Object.entries(groupedSkills).map(([groupName, groupSkills]) => (
          groupSkills.length > 0 && (
            <div key={groupName} className="mb-6 last:mb-0">
              <h4 className="text-md font-medium text-gray-900 mb-3 capitalize">
                {groupName} ({groupSkills.length})
              </h4>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {groupSkills.map((skill, index) => {
                  const importanceInfo = getImportanceInfo(skill.importance);
                  
                  return (
                    <div
                      key={`${skill.name}-${index}`}
                      className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-gray-300 transition-colors"
                    >
                      {/* Skill Header */}
                      <div className="flex items-start justify-between mb-2">
                        <h5 className="font-medium text-gray-900 leading-tight">
                          {skill.name}
                        </h5>
                        
                      </div>

                      {/* Skill Details */}
                      <div className="space-y-2">
                        {/* Importance and Category */}
                        <div className="flex items-center space-x-2">
                          <span className={`inline-flex items-center px-2 py-1 text-xs font-medium rounded border ${importanceInfo.color}`}>
                            {importanceInfo.label}
                          </span>
                          <span className="text-xs text-gray-500 bg-white px-2 py-1 rounded border">
                            {skill.category}
                          </span>
                        </div>

                        {/* Experience */}
                        {skill.years_required && (
                          <div className="flex items-center justify-end text-xs text-gray-600">
                            <span className="text-gray-500">
                              {skill.years_required}+ years
                            </span>
                          </div>
                        )}

                        {/* Context */}
                        {skill.context && (
                          <div className="text-xs text-gray-500 italic leading-relaxed">
                            "{skill.context}"
                          </div>
                        )}

                        {/* Related Skills */}
                        {skill.related_skills.length > 0 && (
                          <div className="text-xs text-gray-500">
                            <span className="font-medium">Related:</span>{' '}
                            {skill.related_skills.slice(0, 3).join(', ')}
                            {skill.related_skills.length > 3 && '...'}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )
        ))}

        {filteredSkills.length === 0 && (
          <div className="text-center py-8">
            <FunnelIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h4 className="mt-4 text-lg font-medium text-gray-900">No skills match filters</h4>
            <p className="mt-2 text-gray-500">
              Try adjusting your filters to see more results.
            </p>
          </div>
        )}
      </div>

      {/* Summary Footer */}
      {filteredSkills.length > 0 && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-lg">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-red-500 rounded-full" />
                <span>{skills.filter(s => s.importance === SkillImportance.CRITICAL).length} Critical</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-orange-500 rounded-full" />
                <span>{skills.filter(s => s.importance === SkillImportance.IMPORTANT).length} Important</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-blue-500 rounded-full" />
                <span>{skills.filter(s => s.importance === SkillImportance.PREFERRED).length} Preferred</span>
              </div>
            </div>
            
          </div>
        </div>
      )}
    </div>
  );
};
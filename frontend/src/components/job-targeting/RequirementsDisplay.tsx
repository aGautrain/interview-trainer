/**
 * RequirementsDisplay Component
 * 
 * Displays job requirements analysis including key requirements, experience level,
 * and difficulty assessment with visual indicators and categorization.
 */

import React, { useMemo } from 'react';
import {
  DocumentTextIcon,
  AcademicCapIcon,
  ClockIcon,
  ChartBarIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { 
  DifficultyLevel,
  analysisUtils 
} from '../../services/jobAnalysisService';

interface RequirementsDisplayProps {
  requirements: string[];
  experienceLevel: string;
  difficultyLevel: DifficultyLevel;
}

export const RequirementsDisplay: React.FC<RequirementsDisplayProps> = ({
  requirements,
  experienceLevel,
  difficultyLevel
}) => {
  // Categorize requirements based on keywords
  const categorizedRequirements = useMemo(() => {
    const categories = {
      technical: [] as string[],
      experience: [] as string[],
      education: [] as string[],
      soft_skills: [] as string[],
      other: [] as string[]
    };

    const technicalKeywords = [
      'programming', 'development', 'coding', 'software', 'framework', 'library',
      'database', 'api', 'cloud', 'devops', 'testing', 'debugging', 'architecture',
      'javascript', 'python', 'java', 'react', 'node', 'sql', 'aws', 'docker'
    ];
    
    const experienceKeywords = [
      'years', 'experience', 'senior', 'junior', 'lead', 'management', 'leadership',
      'project', 'team', 'mentoring', 'guidance'
    ];
    
    const educationKeywords = [
      'degree', 'bachelor', 'master', 'phd', 'education', 'university', 'college',
      'certification', 'certified', 'diploma'
    ];
    
    const softSkillsKeywords = [
      'communication', 'collaboration', 'teamwork', 'problem', 'analytical',
      'creative', 'leadership', 'initiative', 'adaptable', 'flexible', 'organize'
    ];

    requirements.forEach(requirement => {
      const lowerReq = requirement.toLowerCase();
      
      if (technicalKeywords.some(keyword => lowerReq.includes(keyword))) {
        categories.technical.push(requirement);
      } else if (experienceKeywords.some(keyword => lowerReq.includes(keyword))) {
        categories.experience.push(requirement);
      } else if (educationKeywords.some(keyword => lowerReq.includes(keyword))) {
        categories.education.push(requirement);
      } else if (softSkillsKeywords.some(keyword => lowerReq.includes(keyword))) {
        categories.soft_skills.push(requirement);
      } else {
        categories.other.push(requirement);
      }
    });

    return categories;
  }, [requirements]);

  // Get difficulty display info
  const getDifficultyInfo = (difficulty: DifficultyLevel) => {
    switch (difficulty) {
      case DifficultyLevel.BEGINNER:
        return { 
          label: 'Beginner', 
          color: 'text-green-700 bg-green-50 border-green-200',
          icon: CheckCircleIcon,
          description: 'Entry-level position suitable for beginners'
        };
      case DifficultyLevel.INTERMEDIATE:
        return { 
          label: 'Intermediate', 
          color: 'text-yellow-700 bg-yellow-50 border-yellow-200',
          icon: ClockIcon,
          description: 'Mid-level position requiring some experience'
        };
      case DifficultyLevel.ADVANCED:
        return { 
          label: 'Advanced', 
          color: 'text-orange-700 bg-orange-50 border-orange-200',
          icon: ChartBarIcon,
          description: 'Senior-level position with complex requirements'
        };
      case DifficultyLevel.EXPERT:
        return { 
          label: 'Expert', 
          color: 'text-red-700 bg-red-50 border-red-200',
          icon: ExclamationTriangleIcon,
          description: 'Expert-level position requiring extensive experience'
        };
      default:
        return { 
          label: 'Unknown', 
          color: 'text-gray-700 bg-gray-50 border-gray-200',
          icon: CheckCircleIcon,
          description: 'Difficulty level not determined'
        };
    }
  };

  // Get category info
  const getCategoryInfo = (category: string) => {
    switch (category) {
      case 'technical':
        return {
          label: 'Technical Requirements',
          icon: DocumentTextIcon,
          color: 'text-blue-600',
          bgColor: 'bg-blue-50'
        };
      case 'experience':
        return {
          label: 'Experience Requirements',
          icon: ClockIcon,
          color: 'text-purple-600',
          bgColor: 'bg-purple-50'
        };
      case 'education':
        return {
          label: 'Education Requirements',
          icon: AcademicCapIcon,
          color: 'text-indigo-600',
          bgColor: 'bg-indigo-50'
        };
      case 'soft_skills':
        return {
          label: 'Soft Skills',
          icon: ChartBarIcon,
          color: 'text-green-600',
          bgColor: 'bg-green-50'
        };
      default:
        return {
          label: 'Other Requirements',
          icon: DocumentTextIcon,
          color: 'text-gray-600',
          bgColor: 'bg-gray-50'
        };
    }
  };

  const difficultyInfo = getDifficultyInfo(difficultyLevel);
  const DifficultyIcon = difficultyInfo.icon;

  if (requirements.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <DocumentTextIcon className="h-5 w-5 mr-2" />
          Job Requirements
        </h3>
        <div className="text-center py-8">
          <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h4 className="mt-4 text-lg font-medium text-gray-900">No requirements extracted</h4>
          <p className="mt-2 text-gray-500">
            No specific requirements were identified in the job description.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <DocumentTextIcon className="h-5 w-5 mr-2" />
          Job Requirements ({requirements.length})
        </h3>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Experience Level */}
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="flex items-center">
              <ClockIcon className="h-5 w-5 text-blue-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-blue-900">Experience Level</p>
                <p className="text-lg font-semibold text-blue-700 capitalize">
                  {analysisUtils.formatExperienceLevel(experienceLevel)}
                </p>
              </div>
            </div>
          </div>

          {/* Difficulty Assessment */}
          <div className={`rounded-lg p-4 border ${difficultyInfo.color}`}>
            <div className="flex items-center">
              <DifficultyIcon className="h-5 w-5 mr-2" />
              <div>
                <p className="text-sm font-medium">Role Difficulty</p>
                <p className="text-lg font-semibold">
                  {difficultyInfo.label}
                </p>
                <p className="text-xs mt-1 opacity-80">
                  {difficultyInfo.description}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Requirements Content */}
      <div className="p-6">
        <div className="space-y-6">
          {Object.entries(categorizedRequirements).map(([category, categoryRequirements]) => {
            if (categoryRequirements.length === 0) return null;
            
            const categoryInfo = getCategoryInfo(category);
            const CategoryIcon = categoryInfo.icon;
            
            return (
              <div key={category}>
                <div className="flex items-center mb-3">
                  <CategoryIcon className={`h-5 w-5 mr-2 ${categoryInfo.color}`} />
                  <h4 className="text-md font-medium text-gray-900">
                    {categoryInfo.label} ({categoryRequirements.length})
                  </h4>
                </div>
                
                <div className={`rounded-lg p-4 ${categoryInfo.bgColor}`}>
                  <ul className="space-y-2">
                    {categoryRequirements.map((requirement, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-800 leading-relaxed">
                          {requirement}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            );
          })}
        </div>

        {/* Summary */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h4 className="text-md font-medium text-gray-900 mb-3">Requirements Summary</h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
            <div className="text-center">
              <div className="text-lg font-semibold text-blue-600">
                {categorizedRequirements.technical.length}
              </div>
              <div className="text-gray-600">Technical</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-purple-600">
                {categorizedRequirements.experience.length}
              </div>
              <div className="text-gray-600">Experience</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-indigo-600">
                {categorizedRequirements.education.length}
              </div>
              <div className="text-gray-600">Education</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-green-600">
                {categorizedRequirements.soft_skills.length}
              </div>
              <div className="text-gray-600">Soft Skills</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
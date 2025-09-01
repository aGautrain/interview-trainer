"""
Job Analysis Service for the Interview Trainer application.

This service orchestrates the complete job analysis workflow using the LLM abstraction layer
to analyze job descriptions, extract skills, match them with existing database entries,
and generate personalized training recommendations.

Key Features:
- Complete job description analysis using LLM providers
- Skills extraction and matching with database
- Training recommendations based on skill gaps
- Comprehensive error handling and retry logic
- Performance optimization and metrics tracking
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple, Any
from uuid import uuid4

from database import fetch_all, fetch_one, execute, fetch_val
from schemas.job_analysis import (
    JobAnalysisRequest, JobAnalysisResponse, JobAnalysisResult,
    SkillRecommendation, ExtractedSkillEnhanced, TrainingRecommendation,
    AnalysisStatus, SkillImportance, TrainingPriority,
    AnalysisMetrics
)
from schemas.base import DifficultyLevel, SkillType
from services.llm import (
    get_available_provider, LLMProvider, JobAnalysis, ExtractedSkill,
    LLMProviderError, RateLimitError, AuthenticationError
)




class JobAnalysisService:
    """
    Service class for comprehensive job analysis operations.
    
    This service handles the complete workflow from job description analysis
    to personalized training recommendations, including caching and error handling.
    """
    
    def __init__(self):
        """Initialize the job analysis service"""
        self._llm_provider: Optional[LLMProvider] = None
        self._max_retry_attempts = 3
        self._retry_delay_base = 1.0  # Base delay for exponential backoff
        
        # Skill matching configuration
        self._exact_match_threshold = 1.0
        self._synonym_match_threshold = 0.9
        self._partial_match_threshold = 0.7
        self._semantic_match_threshold = 0.6
        
        # Initialize metrics
        self._metrics = AnalysisMetrics()
    
    async def _get_llm_provider(self) -> LLMProvider:
        """Get or initialize the LLM provider"""
        if self._llm_provider is None:
            self._llm_provider = await get_available_provider()
            if not self._llm_provider:
                raise LLMProviderError("No LLM provider available", "system")
        return self._llm_provider
    
    async def analyze_job_description(
        self, 
        request: JobAnalysisRequest
    ) -> JobAnalysisResponse:
        """
        Perform complete job description analysis.
        
        This is the main entry point that orchestrates the entire analysis workflow:
        1. Extract skills using LLM provider
        2. Match skills with database entries
        3. Generate training recommendations
        4. Calculate readiness scores
        
        Args:
            request: Job analysis request with description and context
            
        Returns:
            JobAnalysisResponse with complete analysis results
        """
        start_time = time.time()
        analysis_id = str(uuid4())
        
        
        try:
            
            # Perform LLM analysis
            llm_provider = await self._get_llm_provider()
            llm_response = await self._analyze_with_retry(
                llm_provider, 
                request.job_description, 
                request.company_context
            )
            
            if not llm_response.success:
                raise LLMProviderError(
                    llm_response.error or "LLM analysis failed",
                    llm_provider.provider_name
                )
            
            # Extract skills and generate unified skill recommendations
            job_analysis = JobAnalysis(**llm_response.data)
            skill_recommendations = await self._generate_unified_skill_recommendations(job_analysis, request.user_id)
            
            # Build comprehensive result
            result = JobAnalysisResult(
                job_title=job_analysis.job_title or request.job_title,
                company_name=request.company_name,
                industry=job_analysis.industry,
                key_requirements=job_analysis.key_requirements,
                skill_recommendations=skill_recommendations,
                experience_level=job_analysis.experience_level,
                difficulty_assessment=self._map_difficulty_level(job_analysis.difficulty_assessment),
                role_summary=job_analysis.summary,
                analysis_metadata={
                    "llm_provider": llm_provider.provider_name,
                    "analysis_depth": request.analysis_depth,
                    "skills_count": len(skill_recommendations)
                }
            )
            
            
            # Update metrics
            processing_time = (time.time() - start_time) * 1000
            self._metrics.total_analyses += 1
            self._metrics.successful_analyses += 1
            self._metrics.total_tokens_used += llm_response.tokens_used or 0
            
            if self._metrics.avg_processing_time_ms:
                self._metrics.avg_processing_time_ms = (
                    self._metrics.avg_processing_time_ms + processing_time
                ) / 2
            else:
                self._metrics.avg_processing_time_ms = processing_time
            
            
            return JobAnalysisResponse(
                success=True,
                status=AnalysisStatus.COMPLETED,
                result=result,
                processing_time_ms=processing_time,
                llm_provider=llm_provider.provider_name,
                tokens_used=llm_response.tokens_used,
                analysis_id=analysis_id
            )
            
        except Exception as e:
            self._metrics.total_analyses += 1
            self._metrics.failed_analyses += 1
            
            return JobAnalysisResponse(
                success=False,
                status=AnalysisStatus.FAILED,
                error_message=str(e),
                processing_time_ms=(time.time() - start_time) * 1000,
                analysis_id=analysis_id
            )
    
    async def extract_skills_from_text(
        self, 
        text: str, 
        context_type: str = "job_description"
    ) -> List[ExtractedSkillEnhanced]:
        """
        Extract skills from any text content.
        
        Args:
            text: Text to analyze for skills
            context_type: Type of content being analyzed
            
        Returns:
            List of extracted and enhanced skills
        """
        try:
            llm_provider = await self._get_llm_provider()
            response = await llm_provider.extract_skills(text, context_type)
            
            if not response.success:
                raise LLMProviderError(
                    response.error or "Skill extraction failed",
                    llm_provider.provider_name
                )
            
            # Convert LLM extracted skills to enhanced format
            skills = [ExtractedSkill(**skill) for skill in response.data.get('skills', [])]
            return await self._enhance_raw_skills(skills)
            
        except Exception as e:
            raise
    
    async def generate_training_recommendations(
        self, 
        analysis: JobAnalysisResult, 
        user_id: Optional[str] = None
    ) -> List[TrainingRecommendation]:
        """
        Generate training recommendations based on job analysis.
        
        Args:
            analysis: Complete job analysis result
            user_id: Optional user ID for personalization
            
        Returns:
            List of prioritized training recommendations
        """
        return await self._generate_training_recommendations(analysis.extracted_skills, user_id)
    
    
    async def get_analysis_metrics(self) -> AnalysisMetrics:
        """Get current analysis metrics and statistics"""
        # Note: Skill analysis stats no longer available without cache tables
        
        return self._metrics
    
    # Private helper methods
    
    async def _analyze_with_retry(
        self, 
        provider: LLMProvider, 
        job_description: str, 
        company_context: Optional[str] = None
    ):
        """Perform LLM analysis with retry logic"""
        last_exception = None
        
        for attempt in range(self._max_retry_attempts):
            try:
                response = await provider.analyze_job(job_description, company_context)
                return response
                
            except RateLimitError as e:
                if attempt < self._max_retry_attempts - 1:
                    delay = self._retry_delay_base * (2 ** attempt)
                    await asyncio.sleep(delay)
                last_exception = e
                
            except AuthenticationError as e:
                raise  # Don't retry auth errors
                
            except LLMProviderError as e:
                if attempt < self._max_retry_attempts - 1:
                    delay = self._retry_delay_base * (2 ** attempt)
                    await asyncio.sleep(delay)
                last_exception = e
        
        if last_exception:
            raise last_exception
        raise LLMProviderError("All retry attempts failed", provider.provider_name)
    
    async def _enhance_extracted_skills(
        self, 
        job_analysis: JobAnalysis
    ) -> List[ExtractedSkillEnhanced]:
        """Convert and enhance LLM extracted skills"""
        enhanced_skills = []
        
        # Process technical skills
        for skill in job_analysis.technical_skills:
            enhanced_skills.append(ExtractedSkillEnhanced(
                name=skill.name,
                category=skill.category,
                skill_type=self._map_skill_type(skill.category),
                importance=self._map_importance(skill.importance),
                years_required=skill.years_required,
                context=skill.context,
                synonyms=await self._find_skill_synonyms(skill.name),
                related_skills=await self._find_related_skills(skill.name)
            ))
        
        # Process soft skills
        for skill in job_analysis.soft_skills:
            enhanced_skills.append(ExtractedSkillEnhanced(
                name=skill.name,
                category=skill.category,
                skill_type=SkillType.SOFT_SKILL,
                importance=self._map_importance(skill.importance),
                years_required=skill.years_required,
                context=skill.context,
                synonyms=await self._find_skill_synonyms(skill.name),
                related_skills=await self._find_related_skills(skill.name)
            ))
        
        return enhanced_skills
    
    async def _enhance_raw_skills(
        self, 
        skills: List[ExtractedSkill]
    ) -> List[ExtractedSkillEnhanced]:
        """Enhance raw extracted skills"""
        enhanced_skills = []
        
        for skill in skills:
            enhanced_skills.append(ExtractedSkillEnhanced(
                name=skill.name,
                category=skill.category,
                skill_type=self._map_skill_type(skill.category),
                importance=self._map_importance(skill.importance),
                years_required=skill.years_required,
                context=skill.context,
                synonyms=await self._find_skill_synonyms(skill.name),
                related_skills=await self._find_related_skills(skill.name)
            ))
        
        return enhanced_skills
    
    
    async def _generate_training_recommendations(
        self, 
        extracted_skills: List[ExtractedSkillEnhanced],
        user_id: Optional[str] = None
    ) -> List[TrainingRecommendation]:
        """Generate training recommendations based on extracted skills"""
        recommendations = []
        
        # Prioritize skills by importance
        prioritized_skills = sorted(
            extracted_skills,
            key=lambda x: self._importance_to_priority(x.importance)
        )
        
        for skill in prioritized_skills:
            # Determine priority based on importance and current skill level
            priority = self._determine_training_priority(skill, user_id)
            
            # Generate specific recommendations
            recommended_actions = await self._generate_skill_actions(skill)
            
            recommendation = TrainingRecommendation(
                skill_name=skill.name,
                skill_category=skill.category,
                priority=priority,
                recommended_actions=recommended_actions,
                estimated_duration=self._estimate_training_duration(skill),
                difficulty_level=self._estimate_training_difficulty(skill),
                prerequisite_skills=skill.related_skills[:3],  # Top 3 related skills
                learning_resources=await self._suggest_learning_resources(skill),
                success_metrics=self._define_success_metrics(skill)
            )
            
            recommendations.append(recommendation)
        
        # Limit to top 10 recommendations to avoid overwhelming users
        final_recommendations = recommendations[:10]
        return final_recommendations
    
    
    
    async def _generate_unified_skill_recommendations(
        self, 
        job_analysis: JobAnalysis,
        user_id: Optional[str] = None
    ) -> List[SkillRecommendation]:
        """Generate unified skill recommendations combining skill extraction and training recommendations"""
        skill_recommendations = []
        
        # Process technical skills
        for skill in job_analysis.technical_skills:
            skill_recommendation = await self._create_skill_recommendation(skill, SkillType.PROGRAMMING, user_id)
            skill_recommendations.append(skill_recommendation)
        
        # Process soft skills
        for skill in job_analysis.soft_skills:
            skill_recommendation = await self._create_skill_recommendation(skill, SkillType.SOFT_SKILL, user_id)
            skill_recommendations.append(skill_recommendation)
        
        # Sort by priority (high to low) and importance (critical to nice_to_have)
        skill_recommendations.sort(
            key=lambda x: (
                self._priority_sort_order(x.priority),
                self._importance_sort_order(x.importance)
            )
        )
        
        # Limit to top 15 recommendations to avoid overwhelming users
        return skill_recommendations[:15]
    
    async def _create_skill_recommendation(
        self,
        skill: ExtractedSkill,
        default_skill_type: SkillType,
        user_id: Optional[str] = None
    ) -> SkillRecommendation:
        """Create a unified skill recommendation from extracted skill data"""
        
        # Map importance to priority
        importance = self._map_importance(skill.importance)
        priority = self._importance_to_training_priority(importance)
        
        # Generate training information - use simpler methods for now
        recommended_actions = await self._generate_simple_actions(skill)
        learning_resources = await self._suggest_simple_resources(skill)
        success_metrics = self._define_simple_metrics(skill)
        
        return SkillRecommendation(
            name=skill.name,
            category=skill.category,
            skill_type=self._map_skill_type(skill.category) or default_skill_type,
            importance=importance,
            priority=priority,
            years_required=skill.years_required,
            context=skill.context,
            recommended_actions=recommended_actions,
            estimated_duration=self._estimate_duration_from_skill(skill),
            difficulty_level=self._estimate_difficulty_from_skill(skill),
            prerequisite_skills=await self._find_related_skills(skill.name),
            learning_resources=learning_resources,
            success_metrics=success_metrics,
            synonyms=await self._find_skill_synonyms(skill.name),
            related_skills=await self._find_related_skills(skill.name)
        )
    
    def _importance_to_training_priority(self, importance: SkillImportance) -> TrainingPriority:
        """Convert skill importance to training priority"""
        importance_to_priority_map = {
            SkillImportance.CRITICAL: TrainingPriority.HIGH,
            SkillImportance.IMPORTANT: TrainingPriority.HIGH,
            SkillImportance.PREFERRED: TrainingPriority.MEDIUM,
            SkillImportance.NICE_TO_HAVE: TrainingPriority.LOW
        }
        return importance_to_priority_map.get(importance, TrainingPriority.MEDIUM)
    
    def _priority_sort_order(self, priority: TrainingPriority) -> int:
        """Get sort order for priority (lower number = higher priority)"""
        priority_order = {
            TrainingPriority.HIGH: 0,
            TrainingPriority.MEDIUM: 1,
            TrainingPriority.LOW: 2
        }
        return priority_order.get(priority, 1)
    
    def _importance_sort_order(self, importance: SkillImportance) -> int:
        """Get sort order for importance (lower number = higher importance)"""
        importance_order = {
            SkillImportance.CRITICAL: 0,
            SkillImportance.IMPORTANT: 1,
            SkillImportance.PREFERRED: 2,
            SkillImportance.NICE_TO_HAVE: 3
        }
        return importance_order.get(importance, 2)
    
    async def _generate_simple_actions(self, skill: ExtractedSkill) -> List[str]:
        """Generate simple action recommendations for a skill"""
        actions = [
            f"Learn {skill.name} fundamentals through online courses",
            f"Practice {skill.name} with hands-on projects"
        ]
        if skill.category.lower() in ['programming', 'framework', 'language']:
            actions.append(f"Build a project using {skill.name}")
        return actions
    
    async def _suggest_simple_resources(self, skill: ExtractedSkill) -> List[str]:
        """Generate simple learning resource suggestions"""
        return [
            f"Official {skill.name} documentation",
            f"{skill.name} tutorials and courses",
            f"Community forums and Stack Overflow"
        ]
    
    def _define_simple_metrics(self, skill: ExtractedSkill) -> List[str]:
        """Generate simple success metrics"""
        return [
            f"Complete a {skill.name} tutorial or course",
            f"Build a functional project using {skill.name}"
        ]
    
    def _estimate_duration_from_skill(self, skill: ExtractedSkill) -> str:
        """Estimate training duration based on skill complexity"""
        if skill.years_required and skill.years_required > 2:
            return "3-6 months"
        elif skill.category.lower() in ['programming', 'framework']:
            return "2-4 months"
        else:
            return "1-2 months"
    
    def _estimate_difficulty_from_skill(self, skill: ExtractedSkill) -> DifficultyLevel:
        """Estimate difficulty based on skill and experience requirements"""
        if skill.years_required and skill.years_required > 3:
            return DifficultyLevel.ADVANCED
        elif skill.years_required and skill.years_required > 1:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.BEGINNER
    
    
    # Utility and mapping methods
    
    def _map_difficulty_level(self, difficulty: str) -> DifficultyLevel:
        """Map LLM difficulty assessment to standard enum"""
        difficulty_lower = difficulty.lower()
        if 'beginner' in difficulty_lower or 'entry' in difficulty_lower:
            return DifficultyLevel.BEGINNER
        elif 'advanced' in difficulty_lower or 'senior' in difficulty_lower:
            return DifficultyLevel.ADVANCED
        else:
            return DifficultyLevel.INTERMEDIATE
    
    def _map_skill_type(self, category: str) -> Optional[SkillType]:
        """Map skill category to standard skill type"""
        category_lower = category.lower()
        
        if 'programming' in category_lower or 'language' in category_lower:
            return SkillType.PROGRAMMING
        elif 'framework' in category_lower or 'library' in category_lower:
            return SkillType.FRAMEWORK
        elif 'database' in category_lower or 'sql' in category_lower:
            return SkillType.DATABASE
        elif 'devops' in category_lower or 'deployment' in category_lower:
            return SkillType.DEVOPS
        elif 'system' in category_lower and 'design' in category_lower:
            return SkillType.SYSTEM_DESIGN
        elif 'algorithm' in category_lower or 'data structure' in category_lower:
            return SkillType.ALGORITHMS
        elif 'test' in category_lower:
            return SkillType.TESTING
        elif 'architecture' in category_lower:
            return SkillType.ARCHITECTURE
        elif 'tool' in category_lower:
            return SkillType.TOOLS
        else:
            return SkillType.SOFT_SKILL
    
    def _map_importance(self, importance: str) -> SkillImportance:
        """Map LLM importance to standard enum"""
        importance_lower = importance.lower()
        if 'critical' in importance_lower or 'required' in importance_lower:
            return SkillImportance.CRITICAL
        elif 'important' in importance_lower or 'essential' in importance_lower:
            return SkillImportance.IMPORTANT
        elif 'preferred' in importance_lower or 'desirable' in importance_lower:
            return SkillImportance.PREFERRED
        else:
            return SkillImportance.NICE_TO_HAVE
    
    
    async def _find_skill_synonyms(self, skill_name: str) -> List[str]:
        """Find synonyms for a skill name"""
        # This could be enhanced with a proper synonym database
        # For now, return common programming synonyms
        synonyms_map = {
            'javascript': ['js', 'ecmascript'],
            'typescript': ['ts'],
            'python': ['py'],
            'postgresql': ['postgres', 'pg'],
            'mongodb': ['mongo'],
            'react': ['reactjs'],
            'angular': ['angularjs'],
            'vue': ['vuejs'],
            'node': ['nodejs', 'node.js']
        }
        
        skill_lower = skill_name.lower()
        return synonyms_map.get(skill_lower, [])
    
    async def _find_related_skills(self, skill_name: str) -> List[str]:
        """Find related skills for a given skill"""
        # This could query a skills relationship database
        # For now, return hardcoded relationships
        related_map = {
            'react': ['javascript', 'typescript', 'jsx', 'redux', 'next.js'],
            'python': ['django', 'flask', 'pandas', 'numpy', 'pytest'],
            'javascript': ['html', 'css', 'typescript', 'node.js', 'npm'],
            'sql': ['postgresql', 'mysql', 'database design', 'data modeling'],
            'aws': ['cloud computing', 'docker', 'kubernetes', 'devops']
        }
        
        skill_lower = skill_name.lower()
        return related_map.get(skill_lower, [])
    
    def _calculate_string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings using Levenshtein distance"""
        if str1 == str2:
            return 1.0
        
        # Simple implementation - could be enhanced with more sophisticated algorithms
        len1, len2 = len(str1), len(str2)
        if len1 == 0:
            return 0.0 if len2 > 0 else 1.0
        if len2 == 0:
            return 0.0
        
        # Check if one string contains the other
        if str1 in str2 or str2 in str1:
            return max(len1, len2) / min(len1, len2) * 0.8
        
        # Basic character overlap calculation
        set1, set2 = set(str1), set(str2)
        overlap = len(set1.intersection(set2))
        total_chars = len(set1.union(set2))
        
        return overlap / total_chars if total_chars > 0 else 0.0
    
    def _importance_to_priority(self, importance: SkillImportance) -> int:
        """Convert importance to numeric priority for sorting"""
        priority_map = {
            SkillImportance.CRITICAL: 1,
            SkillImportance.IMPORTANT: 2,
            SkillImportance.PREFERRED: 3,
            SkillImportance.NICE_TO_HAVE: 4
        }
        return priority_map.get(importance, 5)
    
    def _determine_training_priority(
        self, 
        skill: ExtractedSkillEnhanced, 
        user_id: Optional[str]
    ) -> TrainingPriority:
        """Determine training priority for a skill"""
        # Base priority on importance
        if skill.importance == SkillImportance.CRITICAL:
            return TrainingPriority.HIGH
        elif skill.importance == SkillImportance.IMPORTANT:
            return TrainingPriority.MEDIUM
        else:
            return TrainingPriority.LOW
    
    async def _generate_skill_actions(
        self, 
        skill: ExtractedSkillEnhanced
    ) -> List[str]:
        """Generate specific training actions for a skill"""
        actions = []
        
        # Always include fundamentals for comprehensive learning
        actions.append(f"Learn the fundamentals of {skill.name}")
        
        if skill.skill_type == SkillType.PROGRAMMING:
            actions.extend([
                f"Practice coding exercises in {skill.name}",
                f"Build a small project using {skill.name}",
                f"Read {skill.name} documentation and best practices"
            ])
        elif skill.skill_type == SkillType.FRAMEWORK:
            actions.extend([
                f"Complete {skill.name} tutorial or course",
                f"Build a sample application with {skill.name}",
                f"Study {skill.name} architecture and patterns"
            ])
        else:
            actions.extend([
                f"Study {skill.name} concepts and principles",
                f"Practice {skill.name} through hands-on exercises",
                f"Apply {skill.name} in a real-world scenario"
            ])
        
        return actions[:5]  # Limit to 5 actions
    
    def _estimate_training_duration(self, skill: ExtractedSkillEnhanced) -> str:
        """Estimate training duration for a skill"""
        if skill.years_required and skill.years_required > 2:
            return "3-6 months"
        elif skill.importance == SkillImportance.CRITICAL:
            return "4-8 weeks"
        else:
            return "2-4 weeks"
    
    def _estimate_training_difficulty(self, skill: ExtractedSkillEnhanced) -> DifficultyLevel:
        """Estimate training difficulty for a skill"""
        if skill.skill_type in [SkillType.SYSTEM_DESIGN, SkillType.ARCHITECTURE]:
            return DifficultyLevel.ADVANCED
        elif skill.skill_type in [SkillType.ALGORITHMS, SkillType.DEVOPS]:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.BEGINNER
    
    async def _suggest_learning_resources(self, skill: ExtractedSkillEnhanced) -> List[str]:
        """Suggest learning resources for a skill"""
        resources = []
        
        # Add generic resources based on skill type
        if skill.skill_type == SkillType.PROGRAMMING:
            resources.extend([
                f"Official {skill.name} documentation",
                f"{skill.name} interactive tutorials",
                f"Online coding platforms with {skill.name} exercises"
            ])
        elif skill.skill_type == SkillType.FRAMEWORK:
            resources.extend([
                f"{skill.name} official getting started guide",
                f"Video course on {skill.name}",
                f"Community examples and templates"
            ])
        else:
            resources.extend([
                f"Online course on {skill.name}",
                f"Books about {skill.name}",
                f"Professional blogs and articles"
            ])
        
        return resources[:3]  # Limit to 3 resources
    
    def _define_success_metrics(self, skill: ExtractedSkillEnhanced) -> List[str]:
        """Define success metrics for learning a skill"""
        metrics = []
        
        if skill.skill_type == SkillType.PROGRAMMING:
            metrics.extend([
                f"Complete coding challenges in {skill.name}",
                f"Build and deploy a project using {skill.name}",
                f"Pass technical interview questions about {skill.name}"
            ])
        elif skill.skill_type == SkillType.FRAMEWORK:
            metrics.extend([
                f"Build a functional application with {skill.name}",
                f"Understand {skill.name} core concepts",
                f"Follow {skill.name} best practices"
            ])
        else:
            metrics.extend([
                f"Demonstrate understanding of {skill.name} principles",
                f"Apply {skill.name} in practical scenarios",
                f"Explain {skill.name} concepts clearly"
            ])
        
        return metrics[:3]  # Limit to 3 metrics
    
    def _map_years_to_level(self, years: int) -> str:
        """Map years of experience to proficiency level"""
        if years >= 5:
            return "expert"
        elif years >= 3:
            return "advanced"
        elif years >= 1:
            return "intermediate"
        else:
            return "beginner"
    
    def _calculate_gap_severity(
        self, 
        required_level: str, 
        current_level: Optional[str], 
        importance: SkillImportance
    ) -> TrainingPriority:
        """Calculate gap severity based on required vs current level"""
        level_scores = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
        
        required_score = level_scores.get(required_level, 2)
        current_score = level_scores.get(current_level, 0) if current_level else 0
        
        gap = required_score - current_score
        
        # Adjust based on importance
        if importance == SkillImportance.CRITICAL:
            if gap >= 2:
                return TrainingPriority.HIGH
            elif gap >= 1:
                return TrainingPriority.MEDIUM
            else:
                return TrainingPriority.LOW
        elif importance == SkillImportance.IMPORTANT:
            if gap >= 3:
                return TrainingPriority.HIGH
            elif gap >= 2:
                return TrainingPriority.MEDIUM
            else:
                return TrainingPriority.LOW
        else:
            return TrainingPriority.LOW
    
    def _estimate_gap_study_time(
        self, 
        required_level: str, 
        current_level: Optional[str], 
        skill_category: str
    ) -> int:
        """Estimate study time to bridge skill gap (in hours)"""
        level_scores = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
        
        required_score = level_scores.get(required_level, 2)
        current_score = level_scores.get(current_level, 0) if current_level else 0
        
        gap = required_score - current_score
        
        # Base hours per level gap
        base_hours = 40
        
        # Adjust based on skill category complexity
        if 'system design' in skill_category.lower() or 'architecture' in skill_category.lower():
            base_hours = 60
        elif 'algorithm' in skill_category.lower():
            base_hours = 50
        elif 'programming' in skill_category.lower():
            base_hours = 30
        
        return max(10, gap * base_hours)  # Minimum 10 hours


# Global service instance
_job_analysis_service: Optional[JobAnalysisService] = None


async def get_job_analysis_service() -> JobAnalysisService:
    """Get or create the global job analysis service instance"""
    global _job_analysis_service
    if _job_analysis_service is None:
        _job_analysis_service = JobAnalysisService()
    return _job_analysis_service
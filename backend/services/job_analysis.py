"""
Job Analysis Service for the Interview Trainer application.

This service orchestrates the complete job analysis workflow using the LLM abstraction layer
to analyze job descriptions, extract skills, match them with existing database entries,
and generate personalized training recommendations.

Key Features:
- Complete job description analysis using LLM providers
- Skills extraction and matching with database
- Training recommendations based on skill gaps
- Caching for expensive LLM operations
- Comprehensive error handling and retry logic
- Performance optimization and metrics tracking
"""

import asyncio
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from uuid import uuid4

from database import fetch_all, fetch_one, execute, fetch_val
from schemas.job_analysis import (
    JobAnalysisRequest, JobAnalysisResponse, JobAnalysisResult,
    ExtractedSkillEnhanced, SkillMatch, TrainingRecommendation, SkillGapAnalysis,
    AnalysisStatus, SkillImportance, TrainingPriority, JobAnalysisCache,
    AnalysisMetrics, BulkJobAnalysisRequest, BulkJobAnalysisResponse
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
        self._cache_expiry_hours = 24  # Cache results for 24 hours
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
        1. Check cache for existing analysis
        2. Extract skills using LLM provider
        3. Match skills with database entries
        4. Generate training recommendations
        5. Calculate readiness scores
        6. Cache results for future use
        
        Args:
            request: Job analysis request with description and context
            
        Returns:
            JobAnalysisResponse with complete analysis results
        """
        start_time = time.time()
        analysis_id = str(uuid4())
        
        
        try:
            # Check cache first
            cached_result = await self._get_cached_analysis(request)
            if cached_result:
                self._metrics.cache_hits += 1
                return JobAnalysisResponse(
                    success=True,
                    status=AnalysisStatus.CACHED,
                    result=cached_result.analysis_result,
                    cache_hit=True,
                    analysis_id=analysis_id,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            self._metrics.cache_misses += 1
            
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
            
            # Extract and enhance skills
            job_analysis = JobAnalysis(**llm_response.data)
            enhanced_skills = await self._enhance_extracted_skills(job_analysis)
            
            # Match skills with database
            skill_matches = await self._match_skills_with_database(enhanced_skills)
            matched_count = len([m for m in skill_matches if not m.is_new_skill])
            new_count = len([m for m in skill_matches if m.is_new_skill])
            
            # Generate training recommendations
            training_recommendations = await self._generate_training_recommendations(
                skill_matches, request.user_id
            )
            
            # Calculate skill gaps if user provided
            skill_gaps = []
            readiness_score = None
            if request.user_id:
                skill_gaps = await self._analyze_skill_gaps(skill_matches, request.user_id)
                readiness_score = await self._calculate_readiness_score(skill_gaps)
            
            # Build comprehensive result
            result = JobAnalysisResult(
                job_title=job_analysis.job_title or request.job_title,
                company_name=request.company_name,
                industry=job_analysis.industry,
                key_requirements=job_analysis.key_requirements,
                extracted_skills=enhanced_skills,
                skill_matches=skill_matches,
                experience_level=job_analysis.experience_level,
                difficulty_assessment=self._map_difficulty_level(job_analysis.difficulty_assessment),
                role_summary=job_analysis.summary,
                training_recommendations=training_recommendations,
                skill_gaps=skill_gaps,
                readiness_score=readiness_score,
                analysis_metadata={
                    "llm_provider": llm_provider.provider_name,
                    "analysis_depth": request.analysis_depth,
                    "skills_count": len(enhanced_skills),
                    "matches_found": len([m for m in skill_matches if not m.is_new_skill]),
                    "new_skills": len([m for m in skill_matches if m.is_new_skill])
                }
            )
            
            # Cache the result
            await self._cache_analysis_result(request, result, llm_response)
            
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
        return await self._generate_training_recommendations(analysis.skill_matches, user_id)
    
    async def match_existing_skills(
        self, 
        extracted_skills: List[ExtractedSkillEnhanced]
    ) -> List[SkillMatch]:
        """
        Match extracted skills against existing database skills.
        
        Args:
            extracted_skills: Skills extracted from analysis
            
        Returns:
            List of skill matches with confidence scores
        """
        return await self._match_skills_with_database(extracted_skills)
    
    async def bulk_analyze_jobs(
        self, 
        request: BulkJobAnalysisRequest
    ) -> BulkJobAnalysisResponse:
        """
        Analyze multiple job descriptions in parallel.
        
        Args:
            request: Bulk analysis request
            
        Returns:
            BulkJobAnalysisResponse with all results
        """
        start_time = time.time()
        batch_id = request.batch_id or str(uuid4())
        
        
        # Create individual analysis requests
        analysis_requests = []
        for i, job_description in enumerate(request.job_descriptions):
            analysis_requests.append(JobAnalysisRequest(
                job_description=job_description,
                analysis_depth=request.analysis_depth,
                user_id=request.user_id,
                job_title=f"Job {i+1}"  # Default title for bulk
            ))
        
        # Run analyses in parallel with concurrency limit
        semaphore = asyncio.Semaphore(5)  # Limit concurrent analyses
        
        async def analyze_with_semaphore(req):
            async with semaphore:
                return await self.analyze_job_description(req)
        
        results = await asyncio.gather(
            *[analyze_with_semaphore(req) for req in analysis_requests],
            return_exceptions=True
        )
        
        # Process results
        successful_results = []
        failed_count = 0
        total_tokens = 0
        
        for result in results:
            if isinstance(result, Exception):
                failed_count += 1
                # Create error response
                successful_results.append(JobAnalysisResponse(
                    success=False,
                    status=AnalysisStatus.FAILED,
                    error_message=str(result),
                    analysis_id=str(uuid4())
                ))
            else:
                successful_results.append(result)
                if result.tokens_used:
                    total_tokens += result.tokens_used
                if not result.success:
                    failed_count += 1
        
        processing_time = (time.time() - start_time) * 1000
        
        return BulkJobAnalysisResponse(
            success=failed_count < len(request.job_descriptions),  # Success if at least one succeeded
            batch_id=batch_id,
            total_jobs=len(request.job_descriptions),
            successful_analyses=len(request.job_descriptions) - failed_count,
            failed_analyses=failed_count,
            results=successful_results,
            processing_time_ms=processing_time,
            total_tokens_used=total_tokens if total_tokens > 0 else None
        )
    
    async def get_analysis_metrics(self) -> AnalysisMetrics:
        """Get current analysis metrics and statistics"""
        # Update most analyzed skills from database
        skills_query = """
            SELECT skill_name, COUNT(*) as analysis_count
            FROM job_analysis_cache_skills
            GROUP BY skill_name
            ORDER BY analysis_count DESC
            LIMIT 10
        """
        
        try:
            skill_stats = await fetch_all(skills_query)
            self._metrics.most_analyzed_skills = [
                {"skill": row["skill_name"], "count": row["analysis_count"]}
                for row in skill_stats
            ]
        except Exception as e:
            pass
        
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
                confidence_score=self._calculate_skill_confidence(skill),
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
                confidence_score=self._calculate_skill_confidence(skill),
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
                confidence_score=self._calculate_skill_confidence(skill),
                synonyms=await self._find_skill_synonyms(skill.name),
                related_skills=await self._find_related_skills(skill.name)
            ))
        
        return enhanced_skills
    
    async def _match_skills_with_database(
        self, 
        extracted_skills: List[ExtractedSkillEnhanced]
    ) -> List[SkillMatch]:
        """Match extracted skills with database entries"""
        skill_matches = []
        
        # Get all existing skills from database
        existing_skills_query = """
            SELECT DISTINCT name, category, type
            FROM skill_cards
            ORDER BY name
        """
        
        try:
            existing_skills = await fetch_all(existing_skills_query)
            existing_skill_names = {skill['name'].lower(): skill for skill in existing_skills}
            
            for extracted_skill in extracted_skills:
                match = await self._find_best_skill_match(
                    extracted_skill, 
                    existing_skill_names
                )
                skill_matches.append(match)
                
        except Exception as e:
            # If database matching fails, treat all as new skills
            for extracted_skill in extracted_skills:
                skill_matches.append(SkillMatch(
                    extracted_skill=extracted_skill,
                    match_confidence=0.0,
                    match_type="no_database",
                    is_new_skill=True
                ))
        
        return skill_matches
    
    async def _find_best_skill_match(
        self, 
        extracted_skill: ExtractedSkillEnhanced,
        existing_skills: Dict[str, Dict[str, Any]]
    ) -> SkillMatch:
        """Find the best match for an extracted skill"""
        skill_name_lower = extracted_skill.name.lower()
        
        # Check for exact match
        if skill_name_lower in existing_skills:
            existing_skill = existing_skills[skill_name_lower]
            return SkillMatch(
                extracted_skill=extracted_skill,
                matched_skill_id=str(hash(existing_skill['name'])),  # Temporary ID
                matched_skill_name=existing_skill['name'],
                match_confidence=self._exact_match_threshold,
                match_type="exact",
                is_new_skill=False
            )
        
        # Check synonyms
        for synonym in extracted_skill.synonyms:
            if synonym.lower() in existing_skills:
                existing_skill = existing_skills[synonym.lower()]
                return SkillMatch(
                    extracted_skill=extracted_skill,
                    matched_skill_id=str(hash(existing_skill['name'])),
                    matched_skill_name=existing_skill['name'],
                    match_confidence=self._synonym_match_threshold,
                    match_type="synonym",
                    is_new_skill=False
                )
        
        # Check partial matches
        best_match = None
        best_confidence = 0.0
        
        for existing_name, existing_skill in existing_skills.items():
            confidence = self._calculate_string_similarity(skill_name_lower, existing_name)
            
            if confidence > self._partial_match_threshold and confidence > best_confidence:
                best_confidence = confidence
                best_match = SkillMatch(
                    extracted_skill=extracted_skill,
                    matched_skill_id=str(hash(existing_skill['name'])),
                    matched_skill_name=existing_skill['name'],
                    match_confidence=confidence,
                    match_type="partial",
                    is_new_skill=False
                )
        
        if best_match:
            return best_match
        
        # No match found - it's a new skill
        return SkillMatch(
            extracted_skill=extracted_skill,
            match_confidence=0.0,
            match_type="new",
            is_new_skill=True
        )
    
    async def _generate_training_recommendations(
        self, 
        skill_matches: List[SkillMatch],
        user_id: Optional[str] = None
    ) -> List[TrainingRecommendation]:
        """Generate training recommendations based on skill matches"""
        recommendations = []
        
        # Prioritize skills by importance and match status
        prioritized_skills = sorted(
            skill_matches,
            key=lambda x: (
                self._importance_to_priority(x.extracted_skill.importance),
                -x.match_confidence if not x.is_new_skill else 1.0
            )
        )
        
        for skill_match in prioritized_skills:
            skill = skill_match.extracted_skill
            
            # Determine priority based on importance and current skill level
            priority = self._determine_training_priority(skill, skill_match, user_id)
            
            # Generate specific recommendations
            recommended_actions = await self._generate_skill_actions(skill, skill_match)
            
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
    
    async def _analyze_skill_gaps(
        self, 
        skill_matches: List[SkillMatch],
        user_id: str
    ) -> List[SkillGapAnalysis]:
        """Analyze skill gaps for a specific user"""
        skill_gaps = []
        
        # Get user's current skill levels (this would query user progress data)
        user_skills_query = """
            SELECT skill_name, proficiency_level, years_experience
            FROM user_skills
            WHERE user_id = $1
        """
        
        try:
            user_skills = await fetch_all(user_skills_query, user_id)
            user_skill_levels = {
                skill['skill_name'].lower(): {
                    'level': skill['proficiency_level'],
                    'years': skill['years_experience']
                }
                for skill in user_skills
            }
            
            for skill_match in skill_matches:
                skill = skill_match.extracted_skill
                skill_name_lower = skill.name.lower()
                
                # Determine required level
                required_level = self._map_years_to_level(skill.years_required or 0)
                
                # Get current level
                current_level = None
                if skill_name_lower in user_skill_levels:
                    current_level = user_skill_levels[skill_name_lower]['level']
                
                # Calculate gap severity
                gap_severity = self._calculate_gap_severity(
                    required_level, current_level, skill.importance
                )
                
                # Estimate study time
                study_time = self._estimate_gap_study_time(
                    required_level, current_level, skill.category
                )
                
                skill_gaps.append(SkillGapAnalysis(
                    skill_name=skill.name,
                    required_level=required_level,
                    current_level=current_level,
                    gap_severity=gap_severity,
                    estimated_study_time=study_time
                ))
                
        except Exception as e:
            pass
        
        return skill_gaps
    
    async def _calculate_readiness_score(self, skill_gaps: List[SkillGapAnalysis]) -> float:
        """Calculate overall readiness score based on skill gaps"""
        if not skill_gaps:
            return 0.8  # Default score when no user data available
        
        # Weight gaps by severity
        severity_weights = {
            TrainingPriority.HIGH: 1.0,
            TrainingPriority.MEDIUM: 0.7,
            TrainingPriority.LOW: 0.3
        }
        
        total_weight = 0
        readiness_sum = 0
        
        for gap in skill_gaps:
            weight = severity_weights.get(gap.gap_severity, 0.5)
            total_weight += weight
            
            # Calculate individual readiness (1.0 = no gap, 0.0 = maximum gap)
            if gap.current_level is None:
                individual_readiness = 0.2  # Assume some basic knowledge
            else:
                level_mapping = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
                current_score = level_mapping.get(gap.current_level, 1)
                required_score = level_mapping.get(gap.required_level, 2)
                individual_readiness = min(1.0, current_score / required_score)
            
            readiness_sum += individual_readiness * weight
        
        return readiness_sum / total_weight if total_weight > 0 else 0.5
    
    # Caching methods
    
    async def _get_cached_analysis(
        self, 
        request: JobAnalysisRequest
    ) -> Optional[JobAnalysisCache]:
        """Retrieve cached analysis result if available"""
        description_hash = self._hash_job_description(request.job_description)
        
        query = """
            SELECT analysis_result, llm_provider, tokens_used, expires_at, hit_count
            FROM job_analysis_cache
            WHERE job_description_hash = $1 AND expires_at > NOW()
            ORDER BY created_at DESC
            LIMIT 1
        """
        
        try:
            cached_row = await fetch_one(query, description_hash)
            if cached_row:
                # Update hit count and last accessed
                await execute(
                    "UPDATE job_analysis_cache SET hit_count = hit_count + 1, last_accessed = NOW() WHERE job_description_hash = $1",
                    description_hash
                )
                
                return JobAnalysisCache(
                    id="cached",
                    job_description_hash=description_hash,
                    analysis_request=request,
                    analysis_result=JobAnalysisResult(**json.loads(cached_row['analysis_result'])),
                    llm_provider=cached_row['llm_provider'],
                    tokens_used=cached_row['tokens_used'],
                    expires_at=cached_row['expires_at'],
                    hit_count=cached_row['hit_count'],
                    createdAt=datetime.utcnow()
                )
        except Exception as e:
            pass
        
        return None
    
    async def _cache_analysis_result(
        self, 
        request: JobAnalysisRequest,
        result: JobAnalysisResult, 
        llm_response
    ) -> None:
        """Cache analysis result for future use"""
        description_hash = self._hash_job_description(request.job_description)
        expires_at = datetime.utcnow() + timedelta(hours=self._cache_expiry_hours)
        
        cache_query = """
            INSERT INTO job_analysis_cache (
                job_description_hash, analysis_request, analysis_result,
                llm_provider, tokens_used, expires_at
            ) VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (job_description_hash) DO UPDATE SET
                analysis_result = EXCLUDED.analysis_result,
                llm_provider = EXCLUDED.llm_provider,
                tokens_used = EXCLUDED.tokens_used,
                expires_at = EXCLUDED.expires_at,
                updated_at = NOW()
        """
        
        try:
            await execute(
                cache_query,
                description_hash,
                json.dumps(request.model_dump()),
                json.dumps(result.model_dump()),
                llm_response.provider,
                llm_response.tokens_used,
                expires_at
            )
        except Exception as e:
            pass
    
    def _hash_job_description(self, job_description: str) -> str:
        """Create hash of job description for cache key"""
        return hashlib.sha256(job_description.encode('utf-8')).hexdigest()[:16]
    
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
    
    def _calculate_skill_confidence(self, skill: ExtractedSkill) -> float:
        """Calculate confidence score for extracted skill"""
        # Base confidence from context clarity
        confidence = 0.7
        
        # Increase if specific context provided
        if skill.context and len(skill.context) > 20:
            confidence += 0.1
        
        # Increase if years requirement specified
        if skill.years_required is not None:
            confidence += 0.1
        
        # Increase if importance is explicit
        if skill.importance in ['critical', 'required', 'important']:
            confidence += 0.1
        
        return min(1.0, confidence)
    
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
        skill_match: SkillMatch, 
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
        skill: ExtractedSkillEnhanced, 
        skill_match: SkillMatch
    ) -> List[str]:
        """Generate specific training actions for a skill"""
        actions = []
        
        if skill_match.is_new_skill:
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
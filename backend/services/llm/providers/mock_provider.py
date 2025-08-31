"""
Mock LLM provider for development and testing.

This provider simulates realistic LLM responses without making external API calls,
allowing for consistent testing and development without API costs or rate limits.
"""

import asyncio
import random
import time
from typing import Optional, Dict, Any, List

from ..base import (
    LLMProvider, 
    LLMResponse, 
    JobAnalysis, 
    ExtractedSkill,
    LLMProviderError
)
from ..config import MockConfig




class MockProvider(LLMProvider):
    """
    Mock LLM provider that returns realistic responses without external API calls.
    
    Features:
    - Simulates realistic job analysis and skill extraction
    - Configurable delay and failure rate for testing
    - Deterministic responses based on input content
    - Comprehensive coverage of different job types and industries
    """
    
    def __init__(self, config: MockConfig):
        super().__init__(config.model_dump())
        self.mock_config = config
        self.supports_streaming = False
        self.supports_function_calling = True
    
    async def analyze_job(self, job_description: str, company_context: Optional[str] = None) -> LLMResponse:
        """
        Analyze a job description and return mock job analysis.
        
        Args:
            job_description: Job description text to analyze
            company_context: Optional company context
            
        Returns:
            LLMResponse containing JobAnalysis data
        """
        start_time = time.time()

        
        try:
            # Simulate processing delay
            if self.mock_config.simulate_delay:
                await asyncio.sleep(self.mock_config.delay_seconds)
            
            # Simulate random failures
            if random.random() < self.mock_config.failure_rate:
                raise LLMProviderError(
                    "Simulated provider failure", 
                    self.provider_name
                )
            
            # Generate mock analysis based on job content
            analysis = self._generate_mock_job_analysis(job_description, company_context)
            
            processing_time = (time.time() - start_time) * 1000
            tokens_used = self._estimate_tokens(job_description)
            
            return self._create_success_response(
                analysis,
                tokens_used=tokens_used,
                processing_time_ms=processing_time
            )
            
        except LLMProviderError:
            raise
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return self._create_error_response(
                f"Mock analysis failed: {str(e)}",
                processing_time_ms=processing_time
            )
    
    async def extract_skills(self, text: str, context_type: str = "job_description") -> LLMResponse:
        """
        Extract skills from text content.
        
        Args:
            text: Text to analyze for skills
            context_type: Type of content being analyzed
            
        Returns:
            LLMResponse containing list of ExtractedSkill objects
        """
        start_time = time.time()
        
        try:
            # Simulate processing delay
            if self.mock_config.simulate_delay:
                await asyncio.sleep(self.mock_config.delay_seconds * 0.5)  # Shorter delay for skill extraction
            
            # Simulate random failures
            if random.random() < self.mock_config.failure_rate:
                raise LLMProviderError(
                    "Simulated provider failure", 
                    self.provider_name
                )
            
            # Generate mock skills based on text content
            skills = self._generate_mock_skills(text, context_type)
            
            processing_time = (time.time() - start_time) * 1000
            tokens_used = self._estimate_tokens(text)
            
            return self._create_success_response(
                {"skills": [skill.model_dump() for skill in skills]},
                tokens_used=tokens_used,
                processing_time_ms=processing_time
            )
            
        except LLMProviderError:
            raise
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return self._create_error_response(
                f"Mock skill extraction failed: {str(e)}",
                processing_time_ms=processing_time
            )
    
    def _extract_job_title(self, job_description: str) -> Optional[str]:
        """Extract job title from job description using keyword matching"""
        desc_lower = job_description.lower()
        
        # Common job title patterns - look for these in the first few lines
        first_paragraph = desc_lower.split('\n')[0:3]  # First 3 lines
        first_text = ' '.join(first_paragraph)

        
        # Job title patterns with variations
        job_patterns = [
            # Developer roles
            (r'senior\s+(?:software\s+)?(?:engineer|developer)', 'Senior Software Engineer'),
            (r'junior\s+(?:software\s+)?(?:engineer|developer)', 'Junior Software Engineer'),
            (r'lead\s+(?:software\s+)?(?:engineer|developer)', 'Lead Software Engineer'),
            (r'principal\s+(?:software\s+)?(?:engineer|developer)', 'Principal Software Engineer'),
            (r'staff\s+(?:software\s+)?(?:engineer|developer)', 'Staff Software Engineer'),
            (r'(?:senior\s+)?frontend\s+(?:engineer|developer)', 'Senior Frontend Developer' if 'senior' in first_text else 'Frontend Developer'),
            (r'(?:senior\s+)?backend\s+(?:engineer|developer)', 'Senior Backend Developer' if 'senior' in first_text else 'Backend Developer'),
            (r'(?:senior\s+)?full.?stack\s+(?:engineer|developer)', 'Senior Full Stack Developer' if 'senior' in first_text else 'Full Stack Developer'),
            (r'(?:senior\s+)?mobile\s+(?:engineer|developer)', 'Senior Mobile Developer' if 'senior' in first_text else 'Mobile Developer'),
            (r'(?:senior\s+)?react\s+(?:engineer|developer)', 'Senior React Developer' if 'senior' in first_text else 'React Developer'),
            (r'(?:senior\s+)?node\.?js\s+(?:engineer|developer)', 'Senior Node.js Developer' if 'senior' in first_text else 'Node.js Developer'),
            (r'(?:senior\s+)?python\s+(?:engineer|developer)', 'Senior Python Developer' if 'senior' in first_text else 'Python Developer'),
            
            # DevOps roles
            (r'(?:senior\s+)?devops\s+engineer', 'Senior DevOps Engineer' if 'senior' in first_text else 'DevOps Engineer'),
            (r'(?:senior\s+)?site\s+reliability\s+engineer', 'Senior Site Reliability Engineer' if 'senior' in first_text else 'Site Reliability Engineer'),
            (r'(?:senior\s+)?cloud\s+engineer', 'Senior Cloud Engineer' if 'senior' in first_text else 'Cloud Engineer'),
            (r'(?:senior\s+)?infrastructure\s+engineer', 'Senior Infrastructure Engineer' if 'senior' in first_text else 'Infrastructure Engineer'),
            
            # Data roles
            (r'(?:senior\s+)?data\s+scientist', 'Senior Data Scientist' if 'senior' in first_text else 'Data Scientist'),
            (r'(?:senior\s+)?data\s+engineer', 'Senior Data Engineer' if 'senior' in first_text else 'Data Engineer'),
            (r'(?:senior\s+)?data\s+analyst', 'Senior Data Analyst' if 'senior' in first_text else 'Data Analyst'),
            (r'machine\s+learning\s+engineer', 'Machine Learning Engineer'),
            
            # Product/Design roles
            (r'(?:senior\s+)?product\s+manager', 'Senior Product Manager' if 'senior' in first_text else 'Product Manager'),
            (r'(?:senior\s+)?ui/ux\s+designer', 'Senior UI/UX Designer' if 'senior' in first_text else 'UI/UX Designer'),
            (r'(?:senior\s+)?ux\s+designer', 'Senior UX Designer' if 'senior' in first_text else 'UX Designer'),
            
            # Leadership roles
            (r'engineering\s+manager', 'Engineering Manager'),
            (r'technical\s+lead', 'Technical Lead'),
            (r'architect', 'Software Architect'),
            (r'cto|chief\s+technology\s+officer', 'Chief Technology Officer'),
            
            # General fallbacks
            (r'(?:senior\s+)?software\s+engineer', 'Senior Software Engineer' if 'senior' in first_text else 'Software Engineer'),
            (r'(?:senior\s+)?developer', 'Senior Developer' if 'senior' in first_text else 'Software Developer'),
            (r'(?:senior\s+)?engineer', 'Senior Engineer' if 'senior' in first_text else 'Software Engineer'),
        ]
        
        import re
        
        # Try to match job title patterns
        for pattern, title in job_patterns:
            if re.search(pattern, first_text):
                return title
        
        # If no pattern matched, try to extract from common job posting formats
        # Look for patterns like "Job Title: XXX" or "Position: XXX" or "Role: XXX"
        title_markers = [r'job\s+title:\s*([^\n]+)', r'position:\s*([^\n]+)', r'role:\s*([^\n]+)', r'we.*looking.*for.*([^\n]+)']
        
        for marker in title_markers:
            match = re.search(marker, first_text, re.IGNORECASE)
            if match:
                extracted = match.group(1).strip()
                if len(extracted) > 5 and len(extracted) < 100:  # Reasonable title length
                    return extracted.title()
        
        return None

    def _generate_mock_job_analysis(self, job_description: str, company_context: Optional[str]) -> JobAnalysis:
        """Generate realistic mock job analysis based on job description content."""
        # Extract job title from description
        job_title = self._extract_job_title(job_description)
        
        # Analyze job content to determine type and requirements
        desc_lower = job_description.lower()
        
        # Determine job characteristics
        is_senior = any(term in desc_lower for term in ["senior", "lead", "principal", "architect", "director"])
        is_junior = any(term in desc_lower for term in ["junior", "entry", "graduate", "intern"])
        is_backend = any(term in desc_lower for term in ["backend", "api", "server", "database", "microservices"])
        is_frontend = any(term in desc_lower for term in ["frontend", "react", "vue", "angular", "ui", "ux"])
        is_fullstack = any(term in desc_lower for term in ["fullstack", "full-stack", "full stack"])
        is_devops = any(term in desc_lower for term in ["devops", "cloud", "aws", "docker", "kubernetes", "infrastructure"])
        is_mobile = any(term in desc_lower for term in ["mobile", "ios", "android", "react native", "flutter"])
        is_data = any(term in desc_lower for term in ["data", "analytics", "machine learning", "ai", "python", "sql"])
        
        # Determine experience level
        if is_senior:
            experience_level = "senior"
        elif is_junior:
            experience_level = "junior"
        else:
            experience_level = "mid"
        
        
        # Determine industry
        industry = "technology"
        if any(term in desc_lower for term in ["fintech", "finance", "banking"]):
            industry = "fintech"
        elif any(term in desc_lower for term in ["healthcare", "medical", "biotech"]):
            industry = "healthcare"
        elif any(term in desc_lower for term in ["ecommerce", "e-commerce", "retail"]):
            industry = "ecommerce"
        elif any(term in desc_lower for term in ["startup", "scale-up"]):
            industry = "startup"
        
        # Generate technical skills based on job type
        technical_skills = []
        
        if is_backend or is_fullstack:
            technical_skills.extend([
                ExtractedSkill(
                    name="Python",
                    category="programming",
                    importance="critical",
                    years_required=3 if is_senior else 1 if is_junior else 2,
                    context="Backend development and API design"
                ),
                ExtractedSkill(
                    name="FastAPI",
                    category="framework",
                    importance="important",
                    years_required=1 if is_senior else None,
                    context="Building REST APIs"
                ),
                ExtractedSkill(
                    name="PostgreSQL",
                    category="database",
                    importance="important",
                    years_required=2 if is_senior else 1,
                    context="Database design and optimization"
                )
            ])
        
        if is_frontend or is_fullstack:
            technical_skills.extend([
                ExtractedSkill(
                    name="React",
                    category="framework",
                    importance="critical",
                    years_required=2 if is_senior else 1,
                    context="Frontend component development"
                ),
                ExtractedSkill(
                    name="TypeScript",
                    category="programming",
                    importance="important",
                    years_required=1 if is_senior else None,
                    context="Type-safe JavaScript development"
                ),
                ExtractedSkill(
                    name="CSS",
                    category="programming",
                    importance="important",
                    context="Responsive design and styling"
                )
            ])
        
        if is_devops:
            technical_skills.extend([
                ExtractedSkill(
                    name="AWS",
                    category="devops",
                    importance="critical",
                    years_required=2 if is_senior else 1,
                    context="Cloud infrastructure management"
                ),
                ExtractedSkill(
                    name="Docker",
                    category="devops",
                    importance="important",
                    years_required=1,
                    context="Containerization and deployment"
                ),
                ExtractedSkill(
                    name="Kubernetes",
                    category="devops",
                    importance="preferred" if is_junior else "important",
                    years_required=1 if not is_junior else None,
                    context="Container orchestration"
                )
            ])
        
        if is_mobile:
            technical_skills.extend([
                ExtractedSkill(
                    name="React Native",
                    category="framework",
                    importance="critical",
                    years_required=2 if is_senior else 1,
                    context="Cross-platform mobile development"
                ),
                ExtractedSkill(
                    name="JavaScript",
                    category="programming",
                    importance="critical",
                    years_required=3 if is_senior else 2,
                    context="Mobile app development"
                )
            ])
        
        if is_data:
            technical_skills.extend([
                ExtractedSkill(
                    name="Python",
                    category="programming",
                    importance="critical",
                    years_required=3 if is_senior else 2,
                    context="Data analysis and machine learning"
                ),
                ExtractedSkill(
                    name="SQL",
                    category="database",
                    importance="critical",
                    years_required=2 if is_senior else 1,
                    context="Data querying and analysis"
                ),
                ExtractedSkill(
                    name="Pandas",
                    category="framework",
                    importance="important",
                    years_required=1,
                    context="Data manipulation and analysis"
                )
            ])
        
        # Add some universal skills
        if random.random() > 0.3:  # 70% chance
            technical_skills.append(ExtractedSkill(
                name="Git",
                category="tools",
                importance="important",
                context="Version control and collaboration"
            ))
        
        # Generate soft skills
        soft_skills = [
            ExtractedSkill(
                name="Communication",
                category="soft_skill",
                importance="important",
                context="Collaborating with cross-functional teams"
            ),
            ExtractedSkill(
                name="Problem Solving",
                category="soft_skill",
                importance="critical",
                context="Analyzing complex technical challenges"
            )
        ]
        
        if is_senior:
            soft_skills.extend([
                ExtractedSkill(
                    name="Leadership",
                    category="soft_skill",
                    importance="important",
                    context="Mentoring junior developers and leading projects"
                ),
                ExtractedSkill(
                    name="Architecture Design",
                    category="soft_skill",
                    importance="important",
                    context="Designing scalable system architecture"
                )
            ])
        
        # Generate key requirements
        requirements = [
            f"Bachelor's degree in Computer Science or related field",
            f"{3 if is_senior else 1 if is_junior else 2}+ years of software development experience"
        ]
        
        if is_backend:
            requirements.append("Strong experience with backend technologies and API design")
        if is_frontend:
            requirements.append("Proficiency in modern frontend frameworks and responsive design")
        if is_devops:
            requirements.append("Experience with cloud platforms and infrastructure automation")
        
        # Generate summary
        role_type = "Senior " if is_senior else "Junior " if is_junior else ""
        domain = "Backend" if is_backend else "Frontend" if is_frontend else "Full-Stack" if is_fullstack else "DevOps" if is_devops else "Mobile" if is_mobile else "Data" if is_data else "Software"
        
        summary = f"{role_type}{domain} Developer position focusing on building scalable applications in the {industry} industry."
        
        # Determine difficulty
        difficulty = "high" if is_senior else "low" if is_junior else "medium"
        
        
        return JobAnalysis(
            job_title=job_title,
            key_requirements=requirements,
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            experience_level=experience_level,
            industry=industry,
            summary=summary,
            difficulty_assessment=difficulty
        )
    
    def _generate_mock_skills(self, text: str, context_type: str) -> List[ExtractedSkill]:
        """Generate mock skills based on text content."""
        text_lower = text.lower()
        skills = []
        
        # Common programming languages
        programming_skills = {
            "python": ("programming", "critical"),
            "javascript": ("programming", "critical"),
            "typescript": ("programming", "important"),
            "java": ("programming", "important"),
            "c#": ("programming", "important"),
            "go": ("programming", "preferred"),
            "rust": ("programming", "preferred")
        }
        
        # Frameworks and libraries
        framework_skills = {
            "react": ("framework", "critical"),
            "vue": ("framework", "important"),
            "angular": ("framework", "important"),
            "fastapi": ("framework", "important"),
            "django": ("framework", "important"),
            "flask": ("framework", "preferred"),
            "express": ("framework", "important"),
            "node.js": ("framework", "important"),
            "spring": ("framework", "important")
        }
        
        # Databases
        database_skills = {
            "postgresql": ("database", "important"),
            "mysql": ("database", "important"),
            "mongodb": ("database", "preferred"),
            "redis": ("database", "preferred"),
            "elasticsearch": ("database", "preferred")
        }
        
        # DevOps and tools
        devops_skills = {
            "docker": ("devops", "important"),
            "kubernetes": ("devops", "preferred"),
            "aws": ("devops", "important"),
            "azure": ("devops", "preferred"),
            "gcp": ("devops", "preferred"),
            "git": ("tools", "important"),
            "jenkins": ("devops", "preferred"),
            "terraform": ("devops", "preferred")
        }
        
        # Check for skills in text
        all_skills = {**programming_skills, **framework_skills, **database_skills, **devops_skills}
        
        for skill_name, (category, importance) in all_skills.items():
            if skill_name in text_lower:
                # Determine years of experience based on context
                years_required = None
                if importance == "critical":
                    years_required = random.choice([1, 2, 3])
                elif importance == "important":
                    years_required = random.choice([1, 2])
                
                skills.append(ExtractedSkill(
                    name=skill_name.title(),
                    category=category,
                    importance=importance,
                    years_required=years_required,
                    context=f"Mentioned in {context_type}"
                ))
        
        # Add some soft skills if not many technical skills found
        if len(skills) < 3:
            soft_skills_options = [
                ("Communication", "soft_skill", "important"),
                ("Problem Solving", "soft_skill", "critical"),
                ("Teamwork", "soft_skill", "important"),
                ("Adaptability", "soft_skill", "preferred")
            ]
            
            for skill_name, category, importance in soft_skills_options[:2]:
                skills.append(ExtractedSkill(
                    name=skill_name,
                    category=category,
                    importance=importance,
                    context=f"Inferred from {context_type}"
                ))
        
        return skills
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for the given text (rough approximation)."""
        # Rough estimation: ~4 characters per token
        return len(text) // 4
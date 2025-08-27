"""
Job Analyzer Service for the Interview Trainer application.
Handles analysis of job postings to extract relevant skills and requirements.
"""

import json
import logging
from typing import List, Dict, Any
from .llm_service import LLMService

logger = logging.getLogger(__name__)

class JobAnalyzer:
    """
    Service class for analyzing job postings and extracting relevant information.
    
    This service handles:
    - Skill extraction from job descriptions
    - Requirements analysis
    - Job categorization
    - Skill level assessment
    """
    
    def __init__(self):
        """Initialize the job analyzer service."""
        self.llm_service = LLMService()
    
    def extract_skills(self, description: str, requirements: str = "") -> List[Dict[str, Any]]:
        """
        Extract relevant skills from a job description and requirements.
        
        Args:
            description: The main job description text
            requirements: Additional requirements text (optional)
            
        Returns:
            List of skill dictionaries with name, category, level, and description
        """
        try:
            # Combine description and requirements for analysis
            full_text = f"{description}\n\nRequirements:\n{requirements}" if requirements else description
            
            # Use LLM to extract skills
            skills_data = self.llm_service._make_api_call(
                self._create_skill_extraction_prompt(full_text),
                max_tokens=1000
            )
            
            # Parse the response
            skills = self._parse_skills_response(skills_data)
            
            logger.info(f"Extracted {len(skills)} skills from job description")
            return skills
            
        except Exception as e:
            logger.error(f"Failed to extract skills using LLM: {e}")
            # Return fallback skills if LLM fails
            return self._get_fallback_skills(description, requirements)
    
    def analyze_job_complexity(self, description: str, requirements: str = "") -> Dict[str, Any]:
        """
        Analyze the complexity level of a job posting.
        
        Args:
            description: The job description text
            requirements: Additional requirements text
            
        Returns:
            Dictionary with complexity analysis
        """
        try:
            full_text = f"{description}\n\nRequirements:\n{requirements}" if requirements else description
            
            prompt = self._create_complexity_analysis_prompt(full_text)
            response = self.llm_service._make_api_call(prompt, max_tokens=500)
            
            # Parse complexity analysis
            analysis = self._parse_complexity_response(response)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze job complexity: {e}")
            return self._get_fallback_complexity_analysis()
    
    def categorize_job(self, title: str, description: str) -> Dict[str, Any]:
        """
        Categorize a job posting based on title and description.
        
        Args:
            title: Job title
            description: Job description
            
        Returns:
            Dictionary with job category information
        """
        try:
            full_text = f"Title: {title}\n\nDescription: {description}"
            
            prompt = self._create_job_categorization_prompt(full_text)
            response = self.llm_service._make_api_call(prompt, max_tokens=500)
            
            # Parse categorization
            category = self._parse_categorization_response(response)
            
            return category
            
        except Exception as e:
            logger.error(f"Failed to categorize job: {e}")
            return self._get_fallback_job_category()
    
    def _create_skill_extraction_prompt(self, job_text: str) -> str:
        """Create a prompt for extracting skills from job text."""
        
        prompt = f"""
        Analyze the following job posting and extract the key technical and soft skills required.
        
        Job Posting:
        {job_text}
        
        For each skill, provide:
        1. Skill name (e.g., "Python", "React", "Leadership")
        2. Category (e.g., "Programming Language", "Framework", "Soft Skill")
        3. Level (e.g., "Beginner", "Intermediate", "Advanced")
        4. Brief description of how it's used in this role
        
        Format your response as a JSON array with this structure:
        [
            {{
                "name": "Skill Name",
                "category": "Skill Category",
                "level": "Beginner/Intermediate/Advanced",
                "description": "Brief description of skill usage in this role"
            }}
        ]
        
        Focus on:
        - Technical skills (programming languages, frameworks, tools)
        - Domain knowledge (machine learning, web development, etc.)
        - Soft skills (communication, leadership, problem-solving)
        - Experience levels and requirements
        
        Make sure the response is valid JSON and includes 8-15 relevant skills.
        """
        
        return prompt.strip()
    
    def _create_complexity_analysis_prompt(self, job_text: str) -> str:
        """Create a prompt for analyzing job complexity."""
        
        prompt = f"""
        Analyze the complexity level of this job posting:
        
        {job_text}
        
        Provide analysis in JSON format:
        {{
            "overall_level": "Entry/Intermediate/Senior/Lead/Principal",
            "technical_complexity": "Low/Medium/High",
            "experience_required": "0-2 years/3-5 years/5+ years/10+ years",
            "responsibility_level": "Individual Contributor/Team Lead/Manager/Director",
            "reasoning": "Brief explanation of the complexity assessment"
        }}
        
        Consider:
        - Years of experience mentioned
        - Technical requirements complexity
        - Leadership/management responsibilities
        - Project scope and impact
        """
        
        return prompt.strip()
    
    def _create_job_categorization_prompt(self, job_text: str) -> str:
        """Create a prompt for categorizing a job."""
        
        prompt = f"""
        Categorize this job posting:
        
        {job_text}
        
        Provide categorization in JSON format:
        {{
            "primary_category": "Main job category (e.g., Software Engineering, Data Science, DevOps)",
            "sub_category": "Specific focus area (e.g., Frontend, Backend, Full Stack, ML Engineer)",
            "industry": "Industry sector (e.g., Technology, Finance, Healthcare, E-commerce)",
            "company_size": "Estimated company size (Startup, Small, Medium, Large, Enterprise)",
            "work_type": "Work arrangement (On-site, Remote, Hybrid)"
        }}
        """
        
        return prompt.strip()
    
    def _parse_skills_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse and validate the skills response from the API."""
        try:
            # Try to parse JSON response
            skills = json.loads(response)
            
            # Validate structure
            if not isinstance(skills, list):
                raise ValueError("Response is not a list")
            
            # Validate each skill
            validated_skills = []
            for skill in skills:
                if isinstance(skill, dict) and 'name' in skill:
                    validated_skills.append({
                        'name': skill.get('name', ''),
                        'category': skill.get('category', 'General'),
                        'level': skill.get('level', 'Intermediate'),
                        'description': skill.get('description', '')
                    })
            
            return validated_skills
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse skills response: {e}")
            # Return fallback skills if parsing fails
            return self._get_fallback_skills("", "")
    
    def _parse_complexity_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate the complexity analysis response."""
        try:
            analysis = json.loads(response)
            
            # Validate required fields
            required_fields = ['overall_level', 'technical_complexity', 'experience_required']
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = 'Unknown'
            
            return analysis
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse complexity response: {e}")
            return self._get_fallback_complexity_analysis()
    
    def _parse_categorization_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate the job categorization response."""
        try:
            category = json.loads(response)
            
            # Validate required fields
            required_fields = ['primary_category', 'sub_category', 'industry']
            for field in required_fields:
                if field not in category:
                    category[field] = 'Unknown'
            
            return category
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse categorization response: {e}")
            return self._get_fallback_job_category()
    
    def _get_fallback_skills(self, description: str, requirements: str) -> List[Dict[str, Any]]:
        """Return fallback skills when LLM analysis fails."""
        logger.info("Using fallback skills due to LLM failure")
        
        # Common skills that might be relevant
        fallback_skills = [
            {
                "name": "Python",
                "category": "Programming Language",
                "level": "Intermediate",
                "description": "Core programming language for development tasks"
            },
            {
                "name": "JavaScript",
                "category": "Programming Language",
                "level": "Intermediate",
                "description": "Frontend and backend web development"
            },
            {
                "name": "SQL",
                "category": "Database",
                "level": "Intermediate",
                "description": "Database querying and management"
            },
            {
                "name": "Git",
                "category": "Version Control",
                "level": "Beginner",
                "description": "Source code version control and collaboration"
            },
            {
                "name": "Problem Solving",
                "category": "Soft Skill",
                "level": "Intermediate",
                "description": "Analytical thinking and solution development"
            }
        ]
        
        return fallback_skills
    
    def _get_fallback_complexity_analysis(self) -> Dict[str, Any]:
        """Return fallback complexity analysis when LLM fails."""
        return {
            "overall_level": "Intermediate",
            "technical_complexity": "Medium",
            "experience_required": "3-5 years",
            "responsibility_level": "Individual Contributor",
            "reasoning": "Standard software engineering role with moderate complexity"
        }
    
    def _get_fallback_job_category(self) -> Dict[str, Any]:
        """Return fallback job category when LLM fails."""
        return {
            "primary_category": "Software Engineering",
            "sub_category": "Full Stack",
            "industry": "Technology",
            "company_size": "Medium",
            "work_type": "Hybrid"
        }

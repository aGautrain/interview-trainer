"""
LLM Service for the Interview Trainer application.
Handles OpenAI API integration for generating interview questions and coding exercises.
"""

import os
import json
import logging
from typing import List, Dict, Any
from openai import OpenAI
from flask import current_app

logger = logging.getLogger(__name__)

class LLMService:
    """
    Service class for interacting with OpenAI's API to generate content.
    
    This service handles:
    - Interview question generation
    - Coding exercise generation
    - Skill extraction from job descriptions
    - Response validation and formatting
    """
    
    def __init__(self):
        """Initialize the LLM service with OpenAI client."""
        self.client = None
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client with API key."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("No OpenAI API key found. Service will use mock responses.")
            return
        
        try:
            self.client = OpenAI(api_key=api_key)
            logger.info(f"OpenAI client initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def _make_api_call(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Make a call to OpenAI API.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens in the response
            
        Returns:
            The model's response text
            
        Raises:
            Exception: If API call fails
        """
        if not self.client:
            raise Exception("OpenAI client not initialized. Please check your API key.")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interview preparation assistant. Generate high-quality, relevant content based on the user's requirements."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise Exception(f"Failed to generate content: {str(e)}")
    
    def generate_questions(self, skills: List[str], question_type: str = "technical", 
                          difficulty: str = "intermediate", count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate interview questions based on skills and parameters.
        
        Args:
            skills: List of skills to base questions on
            question_type: Type of questions (technical, behavioral, situational)
            difficulty: Difficulty level (beginner, intermediate, advanced)
            count: Number of questions to generate
            
        Returns:
            List of question dictionaries with text, category, and hints
        """
        try:
            # Create prompt for question generation
            prompt = self._create_question_prompt(skills, question_type, difficulty, count)
            
            # Make API call
            response = self._make_api_call(prompt, max_tokens=1500)
            
            # Parse and validate response
            questions = self._parse_questions_response(response, count)
            
            logger.info(f"Generated {len(questions)} {difficulty} {question_type} questions")
            return questions
            
        except Exception as e:
            logger.error(f"Failed to generate questions: {e}")
            # Return fallback questions if API fails
            return self._get_fallback_questions(skills, question_type, difficulty, count)
    
    def generate_exercises(self, skills: List[str], programming_language: str = "Python",
                          difficulty: str = "intermediate", count: int = 3) -> List[Dict[str, Any]]:
        """
        Generate coding exercises based on skills and parameters.
        
        Args:
            skills: List of skills to base exercises on
            programming_language: Target programming language
            difficulty: Difficulty level (beginner, intermediate, advanced)
            count: Number of exercises to generate
            
        Returns:
            List of exercise dictionaries with title, description, solution, etc.
        """
        try:
            # Create prompt for exercise generation
            prompt = self._create_exercise_prompt(skills, programming_language, difficulty, count)
            
            # Make API call
            response = self._make_api_call(prompt, max_tokens=2000)
            
            # Parse and validate response
            exercises = self._parse_exercises_response(response, count)
            
            logger.info(f"Generated {len(exercises)} {difficulty} {programming_language} exercises")
            return exercises
            
        except Exception as e:
            logger.error(f"Failed to generate exercises: {e}")
            # Return fallback exercises if API fails
            return self._get_fallback_exercises(skills, programming_language, difficulty, count)
    
    def _create_question_prompt(self, skills: List[str], question_type: str, 
                               difficulty: str, count: int) -> str:
        """Create a prompt for generating interview questions."""
        
        skill_list = ", ".join(skills)
        
        prompt = f"""
        Generate {count} {difficulty}-level {question_type} interview questions based on these skills: {skill_list}
        
        Requirements:
        - Questions should be relevant to the specified skills
        - Difficulty should match the specified level
        - Questions should be clear and actionable
        - Include answer hints or guidance
        
        For each question, provide:
        1. The question text
        2. Category (e.g., algorithms, system design, leadership)
        3. Hints or guidance for answering
        
        Format your response as a JSON array with this structure:
        [
            {{
                "text": "Question text here",
                "category": "category_name",
                "hints": "Helpful hints for answering"
            }}
        ]
        
        Make sure the response is valid JSON and focuses on the specified skills.
        """
        
        return prompt.strip()
    
    def _create_exercise_prompt(self, skills: List[str], programming_language: str,
                               difficulty: str, count: int) -> str:
        """Create a prompt for generating coding exercises."""
        
        skill_list = ", ".join(skills)
        
        prompt = f"""
        Generate {count} {difficulty}-level coding exercises in {programming_language} based on these skills: {skill_list}
        
        Requirements:
        - Exercises should be relevant to the specified skills
        - Difficulty should match the specified level
        - Include clear problem descriptions
        - Provide sample solutions
        - Include test cases
        
        For each exercise, provide:
        1. Title
        2. Problem description
        3. Category (e.g., algorithms, data structures, system design)
        4. Sample solution
        5. Test cases
        6. Estimated time limit (in minutes)
        
        Format your response as a JSON array with this structure:
        [
            {{
                "title": "Exercise title",
                "description": "Problem description",
                "category": "category_name",
                "solution": "Sample solution code",
                "test_cases": "Example test cases",
                "time_limit": estimated_minutes
            }}
        ]
        
        Make sure the response is valid JSON and focuses on the specified skills.
        """
        
        return prompt.strip()
    
    def _parse_questions_response(self, response: str, expected_count: int) -> List[Dict[str, Any]]:
        """Parse and validate the questions response from the API."""
        try:
            # Try to parse JSON response
            questions = json.loads(response)
            
            # Validate structure
            if not isinstance(questions, list):
                raise ValueError("Response is not a list")
            
            # Ensure we have the expected number of questions
            if len(questions) < expected_count:
                logger.warning(f"Expected {expected_count} questions, got {len(questions)}")
            
            # Validate each question
            validated_questions = []
            for q in questions[:expected_count]:
                if isinstance(q, dict) and 'text' in q:
                    validated_questions.append({
                        'text': q.get('text', ''),
                        'category': q.get('category', 'general'),
                        'hints': q.get('hints', '')
                    })
            
            return validated_questions
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse questions response: {e}")
            # Return fallback questions if parsing fails
            return self._get_fallback_questions([], "technical", "intermediate", expected_count)
    
    def _parse_exercises_response(self, response: str, expected_count: int) -> List[Dict[str, Any]]:
        """Parse and validate the exercises response from the API."""
        try:
            # Try to parse JSON response
            exercises = json.loads(response)
            
            # Validate structure
            if not isinstance(exercises, list):
                raise ValueError("Response is not a list")
            
            # Ensure we have the expected number of exercises
            if len(exercises) < expected_count:
                logger.warning(f"Expected {expected_count} exercises, got {len(exercises)}")
            
            # Validate each exercise
            validated_exercises = []
            for ex in exercises[:expected_count]:
                if isinstance(ex, dict) and 'title' in ex and 'description' in ex:
                    validated_exercises.append({
                        'title': ex.get('title', ''),
                        'description': ex.get('description', ''),
                        'category': ex.get('category', 'general'),
                        'solution': ex.get('solution', ''),
                        'test_cases': ex.get('test_cases', ''),
                        'time_limit': ex.get('time_limit', 30)
                    })
            
            return validated_exercises
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse exercises response: {e}")
            # Return fallback exercises if parsing fails
            return self._get_fallback_exercises([], "Python", "intermediate", expected_count)
    
    def _get_fallback_questions(self, skills: List[str], question_type: str, 
                               difficulty: str, count: int) -> List[Dict[str, Any]]:
        """Return fallback questions when API fails."""
        logger.info("Using fallback questions due to API failure")
        
        # Simple fallback questions based on common skills
        fallback_questions = [
            {
                "text": "Explain the difference between a stack and a queue data structure.",
                "category": "data_structures",
                "hints": "Think about the order of insertion and removal operations."
            },
            {
                "text": "What is the time complexity of binary search?",
                "category": "algorithms",
                "hints": "Consider how the search space is reduced in each iteration."
            },
            {
                "text": "How would you handle a production system failure?",
                "category": "system_design",
                "hints": "Consider monitoring, alerting, and recovery procedures."
            }
        ]
        
        return fallback_questions[:count]
    
    def _get_fallback_exercises(self, skills: List[str], programming_language: str,
                                difficulty: str, count: int) -> List[Dict[str, Any]]:
        """Return fallback exercises when API fails."""
        logger.info("Using fallback exercises due to API failure")
        
        # Simple fallback exercises
        fallback_exercises = [
            {
                "title": "Reverse a String",
                "description": "Write a function to reverse a string without using built-in reverse methods.",
                "category": "algorithms",
                "solution": "# Solution code would go here",
                "test_cases": "Test with 'hello' -> 'olleh', 'world' -> 'dlrow'",
                "time_limit": 15
            },
            {
                "title": "Find Missing Number",
                "description": "Given an array containing n distinct numbers from 0 to n, find the missing number.",
                "category": "algorithms",
                "solution": "# Solution code would go here",
                "test_cases": "Test with [0,1,3] -> 2, [0,1,2,4] -> 3",
                "time_limit": 20
            }
        ]
        
        return fallback_exercises[:count]

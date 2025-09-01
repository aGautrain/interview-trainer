#!/usr/bin/env python3
"""
Simple test to verify job analysis updates work without confidence scores.
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas.job_analysis import ExtractedSkillEnhanced, JobAnalysisResult, SkillImportance
from schemas.base import SkillType, DifficultyLevel

async def test_schema_creation():
    """Test creating schemas without confidence scores"""
    print("Testing schema creation without confidence scores...")
    
    # Test ExtractedSkillEnhanced creation
    skill = ExtractedSkillEnhanced(
        name="Python",
        category="Programming Language",
        skill_type=SkillType.PROGRAMMING,
        importance=SkillImportance.CRITICAL,
        years_required=3,
        context="Experience with Python for backend development",
        synonyms=["py"],
        related_skills=["Django", "FastAPI"]
    )
    print(f"Created skill: {skill.name} - {skill.importance}")
    
    
    # Test JobAnalysisResult creation
    result = JobAnalysisResult(
        job_title="Senior Python Developer",
        company_name="Tech Corp",
        industry="Technology",
        key_requirements=["Python", "FastAPI", "PostgreSQL"],
        extracted_skills=[skill],
        experience_level="senior",
        difficulty_assessment=DifficultyLevel.ADVANCED,
        role_summary="Senior Python developer role",
        training_recommendations=[],
        analysis_metadata={}
    )
    print(f"Created result: {result.job_title}")
    
    print("All schemas created successfully without confidence scores!")
    return True

async def main():
    """Run simple test"""
    print("Simple Job Analysis Test")
    print("=" * 30)
    
    try:
        success = await test_schema_creation()
        if success:
            print("\nTest PASSED: All updates work correctly")
            return True
    except Exception as e:
        print(f"\nTest FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())
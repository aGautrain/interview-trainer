#!/usr/bin/env python3
"""
Test script for the job analysis service.
This script validates the integration between the LLM layer and job analysis service.
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from services.job_analysis import get_job_analysis_service
from schemas.job_analysis import JobAnalysisRequest
from services.llm import get_available_provider


async def test_basic_job_analysis():
    """Test basic job analysis functionality"""
    print("🔍 Testing basic job analysis...")
    
    # Sample job description
    job_description = """
    Senior Full Stack Developer Position
    
    We are seeking a Senior Full Stack Developer to join our dynamic team. 
    
    Requirements:
    - 5+ years of experience in web development
    - Strong proficiency in JavaScript, TypeScript, and Python
    - Experience with React, Node.js, and Express
    - Knowledge of PostgreSQL and MongoDB
    - Familiarity with AWS cloud services
    - Experience with Docker and CI/CD pipelines
    - Strong problem-solving skills and attention to detail
    - Excellent communication and teamwork abilities
    
    Responsibilities:
    - Design and develop scalable web applications
    - Collaborate with cross-functional teams
    - Mentor junior developers
    - Participate in code reviews and architectural decisions
    """
    
    # Create analysis request
    request = JobAnalysisRequest(
        job_description=job_description,
        job_title="Senior Full Stack Developer",
        company_name="TechCorp Inc",
        analysis_depth="standard"
    )
    
    # Get service instance
    service = await get_job_analysis_service()
    
    # Perform analysis
    print("📊 Performing job analysis...")
    start_time = datetime.now()
    
    response = await service.analyze_job_description(request)
    
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds() * 1000
    
    # Display results
    print(f"\n⏱️  Processing time: {processing_time:.2f}ms")
    print(f"✅ Analysis successful: {response.success}")
    print(f"📋 Status: {response.status}")
    print(f"🔄 Cache hit: {response.cache_hit}")
    
    if response.success and response.result:
        result = response.result
        print(f"\n📈 Analysis Results:")
        print(f"  - Industry: {result.industry}")
        print(f"  - Experience Level: {result.experience_level}")
        print(f"  - Difficulty: {result.difficulty_assessment}")
        print(f"  - Skills Extracted: {len(result.extracted_skills)}")
        print(f"  - Skills Matched: {len([m for m in result.skill_matches if not m.is_new_skill])}")
        print(f"  - New Skills: {len([m for m in result.skill_matches if m.is_new_skill])}")
        print(f"  - Training Recommendations: {len(result.training_recommendations)}")
        
        # Show top skills
        if result.extracted_skills:
            print(f"\n🔧 Top Skills Found:")
            for i, skill in enumerate(result.extracted_skills[:5]):
                print(f"  {i+1}. {skill.name} ({skill.importance})")
        
        # Show training recommendations
        if result.training_recommendations:
            print(f"\n📚 Training Recommendations:")
            for i, rec in enumerate(result.training_recommendations[:3]):
                print(f"  {i+1}. {rec.skill_name} ({rec.priority}) - {rec.estimated_duration}")
    
    elif not response.success:
        print(f"❌ Analysis failed: {response.error_message}")
    
    return response


async def test_skill_extraction():
    """Test standalone skill extraction"""
    print("\n🔍 Testing skill extraction...")
    
    text = """
    We need someone with expertise in Python, Django, React, PostgreSQL, 
    Docker, Kubernetes, AWS, and machine learning. Experience with 
    data science, pandas, numpy, and scikit-learn is preferred.
    """
    
    service = await get_job_analysis_service()
    skills = await service.extract_skills_from_text(text, "job_requirements")
    
    print(f"📊 Extracted {len(skills)} skills:")
    for skill in skills:
        print(f"  - {skill.name} ({skill.category})")


async def test_bulk_analysis():
    """Test bulk job analysis"""
    print("\n🔍 Testing bulk job analysis...")
    
    from schemas.job_analysis import BulkJobAnalysisRequest
    
    job_descriptions = [
        "Python developer needed with Django and PostgreSQL experience",
        "Frontend developer role requiring React, TypeScript, and CSS skills",
        "DevOps engineer position with Docker, Kubernetes, and AWS knowledge"
    ]
    
    request = BulkJobAnalysisRequest(
        job_descriptions=job_descriptions,
        analysis_depth="basic"
    )
    
    service = await get_job_analysis_service()
    response = await service.bulk_analyze_jobs(request)
    
    print(f"📊 Bulk analysis results:")
    print(f"  - Total jobs: {response.total_jobs}")
    print(f"  - Successful: {response.successful_analyses}")
    print(f"  - Failed: {response.failed_analyses}")
    print(f"  - Processing time: {response.processing_time_ms:.2f}ms")
    
    return response


async def test_llm_provider():
    """Test LLM provider availability"""
    print("\n🔍 Testing LLM provider...")
    
    try:
        provider = await get_available_provider()
        if provider:
            print(f"✅ LLM Provider available: {provider.provider_name}")
            
            # Test health check
            healthy = await provider.health_check()
            print(f"🏥 Health check: {'✅ Healthy' if healthy else '❌ Unhealthy'}")
            
            # Show provider info
            info = provider.get_provider_info()
            print(f"📋 Provider info: {json.dumps(info, indent=2)}")
            
            return True
        else:
            print("❌ No LLM provider available")
            return False
            
    except Exception as e:
        print(f"❌ LLM provider error: {e}")
        return False


async def test_cache_functionality():
    """Test caching functionality"""
    print("\n🔍 Testing cache functionality...")
    
    job_description = "Simple Python developer role with Flask experience"
    
    request = JobAnalysisRequest(
        job_description=job_description,
        job_title="Python Developer"
    )
    
    service = await get_job_analysis_service()
    
    # First request (should miss cache)
    print("📊 First analysis (cache miss expected)...")
    response1 = await service.analyze_job_description(request)
    print(f"  - Cache hit: {response1.cache_hit}")
    print(f"  - Processing time: {response1.processing_time_ms:.2f}ms")
    
    # Second request (should hit cache)
    print("📊 Second analysis (cache hit expected)...")
    response2 = await service.analyze_job_description(request)
    print(f"  - Cache hit: {response2.cache_hit}")
    print(f"  - Processing time: {response2.processing_time_ms:.2f}ms")
    
    # Verify cache performance improvement
    if response1.processing_time_ms and response2.processing_time_ms:
        improvement = response1.processing_time_ms / response2.processing_time_ms
        print(f"🚀 Cache performance improvement: {improvement:.2f}x faster")


async def main():
    """Run all tests"""
    print("🧪 Job Analysis Service Test Suite")
    print("=" * 50)
    
    try:
        # Test LLM provider first
        provider_available = await test_llm_provider()
        
        if not provider_available:
            print("\n⚠️  LLM provider not available. Some tests may fail.")
            print("   Make sure LLM configuration is set up properly.")
        
        # Test basic functionality
        await test_basic_job_analysis()
        
        # Test skill extraction
        await test_skill_extraction()
        
        # Test bulk analysis
        await test_bulk_analysis()
        
        # Test caching
        await test_cache_functionality()
        
        # Get service metrics
        print("\n📊 Service Metrics:")
        service = await get_job_analysis_service()
        metrics = await service.get_analysis_metrics()
        
        print(f"  - Total analyses: {metrics.total_analyses}")
        print(f"  - Successful: {metrics.successful_analyses}")
        print(f"  - Failed: {metrics.failed_analyses}")
        print(f"  - Cache hits: {metrics.cache_hits}")
        print(f"  - Cache misses: {metrics.cache_misses}")
        print(f"  - Avg processing time: {metrics.avg_processing_time_ms:.2f}ms")
        print(f"  - Total tokens used: {metrics.total_tokens_used}")
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
"""
Basic tests for the Interview Trainer application.
Tests core functionality and ensures the application can start properly.
"""

import pytest
from app import create_app, db
from app.models import JobPosting, Skill, Question, CodingExercise

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

def test_app_creation(app):
    """Test that the Flask app can be created successfully."""
    assert app is not None
    assert app.config['TESTING'] is True

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'Interview Trainer API' in data['message']

def test_models_creation(app):
    """Test that database models can be created."""
    with app.app_context():
        # Test JobPosting creation
        job = JobPosting(
            title="Software Engineer",
            company="Test Corp",
            description="A test job posting",
            location="Remote"
        )
        db.session.add(job)
        db.session.commit()
        
        assert job.id is not None
        assert job.title == "Software Engineer"
        
        # Test Skill creation
        skill = Skill(
            name="Python",
            category="Programming Language",
            level="Intermediate"
        )
        db.session.add(skill)
        db.session.commit()
        
        assert skill.id is not None
        assert skill.name == "Python"
        
        # Test relationship
        job.skills.append(skill)
        db.session.commit()
        
        assert len(job.skills) == 1
        assert job.skills[0].name == "Python"

def test_skills_endpoint(client):
    """Test the skills endpoint."""
    response = client.get('/api/skills')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert 'skills' in data
    assert 'count' in data

def test_job_postings_endpoint(client):
    """Test the job postings endpoint."""
    response = client.get('/api/job-postings')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert 'job_postings' in data
    assert 'count' in data

def test_history_endpoint(client):
    """Test the history endpoint."""
    response = client.get('/api/history')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert 'history' in data
    assert 'count' in data

def test_analyze_job_missing_description(client):
    """Test job analysis with missing required field."""
    response = client.post('/api/analyze-job', json={})
    assert response.status_code == 400
    
    data = response.get_json()
    assert 'error' in data
    assert 'description' in data['error']

def test_generate_questions_missing_job_id(client):
    """Test question generation with missing required field."""
    response = client.post('/api/generate-questions', json={})
    assert response.status_code == 400
    
    data = response.get_json()
    assert 'error' in data
    assert 'job_posting_id' in data['error']

def test_generate_exercises_missing_job_id(client):
    """Test exercise generation with missing required field."""
    response = client.post('/api/generate-exercises', json={})
    assert response.status_code == 400
    
    data = response.get_json()
    assert 'error' in data
    assert 'job_posting_id' in data['error']

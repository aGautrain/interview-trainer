"""
API routes for the Interview Trainer application.
Handles HTTP requests and responses for all core functionality.
"""

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
import logging

# Import models and services
from .models import db, JobPosting, Skill, Question, CodingExercise, UserSession
from .services.job_analyzer import JobAnalyzer
from .services.llm_service import LLMService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create API blueprint
api_bp = Blueprint('api', __name__)

# Initialize services
job_analyzer = JobAnalyzer()
llm_service = LLMService()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running."""
    return jsonify({
        'status': 'healthy',
        'message': 'Interview Trainer API is running',
        'version': '1.0.0'
    })

@api_bp.route('/analyze-job', methods=['POST'])
def analyze_job():
    """
    Analyze a job posting and extract relevant skills.
    
    Expected JSON payload:
    {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "description": "Job description text...",
        "requirements": "Job requirements text...",
        "location": "Remote"
    }
    
    Returns:
        JSON with extracted skills and job analysis
    """
    try:
        # Validate request data
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({
                'error': 'Missing required field: description'
            }), 400
        
        # Extract job information
        title = data.get('title', 'Unknown Position')
        company = data.get('company')
        description = data['description']
        requirements = data.get('requirements', '')
        location = data.get('location')
        
        # Create job posting in database
        job_posting = JobPosting(
            title=title,
            company=company,
            description=description,
            requirements=requirements,
            location=location
        )
        
        # Analyze job and extract skills using LLM
        skills_data = job_analyzer.extract_skills(description, requirements)
        
        # Create or get existing skills
        skills = []
        for skill_data in skills_data:
            skill = Skill.query.filter_by(name=skill_data['name']).first()
            if not skill:
                skill = Skill(
                    name=skill_data['name'],
                    category=skill_data.get('category'),
                    level=skill_data.get('level'),
                    description=skill_data.get('description')
                )
                db.session.add(skill)
            
            skills.append(skill)
        
        # Associate skills with job posting
        job_posting.skills = skills
        
        # Save to database
        db.session.add(job_posting)
        db.session.commit()
        
        # Return analysis results
        return jsonify({
            'success': True,
            'job_posting': job_posting.to_dict(),
            'extracted_skills': [skill.to_dict() for skill in skills],
            'message': f'Successfully analyzed job posting and extracted {len(skills)} skills'
        }), 201
        
    except Exception as e:
        logger.error(f"Error analyzing job: {str(e)}")
        db.session.rollback()
        return jsonify({
            'error': 'Failed to analyze job posting',
            'message': str(e)
        }), 500

@api_bp.route('/generate-questions', methods=['POST'])
def generate_questions():
    """
    Generate interview questions based on skills and parameters.
    
    Expected JSON payload:
    {
        "job_posting_id": 1,
        "question_type": "technical",
        "difficulty": "intermediate",
        "count": 5
    }
    
    Returns:
        JSON with generated questions
    """
    try:
        # Validate request data
        data = request.get_json()
        if not data or 'job_posting_id' not in data:
            return jsonify({
                'error': 'Missing required field: job_posting_id'
            }), 400
        
        job_posting_id = data['job_posting_id']
        question_type = data.get('question_type', 'technical')
        difficulty = data.get('difficulty', 'intermediate')
        count = data.get('count', 5)
        
        # Get job posting and skills
        job_posting = JobPosting.query.get(job_posting_id)
        if not job_posting:
            return jsonify({
                'error': 'Job posting not found'
            }), 404
        
        skills = [skill.name for skill in job_posting.skills]
        
        # Generate questions using LLM
        questions_data = llm_service.generate_questions(
            skills=skills,
            question_type=question_type,
            difficulty=difficulty,
            count=count
        )
        
        # Create question objects
        questions = []
        for q_data in questions_data:
            question = Question(
                text=q_data['text'],
                question_type=question_type,
                difficulty=difficulty,
                category=q_data.get('category'),
                answer_hints=q_data.get('hints'),
                job_posting_id=job_posting_id
            )
            questions.append(question)
        
        # Save questions to database
        db.session.add_all(questions)
        db.session.commit()
        
        # Return generated questions
        return jsonify({
            'success': True,
            'questions': [q.to_dict() for q in questions],
            'message': f'Successfully generated {len(questions)} {difficulty} {question_type} questions'
        }), 201
        
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}")
        db.session.rollback()
        return jsonify({
            'error': 'Failed to generate questions',
            'message': str(e)
        }), 500

@api_bp.route('/generate-exercises', methods=['POST'])
def generate_exercises():
    """
    Generate coding exercises based on skills and parameters.
    
    Expected JSON payload:
    {
        "job_posting_id": 1,
        "programming_language": "Python",
        "difficulty": "intermediate",
        "count": 3
    }
    
    Returns:
        JSON with generated coding exercises
    """
    try:
        # Validate request data
        data = request.get_json()
        if not data or 'job_posting_id' not in data:
            return jsonify({
                'error': 'Missing required field: job_posting_id'
            }), 400
        
        job_posting_id = data['job_posting_id']
        programming_language = data.get('programming_language', 'Python')
        difficulty = data.get('difficulty', 'intermediate')
        count = data.get('count', 3)
        
        # Get job posting and skills
        job_posting = JobPosting.query.get(job_posting_id)
        if not job_posting:
            return jsonify({
                'error': 'Job posting not found'
            }), 404
        
        skills = [skill.name for skill in job_posting.skills]
        
        # Generate exercises using LLM
        exercises_data = llm_service.generate_exercises(
            skills=skills,
            programming_language=programming_language,
            difficulty=difficulty,
            count=count
        )
        
        # Create exercise objects
        exercises = []
        for ex_data in exercises_data:
            exercise = CodingExercise(
                title=ex_data['title'],
                description=ex_data['description'],
                programming_language=programming_language,
                difficulty=difficulty,
                category=ex_data.get('category'),
                solution=ex_data.get('solution'),
                test_cases=ex_data.get('test_cases'),
                time_limit=ex_data.get('time_limit'),
                job_posting_id=job_posting_id
            )
            exercises.append(exercise)
        
        # Save exercises to database
        db.session.add_all(exercises)
        db.session.commit()
        
        # Return generated exercises
        return jsonify({
            'success': True,
            'exercises': [ex.to_dict() for ex in exercises],
            'message': f'Successfully generated {len(exercises)} {difficulty} {programming_language} exercises'
        }), 201
        
    except Exception as e:
        logger.error(f"Error generating exercises: {str(e)}")
        db.session.rollback()
        return jsonify({
            'error': 'Failed to generate exercises',
            'message': str(e)
        }), 500

@api_bp.route('/skills', methods=['GET'])
def get_skills():
    """Get all available skills in the system."""
    try:
        skills = Skill.query.all()
        return jsonify({
            'success': True,
            'skills': [skill.to_dict() for skill in skills],
            'count': len(skills)
        })
    except Exception as e:
        logger.error(f"Error fetching skills: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch skills',
            'message': str(e)
        }), 500

@api_bp.route('/job-postings', methods=['GET'])
def get_job_postings():
    """Get all job postings in the system."""
    try:
        job_postings = JobPosting.query.order_by(JobPosting.created_at.desc()).all()
        return jsonify({
            'success': True,
            'job_postings': [job.to_dict() for job in job_postings],
            'count': len(job_postings)
        })
    except Exception as e:
        logger.error(f"Error fetching job postings: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch job postings',
            'message': str(e)
        }), 500

@api_bp.route('/job-postings/<int:job_id>', methods=['GET'])
def get_job_posting(job_id):
    """Get a specific job posting by ID."""
    try:
        job_posting = JobPosting.query.get(job_id)
        if not job_posting:
            return jsonify({
                'error': 'Job posting not found'
            }), 404
        
        return jsonify({
            'success': True,
            'job_posting': job_posting.to_dict()
        })
    except Exception as e:
        logger.error(f"Error fetching job posting {job_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch job posting',
            'message': str(e)
        }), 500

@api_bp.route('/history', methods=['GET'])
def get_history():
    """Get generation history for all job postings."""
    try:
        job_postings = JobPosting.query.order_by(JobPosting.created_at.desc()).limit(10).all()
        
        history = []
        for job in job_postings:
            history.append({
                'job_posting': job.to_dict(),
                'questions': [q.to_dict() for q in job.questions],
                'exercises': [ex.to_dict() for ex in job.exercises]
            })
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch history',
            'message': str(e)
        }), 500

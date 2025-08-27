"""
Flask application factory for the Interview Trainer application.
This module creates and configures the Flask app with all necessary extensions.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# Import configuration
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name (str): Configuration environment name
        
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = config['default']
    else:
        config_name = config.get(config_name, config['default'])
    
    app.config.from_object(config_name)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Debug toolbar removed due to compatibility issues
    
    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    return app

def register_error_handlers(app):
    """Register custom error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors."""
        return {'error': 'Bad Request', 'message': str(error)}, 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors."""
        return {'error': 'Not Found', 'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors."""
        return {'error': 'Internal Server Error', 'message': 'Something went wrong'}, 500

def register_cli_commands(app):
    """Register custom CLI commands for the application."""
    
    @app.cli.command('init-db')
    def init_db():
        """Initialize the database with sample data."""
        from .models import JobPosting, Skill, Question, CodingExercise
        from .utils.seed_data import seed_database
        
        print("Creating database tables...")
        db.create_all()
        
        print("Seeding database with sample data...")
        seed_database()
        
        print("Database initialization complete!")
    
    @app.cli.command('test')
    def test():
        """Run the test suite."""
        import pytest
        import sys
        
        print("Running tests...")
        exit_code = pytest.main(['tests/', '-v', '--cov=app'])
        sys.exit(exit_code)

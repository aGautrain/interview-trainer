"""
Configuration settings for the Interview Trainer application.
Supports different environments: development, testing, and production.
"""

import os
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).parent

class Config:
    """Base configuration class with common settings."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{BASE_DIR}/interview_trainer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # LLM API settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']  # React dev servers
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_STORAGE_URL = "memory://"

class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    SQLALCHEMY_ECHO = True  # Log all SQL queries
    
    # Enable Flask-DebugToolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class TestingConfig(Config):
    """Testing environment configuration."""
    
    DEBUG = False
    TESTING = True
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF protection in tests
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Production security settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Disable SQL query logging
    SQLALCHEMY_ECHO = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment variable."""
    # Flask 3.x uses FLASK_DEBUG instead of FLASK_ENV
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    env = 'development' if debug else 'production'
    return config.get(env, config['default'])


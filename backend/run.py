"""
Main entry point for the Interview Trainer Flask application.
Runs the development server and handles application startup.
"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function to run the Flask application."""
    
    # Create Flask application instance
    app = create_app()
    
    # Get configuration
    debug = app.config.get('DEBUG', False)
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print("=" * 60)
    print("🚀 Interview Trainer API Starting...")
    print("=" * 60)
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug Mode: {'ON' if debug else 'OFF'}")
    print(f"🗄️  Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')}")
    print(f"🤖 LLM Model: {os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')}")
    print("=" * 60)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: No OpenAI API key found!")
        print("   The application will use fallback responses.")
        print("   Set OPENAI_API_KEY environment variable for full functionality.")
        print("=" * 60)
    
    # Run the application
    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug
        )
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        raise

if __name__ == '__main__':
    main()

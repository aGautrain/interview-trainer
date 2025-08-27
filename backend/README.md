# Interview Trainer - Backend API

This is the Flask backend for the Interview Trainer application, providing a RESTful API for job analysis, question generation, and coding exercise creation.

## 🚀 Features

- **Job Analysis**: Extract skills from job descriptions using LLM
- **Question Generation**: Create custom interview questions based on skills
- **Exercise Creation**: Generate coding challenges with solutions
- **Skill Management**: Organize and categorize technical skills
- **History Tracking**: Keep track of all generated content

## 🛠️ Tech Stack

- **Framework**: Flask 3.1.2
- **Database**: SQLAlchemy + SQLite
- **LLM Integration**: OpenAI API
- **Testing**: pytest with coverage
- **Development**: Docker, Docker Compose, Flask-Migrate
- **Containerization**: Python 3.12 slim image

## 📋 Prerequisites

- **Docker Desktop** installed and running
- **Docker Compose** (usually included with Docker Desktop)
- OpenAI API key (optional, fallback responses available)
- **Alternative**: Python 3.8+ with pip (for local development)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Navigate to backend directory
cd backend

# Build and start the service
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
```

The API will be available at `http://localhost:5000`

### Option 2: Local Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env

# Edit .env file with your settings
# At minimum, set your OpenAI API key for full functionality

# Start the development server
python run.py
```

The API will be available at `http://127.0.0.1:5000`

## 🐳 Docker Management

### Using Docker Compose (Recommended)

```bash
# Build image
docker-compose build

# Start service
docker-compose up -d

# Run tests
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# View logs
docker-compose logs -f backend

# Stop service
docker-compose down

# Clean up
docker-compose down -v --rmi all
```

### Using PowerShell Script (Windows)

```powershell
# Build image
.\run-docker.ps1 build

# Start service
.\run-docker.ps1 run

# Run tests
.\run-docker.ps1 test

# Check health
.\run-docker.ps1 health

# View logs
.\run-docker.ps1 logs

# Stop service
.\run-docker.ps1 stop
```

### Using Make (Linux/Mac)

```bash
# Build image
make build

# Start service
make run

# Run tests
make test

# Check health
make health

# View logs
make logs

# Stop service
make stop
```

## 🔧 Configuration

### Environment Variables

| Variable         | Description                | Default                   |
| ---------------- | -------------------------- | ------------------------- |
| `FLASK_ENV`      | Flask environment          | `development`             |
| `FLASK_DEBUG`    | Enable debug mode          | `True`                    |
| `OPENAI_API_KEY` | OpenAI API key             | Required for LLM features |
| `OPENAI_MODEL`   | OpenAI model to use        | `gpt-3.5-turbo`           |
| `DATABASE_URL`   | Database connection string | SQLite file               |

### Database

The application uses SQLite by default for development. The database file will be created automatically at `interview_trainer.db`.

## 📚 API Endpoints

### Health Check

- `GET /api/health` - API status and version

### Job Analysis

- `POST /api/analyze-job` - Analyze job posting and extract skills
- `GET /api/job-postings` - List all job postings
- `GET /api/job-postings/<id>` - Get specific job posting

### Content Generation

- `POST /api/generate-questions` - Generate interview questions
- `POST /api/generate-exercises` - Generate coding exercises

### Data Retrieval

- `GET /api/skills` - List all available skills
- `GET /api/history` - Get generation history

## 🧪 Testing

### Run Tests with Docker (Recommended)

```bash
# Run all tests in Docker
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Or using the management scripts
.\run-docker.ps1 test  # Windows
make test               # Linux/Mac
```

### Run Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_basic.py -v
```

### Test Coverage

The test suite aims for:

- **Routes**: 100% coverage
- **Services**: 95% coverage
- **Models**: 90% coverage
- **Overall**: 90%+ coverage

## 🗄️ Database Models

### Core Entities

- **JobPosting**: Job descriptions and requirements
- **Skill**: Technical and soft skills
- **Question**: Generated interview questions
- **CodingExercise**: Programming challenges
- **UserSession**: User preferences and API keys

### Relationships

- Job postings have many skills (many-to-many)
- Job postings have many questions (one-to-many)
- Job postings have many exercises (one-to-many)

## 🐳 Docker Features

### Benefits of Dockerization

- **Consistent Environment**: Same setup across all development machines
- **Easy Setup**: No need to install Python or manage virtual environments
- **Isolation**: Dependencies are contained within the container
- **Cross-Platform**: Works identically on Windows, macOS, and Linux
- **Production Ready**: Easy to deploy to any Docker-compatible environment

### Container Details

- **Base Image**: Python 3.11 slim (optimized for size)
- **Security**: Non-root user execution
- **Health Checks**: Automatic health monitoring
- **Volume Mounting**: Live code reloading during development
- **Network Isolation**: Dedicated network for services

### Environment Support

- **Development**: Hot reloading, debug mode, detailed logging
- **Testing**: Isolated test environment with in-memory database
- **Production**: Optimized for performance and security

## 🔌 LLM Integration

### OpenAI API

The application integrates with OpenAI's API for:

- Skill extraction from job descriptions
- Question generation based on skills
- Coding exercise creation
- Job complexity analysis

### Fallback Responses

When the API is unavailable or fails, the system provides:

- Pre-defined skill sets
- Sample interview questions
- Basic coding exercises
- Default complexity assessments

## 🚀 Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes.py            # API endpoints
│   └── services/
│       ├── __init__.py
│       ├── llm_service.py   # OpenAI integration
│       └── job_analyzer.py  # Job analysis logic
├── tests/                   # Test suite
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── run.py                 # Application entry point
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Development environment
├── docker-compose.test.yml # Testing environment
├── .dockerignore          # Docker build exclusions
├── Makefile               # Development commands (Linux/Mac)
├── run-docker.ps1        # Docker management script (Windows)
├── DOCKER_README.md       # Comprehensive Docker guide
└── TESTING_SUMMARY.md     # Testing results and setup
```

### Adding New Features

1. **Models**: Add new database models in `app/models.py`
2. **Services**: Create business logic in `app/services/`
3. **Routes**: Add API endpoints in `app/routes.py`
4. **Tests**: Write tests in `tests/` directory

### Code Quality

- Use type hints for all function parameters
- Write comprehensive docstrings
- Follow PEP 8 style guidelines
- Maintain test coverage above 90%

## 🐛 Troubleshooting

### Docker Issues

1. **Container won't start**: Check if port 5000 is available
2. **Build failures**: Ensure Docker Desktop is running
3. **Permission errors**: Run `docker-compose down -v --rmi all` and rebuild
4. **Network issues**: Check Docker network configuration

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated (local development)
2. **Database Errors**: Check database file permissions
3. **API Failures**: Verify OpenAI API key and internet connection
4. **CORS Issues**: Check CORS configuration in config.py

### Debug Mode

Enable debug mode for detailed error messages:

```bash
export FLASK_DEBUG=True
python run.py
```

## 📝 API Examples

### Analyze Job Posting

```bash
curl -X POST http://localhost:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "description": "We are looking for a Python developer...",
    "location": "Remote"
  }'
```

### Generate Questions

```bash
curl -X POST http://localhost:5000/api/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "job_posting_id": 1,
    "question_type": "technical",
    "difficulty": "intermediate",
    "count": 5
  }'
```

## 📋 Available Commands

### Docker Management Commands

| Command   | Description        | Windows                    | Linux/Mac      |
| --------- | ------------------ | -------------------------- | -------------- |
| `build`   | Build Docker image | `.\run-docker.ps1 build`   | `make build`   |
| `run`     | Start service      | `.\run-docker.ps1 run`     | `make run`     |
| `run-dev` | Start with logs    | `.\run-docker.ps1 run-dev` | `make run-dev` |
| `test`    | Run tests          | `.\run-docker.ps1 test`    | `make test`    |
| `logs`    | View logs          | `.\run-docker.ps1 logs`    | `make logs`    |
| `stop`    | Stop service       | `.\run-docker.ps1 stop`    | `make stop`    |
| `health`  | Check health       | `.\run-docker.ps1 health`  | `make health`  |
| `clean`   | Clean up           | `.\run-docker.ps1 clean`   | `make clean`   |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. **Ensure all tests pass** (use Docker: `.\run-docker.ps1 test`)
6. Submit a pull request

### Development Workflow

```bash
# 1. Start development environment
docker-compose up -d

# 2. Make code changes (files are mounted as volumes)

# 3. Run tests
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# 4. Check API health
curl http://localhost:5000/api/health

# 5. Stop when done
docker-compose down
```

## 📄 License

This project is part of the Interview Trainer application.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the API documentation
3. Check test coverage for examples
4. Open an issue in the repository

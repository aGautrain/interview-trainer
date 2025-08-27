# Interview Trainer Backend - Docker Setup

This document explains how to run the Interview Trainer backend using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (usually included with Docker Desktop)

## Quick Start

### 1. Build the Docker Image

```bash
# Using PowerShell script (Windows)
.\run-docker.ps1 build

# Using Make (Linux/Mac)
make build

# Using Docker Compose directly
docker-compose build
```

### 2. Start the Backend Service

```bash
# Start in background
.\run-docker.ps1 run

# Start with logs (development mode)
.\run-docker.ps1 run-dev
```

### 3. Check Service Status

```bash
.\run-docker.ps1 status
```

### 4. Test the API

```bash
# Health check
.\run-docker.ps1 health

# Or manually test endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/skills
curl http://localhost:5000/api/job-postings
```

## Available Commands

| Command   | Description                 |
| --------- | --------------------------- |
| `build`   | Build the Docker image      |
| `run`     | Start service in background |
| `run-dev` | Start service with logs     |
| `stop`    | Stop the service            |
| `test`    | Run tests in Docker         |
| `logs`    | Show service logs           |
| `shell`   | Open shell in container     |
| `restart` | Restart the service         |
| `status`  | Show service status         |
| `health`  | Test API health             |
| `clean`   | Clean up Docker resources   |

## Running Tests

```bash
# Run tests in Docker (recommended)
.\run-docker.ps1 test

# Run tests locally (requires Python setup)
.\run-docker.ps1 test-local
```

## Development Workflow

1. **Start development server:**

   ```bash
   .\run-docker.ps1 run-dev
   ```

2. **View logs:**

   ```bash
   .\run-docker.ps1 logs
   ```

3. **Make code changes** (files are mounted as volumes)

4. **Restart service if needed:**
   ```bash
   .\run-docker.ps1 restart
   ```

## Environment Variables

The following environment variables can be customized in `docker-compose.yml`:

- `FLASK_ENV`: Environment (development/testing/production)
- `FLASK_DEBUG`: Debug mode (True/False)
- `FLASK_HOST`: Host binding (0.0.0.0 for Docker)
- `FLASK_PORT`: Port (5000)
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string
- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_MODEL`: OpenAI model to use
- `CORS_ORIGINS`: Allowed CORS origins

## Troubleshooting

### Service won't start

```bash
# Check logs
.\run-docker.ps1 logs

# Check status
.\run-docker.ps1 status

# Restart service
.\run-docker.ps1 restart
```

### Port already in use

```bash
# Stop all services
.\run-docker.ps1 stop

# Clean up
.\run-docker.ps1 clean

# Rebuild and start
.\run-docker.ps1 build
.\run-docker.ps1 run
```

### Permission issues

```bash
# Clean up and rebuild
.\run-docker.ps1 clean
.\run-docker.ps1 build
```

## Cleanup

```bash
# Stop and remove containers
.\run-docker.ps1 stop

# Clean up images and volumes
.\run-docker.ps1 clean
```

## API Endpoints

Once running, the following endpoints are available:

- `GET /api/health` - Health check
- `GET /api/skills` - List available skills
- `GET /api/job-postings` - List job postings
- `GET /api/history` - Training history
- `POST /api/analyze-job` - Analyze job posting
- `POST /api/generate-questions` - Generate interview questions
- `POST /api/generate-exercises` - Generate coding exercises

## Database

The application uses SQLite by default, stored in a Docker volume. The database file is created automatically when the service starts.

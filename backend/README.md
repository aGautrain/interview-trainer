# FastAPI Backend

This is a FastAPI backend service that can be easily deployed using Docker Compose.

## Quick Start with Docker Compose

### Prerequisites

- Docker
- Docker Compose

### Running the Service

1. **Start the service:**

   ```bash
   docker-compose up
   ```

2. **Start in background:**

   ```bash
   docker-compose up -d
   ```

3. **Stop the service:**

   ```bash
   docker-compose down
   ```

4. **Rebuild and start:**
   ```bash
   docker-compose up --build
   ```

### Accessing the API

Once running, the API will be available at:

- **API Base URL:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **ReDoc Documentation:** http://localhost:8000/redoc

### Available Endpoints

#### Core Endpoints

- `GET /` - Returns a hello world message

#### Dashboard Endpoints

- `GET /dashboard` - Returns complete dashboard data
- `GET /dashboard/stats` - Returns dashboard statistics

#### Job Endpoints

- `GET /jobs` - Returns all available jobs
- `GET /jobs/{job_id}` - Returns a specific job by ID

#### Skills & Training Endpoints

- `GET /skills` - Returns all available skills
- `GET /skills/{skill_name}/questions` - Returns questions for a specific skill
- `GET /skills/{skill_name}/exercises` - Returns exercises for a specific skill

#### Legacy Endpoints (Backward Compatibility)

- `GET /items/{item_id}` - Returns item information
- `PUT /items/{item_id}` - Updates item information

### Development

The backend code is mounted as a volume, so changes to your Python files will automatically reload the service.

### Health Check

The service includes a health check that verifies the API is responding correctly every 30 seconds.

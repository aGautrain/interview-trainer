# Job Analysis Service

The Job Analysis Service is a comprehensive business logic layer that orchestrates job description analysis using the LLM abstraction layer and integrates with the existing database structure.

## Overview

This service provides intelligent job analysis capabilities including:

- **Complete Job Analysis**: Analyze job descriptions to extract skills, requirements, and generate recommendations
- **Skill Extraction**: Extract and categorize skills from any text content
- **Database Integration**: Match extracted skills with existing database entries
- **Caching Layer**: Optimize performance and costs with intelligent caching
- **Training Recommendations**: Generate personalized training paths based on skill gaps
- **Bulk Processing**: Analyze multiple job descriptions in parallel
- **Metrics & Analytics**: Track usage patterns and performance statistics

## Architecture

### Core Components

1. **JobAnalysisService**: Main orchestration class
2. **Schema Models**: Pydantic models for request/response validation
3. **Database Layer**: PostgreSQL integration with caching tables
4. **LLM Integration**: Uses the existing LLM abstraction layer
5. **API Endpoints**: FastAPI routes for REST API access

### Database Schema

The service uses several PostgreSQL tables:

- `job_analysis_cache`: Caches LLM analysis results
- `job_analysis_history`: Tracks analysis operations for metrics
- `job_analysis_cache_skills`: Individual skill extraction tracking
- `user_skills`: User skill proficiency levels for gap analysis
- `training_recommendations`: Generated training recommendations
- `bulk_job_analyses`: Bulk operation tracking

### Setup Database Tables

Run the setup script to create all necessary tables:

```bash
cd database
python setup_job_analysis.py
```

## API Endpoints

### Core Analysis Endpoints

#### `POST /job-analysis/analyze`
Analyze a single job description with comprehensive results.

**Request:**
```json
{
  "job_description": "Senior Python Developer role...",
  "job_title": "Senior Python Developer",
  "company_name": "TechCorp",
  "analysis_depth": "standard",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "success": true,
  "status": "completed",
  "result": {
    "industry": "Technology",
    "experience_level": "senior",
    "extracted_skills": [...],
    "training_recommendations": [...],
    "readiness_score": 0.75
  },
  "processing_time_ms": 1250.5,
  "cache_hit": false
}
```

#### `POST /job-analysis/extract-skills`
Extract skills from any text content.

**Parameters:**
- `text`: Text content to analyze
- `context_type`: Type of content (job_description, resume, etc.)

#### `POST /job-analysis/analyze-bulk`
Analyze multiple job descriptions in parallel.

**Request:**
```json
{
  "job_descriptions": ["Job 1 text...", "Job 2 text..."],
  "analysis_depth": "standard",
  "user_id": "user123"
}
```

### Utility Endpoints

#### `GET /job-analysis/metrics`
Get service metrics and statistics.

#### `GET /job-analysis/health`
Health check for service and dependencies.

#### `GET /job-analysis/cache/stats`
Cache performance statistics.

#### `DELETE /job-analysis/cache/clear`
Clear expired or all cache entries.

## Usage Examples

### Basic Job Analysis

```python
from services.job_analysis import get_job_analysis_service
from schemas.job_analysis import JobAnalysisRequest

# Get service instance
service = await get_job_analysis_service()

# Create analysis request
request = JobAnalysisRequest(
    job_description="Python developer needed with Django experience...",
    job_title="Python Developer",
    analysis_depth="standard"
)

# Perform analysis
response = await service.analyze_job_description(request)

if response.success:
    result = response.result
    print(f"Found {len(result.extracted_skills)} skills")
    print(f"Training recommendations: {len(result.training_recommendations)}")
```

### Skill Extraction

```python
# Extract skills from any text
skills = await service.extract_skills_from_text(
    "Experience with React, TypeScript, and Node.js required",
    context_type="job_requirements"
)

for skill in skills:
    print(f"{skill.name} ({skill.confidence_score:.2f})")
```

### Bulk Analysis

```python
from schemas.job_analysis import BulkJobAnalysisRequest

# Analyze multiple jobs
bulk_request = BulkJobAnalysisRequest(
    job_descriptions=[
        "Python developer job...",
        "React developer role...",
        "DevOps engineer position..."
    ]
)

bulk_response = await service.bulk_analyze_jobs(bulk_request)
print(f"Processed {bulk_response.successful_analyses} jobs successfully")
```

## Configuration

### LLM Provider Setup

The service automatically uses the configured LLM provider from the LLM abstraction layer. Ensure you have at least one provider configured (OpenAI, Anthropic, or Mock for development).

### Environment Variables

```env
# Database connection (already configured in main app)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=interview_trainer
DB_USER=interview_user
DB_PASSWORD=interview_password

# LLM provider configuration (see LLM service docs)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### Cache Configuration

The service includes intelligent caching with configurable settings:

- **Cache Expiry**: 24 hours by default
- **Retry Logic**: 3 attempts with exponential backoff
- **Concurrent Processing**: Limited to 5 parallel analyses for bulk operations

## Performance Considerations

### Caching Strategy

1. **Job Description Hashing**: Uses SHA-256 hash of job description as cache key
2. **Automatic Expiration**: Cache entries expire after 24 hours
3. **Hit Tracking**: Monitors cache usage for analytics
4. **Cleanup**: Automatic cleanup of expired entries

### Cost Optimization

1. **Intelligent Caching**: Reduces LLM API calls by up to 80%
2. **Bulk Processing**: Optimizes token usage for multiple analyses
3. **Retry Logic**: Handles rate limits gracefully
4. **Token Tracking**: Monitors usage for cost analysis

### Scalability

1. **Database Connection Pooling**: Uses asyncpg pool for efficient DB access
2. **Async Processing**: Fully async implementation for high concurrency
3. **Parallel Processing**: Bulk operations processed in parallel with limits
4. **Resource Management**: Configurable concurrency limits

## Error Handling

### Common Error Scenarios

1. **LLM Provider Unavailable**: Graceful fallback and retry logic
2. **Rate Limiting**: Exponential backoff with configurable limits
3. **Database Errors**: Graceful degradation with error logging
4. **Invalid Input**: Comprehensive validation with helpful error messages

### Monitoring & Logging

1. **Structured Logging**: Comprehensive logging for debugging
2. **Metrics Tracking**: Built-in analytics and performance metrics
3. **Health Checks**: Service health monitoring endpoints
4. **Error Tracking**: Detailed error reporting and categorization

## Development & Testing

### Running Tests

```bash
# Run the test script
cd backend
python test_job_analysis.py
```

### Development Mode

Use the Mock LLM provider for development without external API costs:

```python
from services.llm import MockProvider

# Mock provider provides realistic test data
# without external API calls
```

### Database Setup

```bash
# Create database tables
cd database
python setup_job_analysis.py

# Populate with sample data
python populate_sample_data.py
```

## Integration Points

### Frontend Integration

The service provides REST endpoints that can be integrated with the existing React frontend:

```typescript
// Example frontend integration
const analyzeJob = async (jobDescription: string) => {
  const response = await fetch('/job-analysis/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      job_description: jobDescription,
      analysis_depth: 'standard'
    })
  });
  
  return response.json();
};
```

### Dashboard Integration

Service metrics can be integrated into the existing dashboard:

```python
# Get analysis metrics for dashboard
metrics = await service.get_analysis_metrics()

dashboard_data = {
    'total_analyses': metrics.total_analyses,
    'success_rate': metrics.successful_analyses / metrics.total_analyses,
    'avg_processing_time': metrics.avg_processing_time_ms
}
```

## Future Enhancements

### Planned Features

1. **Advanced Skill Matching**: Semantic similarity using embeddings
2. **Learning Path Generation**: Multi-step training curricula
3. **Company-Specific Analysis**: Tailored analysis based on company context
4. **Resume Matching**: Match user resumes against job requirements
5. **Real-time Analysis**: WebSocket support for live analysis updates

### Performance Improvements

1. **Embeddings Cache**: Pre-computed embeddings for skill matching
2. **Batch Processing**: Optimize LLM calls for bulk operations
3. **Background Processing**: Queue-based analysis for large batches
4. **Result Streaming**: Stream partial results for better UX

## Security Considerations

1. **Input Validation**: Comprehensive validation of all inputs
2. **Rate Limiting**: Protect against abuse with configurable limits
3. **Data Privacy**: User data handling in compliance with privacy requirements
4. **API Security**: Authentication and authorization for sensitive endpoints

## Troubleshooting

### Common Issues

1. **LLM Provider Not Available**: Check configuration and API keys
2. **Database Connection Errors**: Verify database configuration and connectivity
3. **Cache Performance Issues**: Monitor cache hit rates and cleanup expired entries
4. **High Token Usage**: Review analysis depth settings and caching effectiveness

### Debug Endpoints

Use the debug endpoints for troubleshooting:

- `GET /job-analysis/debug/llm-providers`: Check LLM provider status
- `GET /job-analysis/health`: Overall service health
- `GET /job-analysis/metrics`: Performance metrics

---

For more information, see the main project documentation and the LLM service documentation.
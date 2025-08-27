# Interview Trainer Backend - Docker Management Script
# Run this script from the backend directory

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Interview Trainer Backend - Available Commands:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  build     - Build the Docker image" -ForegroundColor Green
    Write-Host "  run       - Start the backend service in background" -ForegroundColor Green
    Write-Host "  run-dev   - Start the backend service with logs" -ForegroundColor Green
    Write-Host "  stop      - Stop the backend service" -ForegroundColor Green
    Write-Host "  test      - Run tests in Docker" -ForegroundColor Green
    Write-Host "  logs      - Show backend logs" -ForegroundColor Green
    Write-Host "  shell     - Open a shell in the running container" -ForegroundColor Green
    Write-Host "  restart   - Restart the backend service" -ForegroundColor Green
    Write-Host "  status    - Show status of services" -ForegroundColor Green
    Write-Host "  health    - Check backend health" -ForegroundColor Green
    Write-Host "  clean     - Clean up Docker containers and images" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\run-docker.ps1 [command]" -ForegroundColor Yellow
}

function Build-Image {
    Write-Host "Building Docker image..." -ForegroundColor Yellow
    docker-compose build
}

function Start-Service {
    Write-Host "Starting backend service..." -ForegroundColor Yellow
    docker-compose up -d
    Write-Host "Service started! Check status with: .\run-docker.ps1 status" -ForegroundColor Green
}

function Start-ServiceDev {
    Write-Host "Starting backend service in development mode..." -ForegroundColor Yellow
    docker-compose up
}

function Stop-Service {
    Write-Host "Stopping backend service..." -ForegroundColor Yellow
    docker-compose down
    Write-Host "Service stopped!" -ForegroundColor Green
}

function Run-Tests {
    Write-Host "Running tests in Docker..." -ForegroundColor Yellow
    docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
}

function Show-Logs {
    Write-Host "Showing backend logs..." -ForegroundColor Yellow
    docker-compose logs -f backend
}

function Open-Shell {
    Write-Host "Opening shell in container..." -ForegroundColor Yellow
    docker-compose exec backend /bin/bash
}

function Restart-Service {
    Write-Host "Restarting backend service..." -ForegroundColor Yellow
    docker-compose restart backend
    Write-Host "Service restarted!" -ForegroundColor Green
}

function Show-Status {
    Write-Host "Service status:" -ForegroundColor Yellow
    docker-compose ps
}

function Test-Health {
    Write-Host "Testing backend health..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -TimeoutSec 5
        Write-Host "✅ Backend is healthy: $($response.message)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Backend is not healthy or not running" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Clean-Docker {
    Write-Host "Cleaning up Docker containers and images..." -ForegroundColor Yellow
    docker-compose down -v --rmi all
    docker system prune -f
    Write-Host "Cleanup completed!" -ForegroundColor Green
}

# Main command execution
switch ($Command.ToLower()) {
    "build" { Build-Image }
    "run" { Start-Service }
    "run-dev" { Start-ServiceDev }
    "stop" { Stop-Service }
    "test" { Run-Tests }
    "logs" { Show-Logs }
    "shell" { Open-Shell }
    "restart" { Restart-Service }
    "status" { Show-Status }
    "health" { Test-Health }
    "clean" { Clean-Docker }
    default { Show-Help }
}

.PHONY: help build run test clean logs shell

help: ## Show this help message
	@echo "Interview Trainer Backend - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker image
	docker-compose build

run: ## Start the backend service
	docker-compose up -d

run-dev: ## Start the backend service in development mode with logs
	docker-compose up

stop: ## Stop the backend service
	docker-compose down

test: ## Run tests in Docker
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

test-local: ## Run tests locally (requires Python and dependencies)
	python -m pytest -v

clean: ## Clean up Docker containers, images, and volumes
	docker-compose down -v --rmi all
	docker system prune -f

logs: ## Show backend logs
	docker-compose logs -f backend

shell: ## Open a shell in the running backend container
	docker-compose exec backend /bin/bash

restart: ## Restart the backend service
	docker-compose restart backend

status: ## Show status of services
	docker-compose ps

health: ## Check backend health
	curl -f http://localhost:5000/api/health || echo "Backend is not healthy"

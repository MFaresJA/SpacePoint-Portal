# SpacePoint Portal API

FastAPI backend for the SpacePoint Portal (role-based platform: Admin, Instructor, Ambassador, Intern).

## Tech Stack
- FastAPI
- PostgreSQL
- Docker + Docker Compose

## Run with Docker (Recommended)
From the `backend/` folder:

```bash
docker compose up --build
```

## API will be available at:

Health: http://localhost:8000/health
DB Health: http://localhost:8000/api/v1/health/db
Docs (Swagger): http://localhost:8000/docs

## Environment Files
- .env.example → template
- .env.dev → local development (ignored by git)
- .env.prod.example → production template only

## Architecture Summary (Aligned with Architecture Pack v1)
- app/main.py → FastAPI app entrypoint
- app/api/ → routers (HTTP endpoints)
- app/services/ → business logic
- app/repositories/ → database access layer
- app/models/ → ORM models (ERD aligned)
- app/core/ → config, security, logging

## Common Issues
Docker command not found
Install Docker Desktop and ensure it is running.

# WSL needs updating (Windows)
Run PowerShell as Admin:
```bash 
wsl --update
```

## Port already in use (8000 or 5432)
Stop the conflicting service or change ports in docker-compose.yml.

## Stop containers backend/ path: 
From the 
```bash
docker compose down
```
# SpacePoint Portal API

FastAPI backend for the SpacePoint Portal (role-based platform: Admin, Instructor, Ambassador, Intern).

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (Migrations)
- JWT Authentication
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

## Authentication (JWT)

### Register

`POST /api/v1/auth/register`

### Login

`POST /api/v1/auth/login`

Returns:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Authorize in Swagger

- Login
- Copy access_token
- Click Authorize
- Paste:
    Bearer YOUR_TOKEN_HERE

## RBAC (Role-Based Access Control)

Supported roles:
- admin
- instructor
- ambassador
- intern

Role-protected endpoints:

- /api/v1/admin/*
- /api/v1/instructor/*
- /api/v1/ambassador/*
- /api/v1/intern/*

Behavior:

- 401 → Not authenticated
- 403 → Authenticated but missing required role

## Admin Capabilities (Week 3 Completed)

Admin can:
* Manage Roles
-   GET /api/v1/admin/users/{user_id}/roles
- POST /api/v1/admin/users/{user_id}/roles/{role_name}
- DELETE /api/v1/admin/users/{user_id}/roles/{role_name}

* Manage User Status
- PATCH /api/v1/admin/users/{user_id}/activate
- PATCH /api/v1/admin/users/{user_id}/deactivate
- PATCH /api/v1/admin/users/{user_id}/verify
- PATCH /api/v1/admin/users/{user_id}/suspend
- PATCH /api/v1/admin/users/{user_id}/unsuspend

* List & View Users
- GET /api/v1/admin/users
- GET /api/v1/admin/users/{user_id}
- Pagination parameters:
- skip → number of records to skip
- limit → number of records to return

* Example:
- /api/v1/admin/users?skip=0&limit=50

## Database & Migrations
- Alembic is used for migrations.

* To create migration:
```bash
alembic revision --autogenerate -m "message"
```
- To apply migration:
```bash
alembic upgrade head
```

Initial migration creates:
- users table
- roles table
- user_roles table

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

---

## 📌 API Reference (Quick Table)

### Public / Utility

| Method | Endpoint | Auth | Role | Description |
|-------:|----------|------|------|-------------|
| GET | `/health` | ❌ | - | API health check |
| GET | `/api/v1/health/db` | ❌ | - | Database health check |

---

### Authentication

| Method | Endpoint | Auth | Role | Description |
|-------:|----------|------|------|-------------|
| POST | `/api/v1/auth/register` | ❌ | - | Create new user + return JWT |
| POST | `/api/v1/auth/login` | ❌ | - | Login user + return JWT |
| GET | `/api/v1/auth/me` | ✅ | any | Get current logged-in user info |

---

### Admin (RBAC: admin)

| Method | Endpoint | Auth | Role | Description |
|-------:|----------|------|------|-------------|
| GET | `/api/v1/admin/ping` | ✅ | admin | Test admin access |
| GET | `/api/v1/admin/users` | ✅ | admin | List users (pagination: skip, limit) |
| GET | `/api/v1/admin/users/{user_id}` | ✅ | admin | Get one user by id |

**Role Management**
| Method | Endpoint | Auth | Role | Description |
|-------:|----------|------|------|-------------|
| GET | `/api/v1/admin/users/{user_id}/roles` | ✅ | admin | List roles for a user |
| POST | `/api/v1/admin/users/{user_id}/roles/{role_name}` | ✅ | admin | Assign role to user |
| DELETE | `/api/v1/admin/users/{user_id}/roles/{role_name}` | ✅ | admin | Remove role from user |

**User Status**
| Method | Endpoint | Auth | Role | Description |
|-------:|----------|------|------|-------------|
| PATCH | `/api/v1/admin/users/{user_id}/activate` | ✅ | admin | Activate user |
| PATCH | `/api/v1/admin/users/{user_id}/deactivate` | ✅ | admin | Deactivate user |
| PATCH | `/api/v1/admin/users/{user_id}/verify` | ✅ | admin | Verify user |
| PATCH | `/api/v1/admin/users/{user_id}/suspend` | ✅ | admin | Suspend user |
| PATCH | `/api/v1/admin/users/{user_id}/unsuspend` | ✅ | admin | Unsuspend user |

---

### Instructor (RBAC: instructor)

| Method | Endpoint | Auth | Role | Description |
|-------:|----------|------|------|-------------|
| GET | `/api/v1/instructor/ping` | ✅ | instructor | Test instructor access |

---

### Ambassador (RBAC: ambassador)

| Method | Endpoint | Auth | Role | Description |
|-------:|----------|------|------|-------------|
| GET | `/api/v1/ambassador/ping` | ✅ | ambassador | Test ambassador access |

---

### Intern (RBAC: intern)

| Method | Endpoint | Auth | Role | Description |
|-------:|----------|------|------|-------------|
| GET | `/api/v1/intern/ping` | ✅ | intern | Test intern access |

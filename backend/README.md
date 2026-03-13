# SpacePoint Portal

The **SpacePoint Portal** is a role-based digital platform designed to support the SpacePoint ecosystem by managing learning journeys, training workflows, collaboration activities, and engagement programs.

The system enables structured participation from multiple user roles including **Admins, Instructors, Ambassadors, and Interns**, each with dedicated workflows and permissions.

This repository contains the **backend implementation of the SpacePoint Portal**, built using **FastAPI**, **PostgreSQL**, and **Docker**, following a scalable layered architecture.

The backend exposes REST APIs responsible for managing:

- Authentication and authorization
- Role-based access control (RBAC)
- Instructor onboarding workflows
- Ambassador outreach and CRM activities
- Intern task submission workflows
- Administrative approvals
- Opportunity management
- Points and recognition systems
- Certificates and badges
- Platform analytics and moderation

---

# Project Repository

GitHub Repository:

https://github.com/MFaresJA/SpacePoint-Portal

---

# Platform Roles

The portal supports multiple roles representing different participants in the SpacePoint ecosystem.

## Admin

Admins manage the entire platform and supervise all workflows.

Admin capabilities include:

- User management
- Role assignment
- Submission approvals
- Platform analytics
- Opportunity management
- Recognition system management

---

## Instructor

Instructors participate in educational workflows and must complete qualification stages before contributing.

Instructor workflow includes:

- Submitting onboarding information
- Completing qualification quizzes
- Submitting scenario responses
- Logging onsite activities

### Instructor Onboarding

Instructors begin by submitting onboarding information which verifies their eligibility to continue the learning journey.

![Instructor Onboarding](images/Instructor Onboarding.png)

---

### Instructor Quiz Submission

After onboarding approval, instructors must complete qualification quizzes.

![Instructor Quiz Submission](images/Instructor Quiz Submission.png)

---

### Scenario Submission

Instructors complete scenario tasks used to evaluate practical knowledge.

![Instructor Scenario](images/Instructor Scenario Submission.png)

---

### Onsite Activity Logging

Instructors can log training activities performed during onsite sessions.

![Instructor Onsite Logs](images/Instructor Onsite Logs.png)

---

# Ambassador Workflow

Ambassadors support outreach and ecosystem growth.

Ambassador responsibilities include:

- Managing CRM leads
- Submitting proposals
- Supporting partnerships
- Participating in outreach activities

### CRM Lead Submission

Ambassadors submit potential collaboration leads through the CRM system.

![Ambassador Lead](images/Ambassador Submit Lead.png)

---

### Proposal Submission

Ambassadors submit proposals for review by administrators.

![Ambassador Proposal](images/Ambassador Submit Proposal.png)

---

# Intern Workflow

Interns participate in development tasks and training programs.

Intern activities include:

- Completing assigned tasks
- Submitting deliverables
- Tracking learning progress
- Participating in platform development

### Intern Submission

Interns upload project submissions for evaluation.

![Intern Submission](images/Intern Submission.png)

---

# Admin Management

Admins supervise and manage all platform activities.

### User Management

Admins can view and manage all platform users.

![Admin Users](images/Admin Users List.png)

---

### Role Assignment

Admins assign roles such as instructor, ambassador, or intern.

![Admin Assign Role](images/Admin Assign Role.png)

---

### Platform Overview

Admins have access to platform analytics through the overview dashboard.

![Admin Overview](images/Admin Overview Dashboard.png)

---

# Recognition System

The portal includes a recognition system to reward active participation.

### Points System

Users earn points based on participation and platform contributions.

![Points System](images/Points Ledger.png)

---

### Certificates

Certificates are issued when users complete major milestones.

![Certificates](images/Certificates Management.png)

---

### Badges

Badges reward achievements and contributions.

![Badges](images/Badges Management.png)

---

# Opportunities Management

Admins can publish opportunities available to the ecosystem.

![Opportunities](images/Opportunities Management.png)

---

# Technology Stack

The backend is implemented using the following technologies:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (database migrations)
- JWT Authentication
- Docker
- Docker Compose

---

# System Architecture

The system follows a layered modular architecture.

app/
├── api/ # HTTP endpoints
├── services/ # Business logic
├── repositories/ # Database access layer
├── models/ # ORM models
├── schemas/ # Pydantic schemas
├── core/ # configuration & security
└── utils/ # helper utilities

This architecture ensures separation of concerns, scalability, and maintainability.

---

# Running the Project

Run the backend using Docker.

From the `backend` folder:


docker compose up --build


---

# API Access

After starting the system:

Health check


http://localhost:8000/health


Database health


http://localhost:8000/api/v1/health/db


Swagger documentation


http://localhost:8000/docs


---

# Authentication

### Register


POST /api/v1/auth/register


### Login


POST /api/v1/auth/login


Returns:


{
"access_token": "...",
"token_type": "bearer"
}


Use the token in Swagger authorization:


Bearer YOUR_TOKEN


---

# Role-Based Access Control

Supported roles:

- admin
- instructor
- ambassador
- intern

Protected routes include:


/api/v1/admin/*
/api/v1/instructor/*
/api/v1/ambassador/*
/api/v1/intern/*


Error behavior:


401 → Not authenticated
403 → Missing required role


---

# Database & Migrations

Alembic is used for database migrations.

Create migration:


alembic revision --autogenerate -m "message"


Apply migration:


alembic upgrade head


---

# Environment Files

Environment configuration templates:


.env.example
.env.dev
.env.prod.example


---

# Author

**Mohammad Fares Aljamous**

Computer Engineering — Artificial Intelligence Concentration  
Abu Dhabi University

Internship Project — SpacePoint Portal Backend

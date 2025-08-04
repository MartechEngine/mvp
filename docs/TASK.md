# MartechEngine: Master Task List

This document is the single source of truth for all development tasks. Each task is based on a corresponding architectural document.

## How to Use This Document (SOP for AI Agent)
1.  Find the next task with a `[ ]` status.
2.  Read the referenced architectural document to understand the requirements.
3.  Implement the code to complete all sub-tasks.
4.  Commit your code with a conventional commit message.
5.  Update the task's checkbox from `[ ]` to `[x]`.
6.  Add a brief completion note under the "Progress Report" section for the task.

---

## Phase 1: Foundation & Core Infrastructure

### 1.1: Enterprise Project Skeleton & Development Tooling
-   **Objective:** Establish a production-ready, scalable monorepo project skeleton with modern development tooling.
-   **Reference:** `1.1-Project-Skeleton-and-Tooling.md`
-   **Sub-Tasks:**
    -   [x] Create comprehensive directory structure.
    -   [ ] Initialize Git repository. (Postponed until after Phase 2)
    -   [x] Create and populate `.gitignore`.
    -   [x] Configure `.editorconfig` and `.pre-commit-config.yaml`.
    -   [ ] Make the initial Git commit. (Postponed until after Phase 2)
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Completed project skeleton and tooling setup. Git initialization postponed.

### 1.2: Enterprise Environment Configuration
-   **Objective:** Establish a secure, scalable, and type-safe configuration management system.
-   **Reference:** `1.2-Environment-Configuration.md`
-   **Sub-Tasks:**
    -   [x] Implement Pydantic `Settings` schema.
    -   [x] Create `backend/.env.example`.
    -   [x] Create `frontend/.env.local.example`.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Created backend Pydantic settings and environment file templates for both backend and frontend.

### 1.3: Enterprise Security Architecture (GCP)
-   **Objective:** Define the security architecture for all environments.
-   **Reference:** `1.3-Production-Security-GCP.md`
-   **Sub-Tasks:**
    -   [x] Create the `scripts/gcp-setup-iam.sh` script for production IAM setup.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Created the production IAM setup script as specified in the architecture.

### 1.4: Enterprise Docker & Containerization Strategy
-   **Objective:** Create production-ready Docker images and a local development environment.
-   **Reference:** `1.4-Docker-Setup.md`
-   **Sub-Tasks:**
    -   [x] Create `backend/Dockerfile`.
    -   [x] Create `frontend/Dockerfile`.
    -   [x] Create root `.env.example` for Docker Compose.
    -   [x] Create `docker-compose.yml`.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Created production-ready Dockerfiles for backend and frontend, and the docker-compose setup for local development.

---

## Phase 2: User Identity & Authentication

### 2.1: Core Data Contracts
-   **Objective:** Establish the shared data structures for authentication between backend and frontend.
-   **Reference:** `2.1-Core-Data-Contracts.md`
-   **Sub-Tasks:**
    -   [x] Implement Pydantic schemas in `backend/app/schemas/`.
    -   [x] Create corresponding TypeScript types in `frontend/src/types/`.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Created all Pydantic schemas and TypeScript types for the API data contract.

### 2.2: Authentication Data Models
-   **Objective:** Define the core SQLAlchemy models for users, organizations, memberships, and sessions.
-   **Reference:** `2.2-Data-Models-Auth-and-Users.md`, `2.2.1-Data-Model-User-Session.md`
-   **Sub-Tasks:**
    -   [x] Implement `User`, `Organization`, `Membership`, and `UserSession` models.
    -   [x] Generate and apply the Alembic database migration.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** All data models implemented as per the architecture. Successfully generated and applied the initial database migration after extensive troubleshooting of the database connection, dependency conflicts, and environment configuration. The backend schema is now up-to-date.

### 2.3: Backend JWT Security Service
-   **Objective:** Implement a robust, secure, and isolated service for handling all JWT operations.
-   **Reference:** `2.3-Backend-Security-JWT-Service.md`
-   **Sub-Tasks:**
    -   [x] Implement the security module with password hashing and JWT functions.
    -   [x] Write comprehensive unit tests for the security module to ensure all functions work as expected, including edge cases.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** 
        - Implemented the core security module (`app/core/security.py`) with functions for password hashing and JWT creation/validation.
        - Fixed critical `AttributeError` in tests by refactoring `config.py` to use `pydantic.SecretStr` for all secrets.
        - Recovered from corrupted configuration files (`config.py`, `.env`) by implementing a robust overwrite strategy.
        - All backend unit tests are now passing, confirming the environment is stable and the security module is working correctly.

### 2.4: Backend Common Schemas

### 2.5: Backend Authentication Endpoints
-   **Objective:** Implement the API endpoints for user signup and login.
-   **Reference:** `docs/architecture/2.5-Backend-Auth-Endpoints.md`
-   **Sub-Tasks:**
    -   [x] Define Pydantic schemas for user creation (`UserCreate`) and user data (`UserRead`) in `user_schemas.py`.
    -   [x] Define Pydantic schemas for login requests (`LoginRequest`) and token responses (`Token`) in `auth_schemas.py`.
    -   [ ] Implement user creation and login logic in `AuthService`.
    -   [ ] Create `/signup` and `/login` endpoints in `api/v1/endpoints/auth.py`.
-   **Progress Report:**
    -   **Status:** In Progress
    -   **Notes:** 
        - **2025-08-04:** Created the necessary Pydantic schemas for user and authentication data models. The next step is to implement the service-layer logic after the IDE restart.
-   **Objective:** Define common Pydantic schemas for API responses and tenancy.
-   **Reference:** `2.4-Backend-Common-Schemas.md`
-   **Sub-Tasks:**
    -   [ ] Implement `ApiSuccessResponse` and `ApiErrorResponse`.
    -   [ ] Implement `TenantBase` and related tenancy schemas.
-   **Progress Report:**
    -   **Status:** Not Started
    -   **Notes:**

### 2.5: Backend Authentication Service
-   **Objective:** Create the core business logic for user registration and login.
-   **Reference:** `2.5-Backend-Auth-Service.md`
-   **Sub-Tasks:**
    -   [x] Implement the `AuthService` class.
    -   [x] Add logic for user registration, password hashing, and login.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Implemented the AuthService with register_user and authenticate_user methods as per the architecture. **Temporary Change for Testing:** Email verification is currently bypassed in `AuthService.register_user` by setting `is_verified=True`. This must be reverted before deployment.

### 2.6: Backend Authentication API
-   **Objective:** Expose the authentication services via secure FastAPI endpoints.
-   **Reference:** `2.6-Backend-Auth-and-User-API.md`
-   **Sub-Tasks:**
    -   [x] Implement `/auth/register`, `/auth/login`, and `/auth/refresh` endpoints.
    -   [x] Implement the `/users/me` endpoint with dependency injection for security.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Implemented the full authentication API, including exception handlers, database dependency, and router integration into the main app.

### 2.7: Frontend API Service Layer
-   **Objective:** Create a centralized, typed, and robust API client for the frontend.
-   **Reference:** `2.7-Frontend-API-Service-Layer.md`
-   **Sub-Tasks:**
    -   [x] Configure a global Axios instance (`apiClient`).
    -   [x] Implement request interceptors for adding auth tokens.
    -   [x] Implement response interceptors for transparent token refresh and global error handling.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Verified and corrected the centralized Axios client, ensuring token and error handling interceptors are implemented as per the architecture.

### 2.8: Frontend Auth Storage Utilities
-   **Objective:** Implement secure, browser-based storage for JWTs.
-   **Reference:** `2.8-Frontend-Auth-Storage-Utilities.md`
-   **Sub-Tasks:**
    -   [x] Create utility functions to get, set, and clear tokens from cookies.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Verified the `auth-storage.ts` utility, confirming the correct implementation of cookie-based token management functions.

### 2.9: Frontend Auth Hooks
-   **Objective:** Encapsulate all authentication-related state management and API calls into custom hooks.
-   **Reference:** `2.9-Frontend-Auth-Hooks.md`
-   **Sub-Tasks:**
    -   [x] Implement `useRegister`, `useLogin`, and `useLogout` mutation hooks.
    -   [x] Implement `useCurrentUser` query hook.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Created the `AuthService` and the full suite of React Query hooks (`useRegister`, `useLogin`, `useLogout`, `useCurrentUser`), connecting the UI to the backend services.

### 2.10: Frontend Auth UI & Forms
-   **Objective:** Build the user-facing login and registration pages.
-   **Reference:** `2.10-Frontend-Auth-UI-Forms.md`
-   **Sub-Tasks:**
    -   [x] Implement Zod validation schemas for login and registration.
    -   [x] Build the `LoginPage` component.
    -   [x] Build the `SignupPage` component.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Implemented Zod validation schemas and the complete `LoginPage` and `SignupPage` components, finalizing the user authentication UI.

### 2.11: Frontend Route Protection
-   **Objective:** Secure frontend routes to ensure only authenticated users can access protected areas.
-   **Reference:** `2.11-Frontend-Route-Protection.md`
-   **Sub-Tasks:**
    -   [x] Implement a `ProtectedRoute` higher-order component (HOC) or equivalent logic.
    -   [x] Apply protection to the main application shell and dashboard.
-   **Progress Report:**
    -   **Status:** Completed
    -   **Notes:** Created the RouteGuard component and applied it to the main dashboard layout, securing all protected routes.


---
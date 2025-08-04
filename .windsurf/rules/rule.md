---
trigger: always_on
---

# MartechEngine: Development Rules & Standard Operating Procedures (SOP)

**Purpose:** This document defines the mandatory rules and procedures for all development on the MartechEngine project. Its primary goal is to ensure code quality, consistency, and a smooth, auditable project management workflow. **All developers, including AI agents, MUST adhere to these rules at all times.**

---

## Section 1: Coding Standards & Style Guide

These rules ensure that our codebase is clean, readable, and maintainable.

### 1.1 General Principles
-   **Clarity Over Cleverness:** Write code that is easy to understand.
-   **DRY (Don't Repeat Yourself):** Abstract reusable logic into functions, services, or components.
-   **Security First:** Never hardcode secrets. Sanitize all user inputs. Use the provided security services for authentication and authorization.

### 1.2 Backend (Python & FastAPI)
1.  **Formatting:** All Python code **MUST** be formatted with `ruff format`. This is enforced automatically by pre-commit hooks.
2.  **Linting:** All Python code **MUST** pass `ruff --fix`. No code with linting errors will be committed.
3.  **Naming Conventions:**
    -   Variables and functions: `snake_case` (e.g., `project_service`).
    -   Classes: `PascalCase` (e.g., `ProjectService`).
    -   Constants: `UPPER_SNAKE_CASE` (e.g., `SCAN_COST`).
4.  **Type Hinting:** All function signatures and variable declarations **MUST** include type hints.
5.  **Architecture:**
    -   **Thin API, Fat Service:** API endpoints in `app/api/` are for HTTP concerns only (request/response validation, dependency injection, calling services).
    -   All business logic **MUST** be encapsulated in a corresponding service class within the `app/services/` directory.

### 1.3 Frontend (TypeScript & Next.js)
1.  **Formatting:** All code (TS, TSX, JSON, CSS) **MUST** be formatted with `prettier`. This is enforced automatically by pre-commit hooks.
2.  **Naming Conventions:**
    -   Variables and functions: `camelCase` (e.g., `useProjects`).
    -   Components and Types/Interfaces: `PascalCase` (e.g., `ProjectCard`, `Project`).
3.  **Component Structure:**
    -   Components should be small and have a single responsibility.
    -   Reusable UI elements go in `src/components/ui`.
    -   Feature-specific components go in `src/components/features/`.
4.  **State Management:**
    -   **Server State:** All data fetched from the API **MUST** be managed by `@tanstack/react-query` via our custom hooks.
    -   **Global Client State:** For UI state shared across many components (e.g., a theme toggle), use `Zustand`.
    -   **Local Component State:** Use React's native `useState` and `useReducer` hooks.
5.  **Data Fetching:**
    -   UI components **MUST NOT** call `axios` or `fetch` directly.
    -   All API interactions **MUST** be done through the custom hooks defined in the `src/hooks/` directory (e.g., `useProjects`, `useAuth`).

### 1.4 Git & Commits
1.  **Branching:** All new work **MUST** be done on a feature branch, named following the pattern `feature/short-description` (e.g., `feature/project-creation-api`).
2.  **Commit Messages:** All commit messages **MUST** follow the **Conventional Commits** specification. This is critical for generating changelogs and understanding the project's history.
    -   **Format:** `<type>(<scope>): <subject>`
    -   **Types:** `feat` (new feature), `fix` (bug fix), `docs` (documentation), `style` (formatting), `refactor`, `test`, `chore` (build changes).
    -   **Example:** `feat(backend): implement ProjectService with plan enforcement`

---

## Section 2: Project Management & AI Agent Workflow (SOP)

This section outlines the precise, step-by-step workflow for completing tasks. This is the **Standard Operating Procedure (SOP)**.

### **Step 1: Start a New Task**
1.  **Consult `TASK.md`:** Open the `TASK.md` file. Find the **first** task in the list that is not yet completed (marked with `[ ]`). This is your current task.
2.  **Read the Architecture:** Before writing any code, read the architectural document(s) listed in the task's "Reference" section. This provides the necessary context and requirements.
3.  **Review the `README.md`:** At the beginning of a work session, quickly review the `README.md` to re-familiarize yourself with the project's high-level vision and setup.

### **Step 2: Implement & Commit**
1.  Write the code required to complete all sub-tasks listed for your current task.
2.  Adhere strictly to the coding standards defined in Section 1 of this document.
3.  Once the implementation is complete and verified, commit the code with a clear, conventional commit message.

### **Step 3: Update Progress (The "Definition of Done")**
A task is only considered "done" after the following updates are made:

1.  **Update `TASK.md` (Mandatory):**
    -   Navigate to the task you just completed.
    -   Change the checkbox from `[ ]` to `[x]`.
    -   In the `Progress Report:` section for that task, add a **single-line note** summarizing the completion.
    -   **Example Note:** "Completed implementation, including Pydantic schemas and all CRUD endpoints."

2.  **Update `PROGRESS.md` (Conditional):**
    -   You only need to update `PROGRESS.md` when you complete a **major milestone**.
    -   **Rule:** If the task you just finished is the **last task of a Phase** (e.g., you just completed task `2.11`), you **MUST** also update `PROGRESS.md`.
    -   **Action:** In `PROGRESS.md`, update the table entry for that Phase: set the "Completion" to "100%" and the "Status" to "Completed".

### Workflow Quick Reference

| When to...                      | Which File...        | Action...                                                                  |
| ------------------------------- | -------------------- | -------------------------------------------------------------------------- |
| **Start any new work**          | `TASK.md`            | Find the next `[ ]` task.                                                  |
| **Understand a task's goal**    | *Architectural Docs* | Read the referenced file(s) (e.g., `1.1-Project-Skeleton.md`).              |
| **Get high-level project info** | `README.md`          | Read the vision and setup instructions.                                    |
| **Finish ANY task**             | `TASK.md`            | Mark the task as `[x]` and add a note to its `Progress Report`.            |
| **Finish the LAST task of a Phase** | `PROGRESS.md`        | Update the Phase status to "Completed" and "100%".                         |
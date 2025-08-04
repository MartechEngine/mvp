# MartechEngine: AI-Powered Marketing Intelligence Platform

**Version: 1.0.0** | **Status: In Development**

This repository contains the complete source code for MartechEngine, an AI-powered marketing intelligence platform designed to transform raw data into strategic insights.

## 1. Project Vision

MartechEngine's vision is to provide a single platform that tells the complete competitive story of a domain. Its core value proposition is the DCS (Domain Competitive Storytelling) Score, a proprietary metric aggregating technical, on-page, and off-page factors. The platform operates on a "Memory-First" principle: it runs deep, credit-consuming scans to populate a central "Project Memory," then allows users to perform fast analysis and AI-powered content generation using this stored intelligence.

**Core Business Logic:** Subscription-first SaaS model with a 7-day free trial, followed by a mandatory paid plan. AI features consume credits, which are allotted monthly and can be topped up.

## 2. Quick Start & Local Development

### Prerequisites
- Docker & Docker Compose
- Node.js (v18+) & npm
- Python (v3.11+) & pip
- Git

### Setup Instructions
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd martechengine
    ```

2.  **Backend Setup:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    # Fill in the required values in .env, especially SECRET_KEY
    ```

3.  **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    cp .env.local.example .env.local
    ```

4.  **Launch the Development Stack:**
    From the project root directory, create the root `.env` file for Docker Compose:
    ```bash
    cp .env.example .env
    # The default values are fine for local development
    ```
    Then, launch the services:
    ```bash
    docker-compose up --build
    ```

5.  **Accessing the Application:**
    -   **Frontend:** `http://localhost:3000`
    -   **Backend API:** `http://localhost:8000/docs`

## 3. Core Architectural Principles

-   **Asynchronous by Default:** Long-running operations are offloaded to Celery background workers.
-   **Security by Design:** Multi-layered security with least-privilege IAM, non-root containers, and a secure JWT refresh token system.
-   **Strongly-Typed Data Contracts:** Pydantic (backend) and TypeScript (frontend) enforce a strict, shared data contract.
-   **Thin API, Fat Service:** API endpoints handle HTTP concerns only; all business logic is encapsulated in the service layer.

---
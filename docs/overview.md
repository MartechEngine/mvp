MartechEngine: The Complete Architectural Blueprint (v1.4 - Commercial-Grade)
Document Version: 1.4 (Commercial-Grade MVP)
Date: May 22, 2024
Status: Finalized Architectural Plan for Implementation
Table of Contents
High-Level Overview
1.1. Short Overview
1.2. User Flow Overview
Executive Summary
2.1. Project Vision & Core Business Logic
2.2. Monetization Strategy
Core Architectural Principles
System Architecture Overview (Cloud Run Edition)
4.1. High-Level System Diagram
4.2. Component Responsibilities
Technology Stack
Backend Architecture: A Microscopic Deep Dive
6.1. Data Models: The Foundation (RAG-Ready & Auditable)
6.2. The Service Layer: Encapsulated Business Logic
6.3. Credit Enforcement & Fault Tolerance (NEW)
6.4. The API Layer: Secure & Thin Gateway
6.5. The Asynchronous Subsystem: Celery for Scale
Frontend Architecture: A Microscopic Deep Dive
7.1. Framework & Core Principles
7.2. State Management Strategy
7.3. API Client & Data Flow
7.4. UI Component & Design System
Frontend Sitemap, Navigation, and UI
8.1. Navigational Principles
8.2. Complete Application Sitemap
8.3. Global Navigation Components (Header & Sidebar)
8.4. Contextual Content Generation CTAs
Critical Workflows (Sequence Diagrams)
9.1. New User Registration & Trial Activation
9.2. DCS Scan Execution Workflow (with Credit Enforcement)
9.3. Secure JWT Refresh Token Flow
Enterprise Readiness: Operations, Security & Testing
10.1. Observability Stack (GCP Native)
10.2. Deployment Strategy (Cloud Run with Traffic Splitting)
10.3. Multi-Layered Testing Strategy
10.4. Local-First Development Environment
High-Level Implementation Roadmap

1. High-Level Overview
1.1. Short Overview
MartechEngine is an AI-powered marketing intelligence platform that transforms raw data into strategic insights. It runs deep "DCS Scans" on websites, analyzing technical SEO, performance, and competitive data. This populates a "Project Memory," which then powers specialized analysis hubs and an AI content generator. The system is a subscription-based SaaS product with a usage-based credit system for AI features. For the MVP, it will be deployed on a scalable, serverless Google Cloud Run architecture, prioritizing developer velocity with a fully containerized local environment and a feature-rich, modern frontend.
1.2. User Flow Overview
Onboarding: A new user signs up and is automatically placed on a 7-day free trial. They create their first "Project" by providing a website URL.
Discovery (DCS Scan): The user initiates a "DCS Scan" on their project. This is an asynchronous background job. They can watch its progress in real-time via a Server-Sent Events (SSE) stream.
Analysis: Once the scan is complete, the user navigates through dedicated Analysis Hubs (Site Audit, Keyword Research, Backlink Analysis) to explore the data. Each hub provides deep insights, visualizations, and tables based on the scan's findings.
Action (Content Generation): Within the analysis hubs, the user encounters contextual Calls-to-Action (CTAs). For example, next to a "Missing Meta Description" issue, a "Generate" button appears.
Creation: Clicking a CTA takes the user to the Content Hub, where the AI generator is pre-configured with the context from the issue. The user confirms, consumes AI credits, and receives the generated content (e.g., a new meta description).
Monetization: When the trial ends or credits run low, the user is prompted to subscribe to a paid plan and can purchase additional credits from the billing page.
2. Executive Summary
2.1. Project Vision & Core Business Logic
MartechEngine's vision is to provide a single platform that tells the complete competitive story of a domain. Its core value proposition is the DCS (Domain Competitive Storytelling) Score, a proprietary, weighted metric aggregating technical, on-page, and off-page factors. The platform operates on a "Memory-First" principle: it runs deep, credit-consuming scans to populate a central "Project Memory," then allows users to perform fast, often free, analysis and AI-powered content generation using this stored intelligence.
2.2. Monetization Strategy
The business model is a subscription-first hybrid:
Free Trial: A 7-day trial of a paid plan with a one-time grant of AI credits.
Mandatory Subscription: A paid subscription is required post-trial for continued platform access.
AI Credits: Generative AI tasks consume credits. Users receive a monthly credit allotment with their subscription.
Credit Top-ups: Paid users can purchase additional AI credits.
Immutable Ledger: All credit transactions are recorded in an immutable CreditLedger table for perfect auditability.
3. Core Architectural Principles
Asynchronous by Default: Long-running operations are offloaded to Celery background workers to keep the API fast.
Security by Design: Multi-layered security including least-privilege IAM, non-root containers, bcrypt hashing, and a secure JWT refresh token rotation system.
Resilience & Fallbacks: External API clients are built with retries and circuit breakers. The DCS scan has a data-sourcing fallback chain (DataForSEO -> Custom Crawler -> Vertex AI Estimate).
Strongly-Typed Data Contracts: Pydantic (backend) and TypeScript (frontend) enforce a strict, shared data contract.
Thin API, Fat Service: API endpoints handle HTTP concerns only; all business logic is encapsulated in the service layer.
Simplified & Scalable Deployment: The MVP uses Google Cloud Run for auto-scaling, serverless container deployment.
Maximum Development Velocity: The development environment is optimized for speed with a comprehensive Docker setup, hot-reloading for all services, and automated quality gates through pre-commit hooks.
4. System Architecture Overview (Cloud Run Edition)
4.1. High-Level System Diagram
graph TD
    subgraph "User's Browser"
        A[Next.js Frontend]
    end

    subgraph "External Services"
        B((Payment Provider))
        C((3rd Party APIs <br> DataForSEO, Google))
    end
    
    subgraph "MartechEngine Production Environment (GCP Serverless)"
        D[Cloud Load Balancer + Cloud Armor] --> E[Cloud Run: Backend API]
        
        E -- "Enqueues tasks in" --> F[Cloud Memorystore: Redis]
        E -- "Reads/Writes to" --> G[Cloud SQL: PostgreSQL]
        
        H[Cloud Run: Celery Worker] -- "Consumes tasks from" --> F
        I[Cloud Run: Celery Beat] -- "Schedules tasks in" --> F
        
        H -- "Reads/Writes to" --> G
        H -- "Calls" --> C
        
        A -- "API Calls" --> D
        B -- "Webhooks" --> D
    end

4.2. Component Responsibilities
Next.js Frontend: A client- and server-rendered single-page application that provides the entire user interface. Served via a serverless host like Vercel or Cloud Run.
Cloud Run (Backend API): A serverless, auto-scaling container running our FastAPI application. Handles all synchronous API requests.
Cloud SQL (PostgreSQL): A fully managed relational database service. The single source of truth for all data.
Cloud Memorystore (Redis): A fully managed Redis service for Celery task queuing and real-time SSE Pub/Sub.
Cloud Run (Celery Worker): A separate, auto-scaling container that executes all long-running background jobs.
Cloud Run (Celery Beat): A singleton container running the Celery Beat scheduler for all cron-like tasks.
5. Technology Stack
(This section remains the same as the previous version, detailing the choices of Python, FastAPI, Next.js, TanStack Query, Zustand, PostgreSQL, Redis, Docker, Cloud Run, etc.)

6. Backend Architecture: A Microscopic Deep Dive
6.1. Data Models: The Foundation (RAG-Ready & Auditable)
The data model foundation is updated to support robust financial and operational auditing.
Multi-Tenancy: The User -> Membership -> Organization model remains the core of data isolation.
Billing & Monetization: Plan and Subscription models are unchanged.
CreditLedger (Revised & Enhanced): The immutable ledger is enhanced to become a fully auditable transactional record.
id, organization_id, user_id, created_at
amount: Integer. Positive for additions, negative for consumption.
action_type (NEW): Enum (SCAN, GENERATION, REFILL, REFUND, SIGNUP_BONUS) to categorize the transaction.
status (NEW): Enum (RESERVED, CONSUMED, REFUNDED, FAILED). A transaction begins as RESERVED and transitions to CONSUMED on success or REFUNDED on failure.
reference_id (NEW): A foreign key linking this transaction directly to the source record (e.g., audit_id, generated_content_asset_id).
reason (NEW): A text field storing the failure reason for REFUNDED or FAILED transactions.
retry_of_ledger_id (NEW): A self-referencing key to link a new attempt to a previously failed transaction.
DCS & AI Data (Three-Tier Architecture): The CentralRawData, ProjectMemory, and Audit/ScanResult models are unchanged, remaining RAG-ready. The Audit model will now display a failure_reason.
6.2. The Service Layer: Encapsulated Business Logic
The services are updated to implement the new fault tolerance logic.
CreditService: Now manages the full lifecycle of a credit transaction: reserve_credits, consume_reservation, and refund_reservation. The reserve_credits method will now first check the organization's current balance and fail immediately if insufficient.
SubscriptionService: The process_monthly_refills task (run by Celery Beat) is now idempotent. It will check the last_refill_date on the Subscription model and only grant credits if the billing anniversary has passed and a refill hasn't already occurred for that period.
DCSOrchestrationEngine & UnifiedAIService: These services are now wrapped in a master try/except block. On any exception during the task, the finally block ensures the refund_reservation method on the CreditService is called, guaranteeing credits are not lost on failure.
6.3. Credit Enforcement & Fault Tolerance (NEW)
This is a new set of core principles that govern all credit-consuming operations in the system.
Pre-authorization Check: Before any credit-consuming task is enqueued (e.g., starting a scan), the API layer will call CreditService.has_sufficient_balance(org_id, required_amount). If this check fails, the API returns a 402 Payment Required error immediately, preventing the task from ever starting.
Transactional Reservation: Every credit-consuming Celery task begins by calling CreditService.reserve_credits(). This creates a CreditLedger entry with status=RESERVED and amount=-[cost]. This atomically decrements the user's "available balance" while the funds are in escrow.
On Success: Consumption: If the task completes successfully, it calls CreditService.consume_reservation(ledger_id), which simply updates the status of the ledger entry from RESERVED to CONSUMED. The transaction is complete.
On Failure: Refund: If the task fails for any reason (API error, timeout, internal exception), the Celery task's failure handler calls CreditService.refund_reservation(ledger_id, reason). This updates the status to REFUNDED and creates a new, corresponding positive transaction for the same amount, ensuring the ledger remains immutable and the balance is correctly restored.
Abuse & Retry Prevention:
Email Verification: A user's is_verified flag must be true before they are allowed to trigger any scan.
Scan Cooldown: A simple cache check (e.g., Redis SETEX) will prevent the same domain from being scanned more than once every 5 minutes to prevent accidental duplicates.
Retry Limiting: The Audit model will track retry_count. The API will reject scan requests for a project that has a currently running or recently failed scan that is still within its retry window.
6.4. The API Layer: Secure & Thin Gateway
The API layer is now responsible for the initial credit check.
Example: POST /dcs/scans/{projectId}/start Endpoint:
Get current user and project.
Check if user is is_verified.
Check scan cooldown cache.
Call CreditService.has_sufficient_balance(org_id, 300). If False, return 402 Payment Required with a clear error message.
Only if all checks pass, create the Audit record and enqueue the Celery task.
6.5. The Asynchronous Subsystem: Celery for Scale
The Celery task definitions are enhanced with robust error handling to ensure refunds are processed.
run_dcs_scan Task (Pseudocode):
@shared_task(bind=True)
def run_dcs_scan(self, audit_id):
    reservation_id = None
    try:
        # 1. Reserve Credits
        reservation_id = credit_service.reserve_credits(...)
        # 2. Run the full scan logic...
        ...
        # 3. If successful, consume the reservation
        credit_service.consume_reservation(reservation_id)
    except Exception as e:
        # 4. If any error occurs, refund the reservation
        if reservation_id:
            credit_service.refund_reservation(reservation_id, reason=str(e))
        # Re-raise exception to mark task as FAILED
        raise e

7. Frontend Architecture: A Microscopic Deep Dive
(This section is largely unchanged but will now leverage the enhanced API responses.)
8. Frontend Sitemap, Navigation, and UI
The UI is updated to reflect the new credit-aware and fault-tolerant backend.

8.2 Clarify the purpose of the existing hubs (Site Audit, Keyword Research) as "live workspaces" showing the latest aggregated data.
Add the new pages for historical reports:
/projects/{projectId}/scans/ (The Scan History list)
/projects/{projectId}/scans/{auditId} (The detailed Unified Scan Report)

8.3. Global Navigation Components (Header & Sidebar)
Header:
CreditMeter: Now fetches and displays the available credit balance. Hovering over it could show a tooltip with "X credits reserved for ongoing scans."
Sidebar: Unchanged.
8.4. Contextual Content Generation CTAs
Credit Cost Display: All CTA buttons that trigger credit-consuming actions will now dynamically display the cost.
Example Button Text: Run Deep Scan (⚡ 300 Credits) or Generate Meta Tags (⚡ 2 Credits).
The button will be disabled with a helpful tooltip if the user's available balance is less than the required cost.
Confirmation Modals: Clicking a credit-consuming CTA will open a confirmation modal:
Content: "This action will consume 2 credits. Your remaining balance will be 118. Do you want to continue?"
Buttons: "Confirm" and "Cancel".
9. Critical Workflows (Sequence Diagrams)
9.2. DCS Scan Execution Workflow (with Credit Enforcement)
sequenceDiagram
    participant Frontend
    participant API
    participant CreditService
    participant CeleryTask
    
    Frontend->>API: POST /dcs/scans/.../start
    API->>CreditService: has_sufficient_balance(300)?
    alt Balance OK
        CreditService-->>API: True
        API->>CeleryTask: Enqueue run_dcs_scan(audit_id)
        API-->>Frontend: 202 Accepted
    else Insufficient Balance
        CreditService-->>API: False
        API-->>Frontend: 402 Payment Required
    end

    sequence Celery Execution
        CeleryTask->>CreditService: reserve_credits(300) -> reservation_id
        alt Scan Fails
            CeleryTask->>CeleryTask: Exception Occurs!
            CeleryTask->>CreditService: refund_reservation(reservation_id, "API Error")
        else Scan Succeeds
            CeleryTask->>CreditService: consume_reservation(reservation_id)
        end
    end



app.martechnine.ai sitemap:

Complete Application Sitemap
This sitemap provides a detailed, page-by-page blueprint of the entire MartechEngine application. It is organized by user state (public vs. authenticated) and by the application's primary navigation areas.
These pages are accessible to any visitor and are focused on getting users into the application. They share a minimal, branded layout without the main application's sidebar or header.
/login
Purpose: To serve as the primary gateway for existing users.
Description: This page presents a clean, simple form for a user to enter their email and password. It will provide clear feedback for common errors such as "Invalid credentials" or "Please verify your email first." Upon successful login, the system will set the necessary authentication tokens and redirect the user to their main project hub (/dashboard).
/signup
Purpose: To onboard new users and their organizations.
Description: This page features a straightforward registration form asking for the user's full name, their organization's name, an email address, and a secure password. Upon successful submission, a new user and their parent organization are created in the backend. The user is then redirected to the /login page with a message instructing them to check their email to complete the verification process.
/auth/verify-email
Purpose: To confirm that a user has access to the email address they signed up with.
Description: This is not a page a user navigates to directly. They land here after clicking a unique link sent to their email. The page automatically reads a token from the URL, sends it to the backend for validation, and then displays a clear, full-screen message indicating whether the verification was successful or if the link has expired.
Purpose: To act as an intelligent, invisible traffic director.
Description: The root of the application (/) is not a destination. When a user lands here, the application performs a quick, silent check for a valid authentication token.
If a valid token is found, the user is instantly and seamlessly redirected to their /dashboard.
If no token is found, they are redirected to the /login page.
A full-page loading animation is shown for the fraction of a second this check takes, ensuring a smooth user experience.
This is the core of the application, where all analysis and content work happens. Access is strictly limited to authenticated users, and all content is contextual to the specific projectId present in the URL.
/dashboard (Project Hub - Global)
Purpose: To serve as the user's main landing page and central hub for managing all their projects.
Description: After logging in, the user lands here. The page displays a grid of cards, each representing one of their projects. It allows them to quickly see the status of their projects and click to dive into a specific one. This page also features the most prominent "Create New Project" button.
/projects/{projectId}/dashboard (Project-Specific Dashboard)
Purpose: To provide a high-level "at-a-glance" overview of a single project's health.
Description: This is the main dashboard for a selected project. It will feature large, clear widgets for the latest overall DCS Score, a summary of critical issues found in the last scan, and trend lines for key metrics. This page serves as the springboard into the more detailed analysis hubs and contains the "Start New Scan" CTA.
Site Audit Hub (/projects/{projectId}/site-audit/)
/projects/{projectId}/site-audit/overview (Default View)
Purpose: To summarize the technical health of the project's website.
Description: Presents key scores related to technical SEO, highlights the top 3-5 most critical issues (e.g., "5 broken internal links," "12 pages with missing meta descriptions"), and provides clear data visualizations.
/projects/{projectId}/site-audit/all-issues
Purpose: To provide an exhaustive, actionable list of all technical problems.
Description: A detailed, sortable, and filterable data table of every single issue discovered during the last scan. Each row represents an issue and is accompanied by a contextual CTA to help fix it (e.g., a "Generate Meta Tag" button).
Keyword Research Hub (/projects/{projectId}/keyword-research/)
/projects/{projectId}/keyword-research/overview (Default View)
Purpose: To provide a strategic overview of the project's keyword landscape.
Description: Features widgets for key metrics like total keywords ranked for, estimated organic traffic, and a visual breakdown of the main semantic topic clusters the site is associated with.
/projects/{projectId}/keyword-research/gaps
Purpose: To uncover high-potential keywords that competitors are ranking for, but the user is not.
Description: A data table of valuable keyword opportunities, complete with search volume and difficulty metrics. Each row is an opportunity and features a "Write Article" CTA.
/projects/{projectId}/keyword-research/tracker
Purpose: To monitor search engine ranking performance over time for the most important keywords.
Description: A page where users can add specific keywords to track. It displays a historical line chart and a data table showing how the project's ranking for those keywords has changed over days or weeks.
Content Hub (/projects/{projectId}/content/)
/projects/{projectId}/content/library (Default View)
Purpose: To act as the central repository for all AI-generated content for the project.
Description: This is the project's "memory" made visible. It's a full-page, searchable, and filterable data table where users can find every piece of content ever generated, from meta tags to full blog posts.
/projects/{projectId}/content/generator
Purpose: To serve as the interactive AI-powered writing assistant.
Description: A powerful, two-column interface. On the left, the user provides instructions to the AI (topic, keywords, tone of voice). On the right, the generated content appears. This page is "smart" and can be pre-filled with context when a user clicks a CTA from another part of the app.
These pages are for managing global account and billing information. They are not tied to a specific project.
/settings/account
Purpose: To allow users to manage their personal profile information.
Description: A clean and simple page with forms for updating their full name and changing their password.
/settings/billing
Purpose: To provide a comprehensive overview of the user's subscription and billing history.
Description: This page shows the user's current subscription plan (e.g., "Pro Plan"), its status (e.g., "Active" or "Trialing"), and the next billing date. It also contains a detailed, paginated table of every transaction from their credit ledger.
/settings/purchase-credits
Purpose: To provide a focused, streamlined experience for purchasing additional AI credits.
Description: A simple, conversion-focused page that displays the available credit packs (e.g., "1,000 Credits for $10") and a clear checkout button that initiates the payment process.
8.3. Global Navigation Components (Header & Sidebar)
The global navigation ensures a consistent and intuitive experience across the entire authenticated application.
Header (Top Bar)
Purpose: Manages the global context and provides access to high-level actions.
Components:
ProjectSelector: A prominent dropdown on the left that displays the name of the currently active project. Clicking it reveals a list of all other projects, allowing the user to switch their entire workspace context with a single click.
CreditMeter: A real-time display in the center-right showing the organization's available credit balance (e.g., "⚡ 1,250 Credits").
BuyCreditsButton: A highly visible call-to-action button (e.g., "+ Buy Credits") located next to the credit meter. It navigates the user directly to the /settings/purchase-credits page. This button is only visible for users on paid plans.
UserNav: A dropdown on the far right, usually triggered by clicking the user's avatar. It contains links to global pages that are not project-specific, such as /settings/account, and includes the "Logout" action.
Sidebar (Left Navigation)
Purpose: Provides the primary, deep navigation within a selected project's workspace. It is structured to be hierarchical and context-aware.
Structure:
Top Section (Dynamic & Project-Specific): This section's links are all dependent on the project selected in the Header. If no project is selected, these links are disabled.
Project Dashboard: A single link to the project's main overview.
Site Audit: A collapsible menu item. When expanded, it reveals sub-menu links to Overview and All Issues.
Keyword Research: A collapsible menu item revealing sub-menu links to Overview, Keyword Gaps, and Rank Tracker.
Content Hub: A collapsible menu item revealing sub-menu links to Library and Generator.
(Visual Divider)
Bottom Section (Static & Global): This section is always visible and contains links to pages that are not tied to a specific project.
Settings: A single, clear menu item, often accompanied by a gear icon. This is the last item in the sidebar. Clicking it expands to reveal the final set of navigation links:
Account (links to /settings/account)
Billing & Plan (links to /settings/billing)
Purchase Credits (links to /settings/purchase-credits)
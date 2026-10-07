# Software Requirements Specification (SRS)
## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Draft                         |
| **Date**            | 2026-10-07                    |
| **Author(s)**       | Magazine Portal Core Team     |
| **Reviewed by**     | —                             |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Functional Requirements](#3-functional-requirements)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [System Architecture Requirements](#5-system-architecture-requirements)
6. [Security & Authentication Requirements](#6-security--authentication-requirements)
7. [Data Requirements](#7-data-requirements)
8. [External Interface Requirements](#8-external-interface-requirements)
9. [Constraints & Assumptions](#9-constraints--assumptions)
10. [Glossary](#10-glossary)

---

## 1. Introduction

### 1.1 Purpose
This SRS describes the complete functional and non-functional requirements for the **College Unified Magazine Portal** — a centralized micro-frontend web platform that aggregates, organizes, and showcases all student publications across multiple academic years.

### 1.2 Scope
The system covers:
- A **Flask-based Core Portal** that auto-discovers and serves all magazine editions.
- A **Micro-Frontend Plugin Architecture** allowing independent sub-teams to develop departmental, hostel, and annual magazines.
- A **Universal Embedded Reader** using `<iframe>` for seamless in-browser reading.
- Role-based access for **Visitors**, **Contributors**, and **Administrators**.

### 1.3 Intended Audience
- Software Architects & Lead Developers
- Sub-team developers (Departmental, Bhavan, Annual)
- College administrators and faculty coordinators
- QA testers
- Deployment / DevOps personnel

### 1.4 Definitions & Acronyms

| Term         | Definition                                                                  |
|--------------|-----------------------------------------------------------------------------|
| SRS          | Software Requirements Specification                                         |
| PRD          | Product Requirements Document                                               |
| MFE          | Micro-Frontend                                                              |
| Flask        | Python-based lightweight WSGI web framework                                 |
| Edition      | A self-contained magazine mini-site (one `index.html` entry point)         |
| Hard Collar  | Mandatory contract: every plugin MUST have `index.html` at its root        |
| Bhavan       | College hostel unit (5 in total)                                            |
| RBAC         | Role-Based Access Control                                                   |
| CI/CD        | Continuous Integration / Continuous Deployment                              |
| CSRF         | Cross-Site Request Forgery                                                  |
| CSP          | Content Security Policy                                                     |
| HSTS         | HTTP Strict Transport Security                                              |

### 1.5 References
- `PRD.md` — Product Requirements Document
- `ARCHITECTURE.md` — System Architecture Design
- `SECURITY.md` — Security & Authentication Design
- `API_DESIGN.md` — API Design Document
- `TEST_PLAN.md` — Test Plan

---

## 2. Overall Description

### 2.1 Product Perspective
The portal is a standalone internal web application deployed on a college server or cloud host. It acts as an aggregation hub — it does **not** create magazines itself, but discovers, indexes, and presents them through a unified interface.

### 2.2 Product Functions (Summary)

| # | Function                                                                 |
|---|--------------------------------------------------------------------------|
| F1 | Auto-scan the repository for new magazine editions                      |
| F2 | Present a landing page with categorised navigation                      |
| F3 | Embed any edition inside an `<iframe>` reader pane                      |
| F4 | Allow admins to publish/unpublish editions                              |
| F5 | Allow admin to set metadata (title, description, cover image) per edition |
| F6 | Support multiple academic years                                         |
| F7 | Provide an Admin Dashboard for edition management                       |
| F8 | Enable Contributor submission workflow via GitHub PR                    |

### 2.3 User Classes and Characteristics

| User Class          | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Visitor (Public)**| Unauthenticated user browsing and reading any published edition.            |
| **Contributor**     | Sub-team member who submits magazine files via Git Pull Request.            |
| **Admin**           | Portal administrator who reviews, approves, and manages editions & metadata.|
| **Super-Admin**     | Root-level user who manages admin accounts and system configuration.        |

### 2.4 Operating Environment
- **Server OS:** Linux (Ubuntu 22.04 LTS recommended) or Windows Server
- **Python Version:** >= 3.10
- **Web Framework:** Flask >= 3.0
- **Browsers Supported:** Chrome >= 110, Firefox >= 110, Edge >= 110, Safari >= 16
- **Deployment:** Local server / AWS EC2 / Railway / Render / any WSGI-compatible host

### 2.5 Design and Implementation Constraints
- All magazine plugins MUST contain an `index.html` as their root entry (Hard Collar).
- No relational database required; JSON metadata files act as the data layer.
- The portal must function without internet access (all assets served locally).
- Sub-team files must be under 50 MB per edition (uncompressed).

### 2.6 Assumptions and Dependencies
- Sub-teams have basic HTML/CSS/JS knowledge.
- A GitHub (or GitLab) repository is used as the central code repository.
- The college provides a server with Python 3.10+ and pip access.
- An admin manages the repository and approves all PRs.

---

## 3. Functional Requirements

### 3.1 Public Portal — FR-PUB

| ID         | Requirement                                                                                               | Priority |
|------------|-----------------------------------------------------------------------------------------------------------|----------|
| FR-PUB-01  | The system SHALL display a landing page with college branding, hero section, and edition categories.      | MUST     |
| FR-PUB-02  | The landing page SHALL list editions grouped under: **Annual**, **Departmental**, and **Bhavan**.         | MUST     |
| FR-PUB-03  | Each category SHALL support filtering by **Academic Year**.                                               | MUST     |
| FR-PUB-04  | Clicking an edition SHALL embed it in an `<iframe>` viewer within the portal.                             | MUST     |
| FR-PUB-05  | The portal SHALL provide a search bar to find editions by title, department, or year.                     | SHOULD   |
| FR-PUB-06  | Each edition card SHALL display: title, cover image, year, category, and a "Read" button.                | MUST     |
| FR-PUB-07  | The portal SHALL support responsive design for mobile, tablet, and desktop viewports.                     | MUST     |
| FR-PUB-08  | The portal SHALL display a "No editions published yet" state when a category is empty.                    | MUST     |
| FR-PUB-09  | A "Fullscreen" button SHALL allow readers to expand the `<iframe>` to full browser window.               | SHOULD   |
| FR-PUB-10  | The portal SHALL show a loading indicator while an edition is being loaded in the iframe.                 | SHOULD   |

### 3.2 Backend Auto-Scanner — FR-SCAN

| ID          | Requirement                                                                                               | Priority |
|-------------|-----------------------------------------------------------------------------------------------------------|----------|
| FR-SCAN-01  | On startup, Flask SHALL scan `static/magazines/` and build an in-memory index of all editions.            | MUST     |
| FR-SCAN-02  | The scanner SHALL expose `GET /api/editions` returning a JSON feed of all published editions.             | MUST     |
| FR-SCAN-03  | The JSON feed SHALL include: `id`, `title`, `year`, `category`, `sub_id`, `path`, `cover_image`, `published`. | MUST |
| FR-SCAN-04  | The scanner SHALL only include editions where `published: true` in their `meta.json`.                     | MUST     |
| FR-SCAN-05  | An admin endpoint `POST /api/admin/rescan` SHALL force a re-index without restarting the server.          | SHOULD   |
| FR-SCAN-06  | If a `meta.json` is absent, the scanner SHALL log a warning and skip that directory.                      | MUST     |
| FR-SCAN-07  | Hot-reloading of new editions WITHOUT server restart SHALL be supported in development mode.              | COULD    |

### 3.3 Admin Dashboard — FR-ADM

| ID         | Requirement                                                                                               | Priority |
|------------|-----------------------------------------------------------------------------------------------------------|----------|
| FR-ADM-01  | Admin route `/admin` SHALL be protected by login authentication.                                          | MUST     |
| FR-ADM-02  | Dashboard SHALL list all discovered editions (published and unpublished).                                 | MUST     |
| FR-ADM-03  | Admin SHALL toggle the `published` status of any edition.                                                 | MUST     |
| FR-ADM-04  | Admin SHALL edit edition metadata: title, description, cover image URL, tags.                             | MUST     |
| FR-ADM-05  | Admin SHALL create, edit, and delete admin accounts (Super-Admin only).                                   | MUST     |
| FR-ADM-06  | Dashboard SHALL show last scan timestamp and allow manual re-scan.                                        | SHOULD   |
| FR-ADM-07  | Admin SHALL be able to view server-side logs from the dashboard.                                          | COULD    |

### 3.4 Authentication & Authorization — FR-AUTH

| ID          | Requirement                                                                                               | Priority |
|-------------|-----------------------------------------------------------------------------------------------------------|----------|
| FR-AUTH-01  | System SHALL implement a secure admin login page at `/admin/login`.                                       | MUST     |
| FR-AUTH-02  | Admin credentials SHALL be stored hashed (bcrypt) and never in plain text.                               | MUST     |
| FR-AUTH-03  | On successful login, a secure HTTP-only session cookie SHALL be issued.                                   | MUST     |
| FR-AUTH-04  | Sessions SHALL expire after 60 minutes of inactivity.                                                     | MUST     |
| FR-AUTH-05  | Failed login attempts SHALL be rate-limited: 5 per 15 minutes per IP.                                    | MUST     |
| FR-AUTH-06  | All `/admin/*` routes SHALL require a valid session; others redirect to `/admin/login`.                   | MUST     |
| FR-AUTH-07  | A CSRF token SHALL be validated on all state-mutating form submissions.                                   | MUST     |
| FR-AUTH-08  | Super-Admin SHALL be the only role that can create or delete admin accounts.                              | MUST     |

### 3.5 Metadata Contract — FR-META

| ID          | Requirement                                                                                               | Priority |
|-------------|-----------------------------------------------------------------------------------------------------------|----------|
| FR-META-01  | Each edition directory MUST contain a `meta.json` file at its root.                                      | MUST     |
| FR-META-02  | `meta.json` SHALL follow the canonical schema defined in `API_DESIGN.md`.                                 | MUST     |
| FR-META-03  | The system SHALL validate `meta.json` on scan and reject malformed entries with a logged error.           | MUST     |
| FR-META-04  | Admin edits to metadata via the dashboard SHALL be written back to the corresponding `meta.json`.         | SHOULD   |

---

## 4. Non-Functional Requirements

### 4.1 Performance — NFR-PERF

| ID            | Requirement                                                                              |
|---------------|------------------------------------------------------------------------------------------|
| NFR-PERF-01   | Landing page SHALL load within **2 seconds** on a 10 Mbps connection.                  |
| NFR-PERF-02   | `/api/editions` SHALL respond within **200ms** under normal load.                       |
| NFR-PERF-03   | The portal SHALL support at least **200 concurrent visitors** without degradation.       |
| NFR-PERF-04   | The portal itself SHALL NOT add more than 100ms overhead to iframe loading.             |

### 4.2 Reliability — NFR-REL

| ID           | Requirement                                                                              |
|--------------|------------------------------------------------------------------------------------------|
| NFR-REL-01   | Portal SHALL have >= 99% uptime during college hours (8am–10pm).                        |
| NFR-REL-02   | Failure of one edition plugin SHALL NOT crash or hang the rest of the portal.           |
| NFR-REL-03   | The system SHALL gracefully handle missing files, showing a "Content Unavailable" error.|

### 4.3 Scalability — NFR-SCALE

| ID             | Requirement                                                                             |
|----------------|-----------------------------------------------------------------------------------------|
| NFR-SCALE-01   | Adding a new academic year SHALL require only creating a new directory.                |
| NFR-SCALE-02   | Adding a new department or bhavan SHALL only need a folder + `meta.json`.              |
| NFR-SCALE-03   | System SHALL handle >= 100 edition plugins without degrading scan or API performance.  |

### 4.4 Security — NFR-SEC

| ID           | Requirement                                                                              |
|--------------|------------------------------------------------------------------------------------------|
| NFR-SEC-01   | All admin communications SHALL be over HTTPS in production.                             |
| NFR-SEC-02   | System SHALL prevent XSS attacks via Content Security Policy (CSP) headers.            |
| NFR-SEC-03   | Admin pages SHALL set `X-Frame-Options: SAMEORIGIN` to prevent clickjacking.           |
| NFR-SEC-04   | No admin credentials or secrets SHALL be committed to the repository.                  |
| NFR-SEC-05   | User input in search and metadata fields SHALL be sanitized server-side.               |

### 4.5 Maintainability — NFR-MAINT

| ID             | Requirement                                                                             |
|----------------|-----------------------------------------------------------------------------------------|
| NFR-MAINT-01   | Codebase SHALL follow PEP 8 (Python) and a documented JS style guide.                 |
| NFR-MAINT-02   | All Flask routes SHALL have corresponding docstrings.                                  |
| NFR-MAINT-03   | A `CONTRIBUTING.md` guide SHALL be available for sub-team onboarding.                 |

### 4.6 Usability — NFR-USE

| ID           | Requirement                                                                              |
|--------------|------------------------------------------------------------------------------------------|
| NFR-USE-01   | A visitor SHALL find and open a magazine edition within **3 clicks**.                   |
| NFR-USE-02   | UI SHALL follow WCAG 2.1 AA accessibility standards.                                    |
| NFR-USE-03   | All interactive elements SHALL have visible focus indicators.                           |

---

## 5. System Architecture Requirements

| ID    | Requirement                                                                                     |
|-------|-------------------------------------------------------------------------------------------------|
| SA-01 | System SHALL follow a micro-frontend plugin architecture.                                       |
| SA-02 | Flask app SHALL serve as both a static file server and an API server.                          |
| SA-03 | Magazine plugins SHALL be isolated; they MUST NOT import each other's assets.                  |
| SA-04 | System SHALL use a filesystem-based data layer (`meta.json` files), not a relational database. |
| SA-05 | System SHALL be deployable via `python app.py` with a single command after setup.              |

---

## 6. Security & Authentication Requirements

> Detailed design is in `SECURITY.md`. Requirements summarized here for traceability.

| ID     | Requirement                                                                                    |
|--------|-----------------------------------------------------------------------------------------------|
| SEC-01 | Admin login SHALL use username + password with bcrypt hashing.                                |
| SEC-02 | Session tokens SHALL be stored server-side (Flask session with a strong SECRET_KEY).          |
| SEC-03 | SECRET_KEY and admin credentials SHALL be stored in `.env` (never committed to git).         |
| SEC-04 | Rate limiting SHALL be applied to `/admin/login` endpoint.                                    |
| SEC-05 | CSRF protection SHALL be implemented for all form submissions.                                |
| SEC-06 | HTTP Security headers SHALL be configured: CSP, HSTS, X-Content-Type-Options, Referrer-Policy.|
| SEC-07 | File path traversal attacks SHALL be prevented; scanner MUST use safe path validation.        |
| SEC-08 | `.env` file and credential store SHALL be listed in `.gitignore`.                            |

---

## 7. Data Requirements

### 7.1 `meta.json` Schema

```json
{
  "id": "string (unique, e.g. 'cs-2026')",
  "title": "string",
  "year": "integer",
  "category": "annual | departmental | bhavan",
  "sub_id": "string (e.g. 'cs', 'bhavan1', null for annual)",
  "description": "string",
  "cover_image": "string (relative path to cover image)",
  "tags": ["string"],
  "published": "boolean",
  "published_date": "ISO8601 date string | null",
  "author_team": "string"
}
```

### 7.2 API Response Schema
Full schema is defined in `API_DESIGN.md`.

---

## 8. External Interface Requirements

### 8.1 User Interface
- Web browser (no mobile app required in v1.0)
- Responsive layout (min supported width: 320px)

### 8.2 Software Interfaces
- Flask WSGI server
- GitHub / GitLab for source code management and PR workflow
- `python-dotenv` for environment variable management
- `Werkzeug` security utilities for password hashing

### 8.3 Communication Interfaces
- HTTP on port 5000 (development) / HTTPS on port 443 (production)

---

## 9. Constraints & Assumptions

| # | Constraint / Assumption                                                                |
|---|----------------------------------------------------------------------------------------|
| C1 | Python 3.10+ must be pre-installed on the server.                                    |
| C2 | Sub-team members must use standard HTML/CSS/JS (no server-side code inside plugins). |
| C3 | All edition plugins must have `index.html` as the root entry file (Hard Collar).     |
| C4 | Cover images must be placed inside the edition's own directory.                       |
| C5 | The portal is an internal college tool; public internet exposure is optional.         |
| C6 | Git PR review is the change-management mechanism; no in-app file upload in v1.0.     |
| A1 | The college server supports Python and pip.                                           |
| A2 | At least one person with server access is designated as the Super-Admin.             |
| A3 | Sub-teams have access to the GitHub repository for PR submission.                    |

---

## 10. Glossary

| Term         | Meaning                                                                     |
|--------------|-----------------------------------------------------------------------------|
| Edition      | A single published magazine (one `index.html` tree)                         |
| Plugin       | Synonym for Edition in the micro-frontend context                           |
| Hard Collar  | Binding rule that every edition must expose `index.html` at its directory root |
| Annual       | The all-college annual magazine                                             |
| Departmental | A magazine published by a specific academic department                      |
| Bhavan       | A college hostel unit (1–5)                                                 |
| meta.json    | Mandatory metadata descriptor file for each edition                         |
| Super-Admin  | Highest privilege admin role                                                |

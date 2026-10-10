# 📚 College Unified Magazine Portal

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask_3.0%2B-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/Tests-19%2F19%20Passing-brightgreen?logo=pytest&logoColor=white)](#f-automated-testing-suite)
[![Architecture](https://img.shields.io/badge/Architecture-Host--Plugin%20Micro--Frontend-teal)](#-system-architecture)
[![Branch](https://img.shields.io/badge/Default_Branch-development-orange)](https://github.com/ShreyansDey/college-magazine-portal/tree/development)

A centralized, production-grade micro-frontend web platform engineered to aggregate, organize, and showcase all student publications across academic years—including **Annual College Magazines**, **Departmental Journals**, and **Bhavan (Hostel) Publications**.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
  - [The "Hard Collar" Contract](#the-hard-collar-contract)
  - [Zero-Database Dynamic Indexing](#zero-database-dynamic-indexing)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Documentation Suite](#-documentation-suite)
- [Quickstart & Complete Experience Guide](#-quickstart--complete-experience-guide)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Installation & Virtual Environment](#2-installation--virtual-environment)
  - [3. Environment Configuration](#3-environment-configuration)
  - [4. Creating Administrator Accounts (`manage.py`)](#4-creating-administrator-accounts-managepy)
  - [5. Launching the Portal Engine](#5-launching-the-portal-engine)
- [Experiencing Every Feature (Full Walkthrough)](#-experiencing-every-feature-full-walkthrough)
  - [A. Public Portal & Multi-Dimensional Discovery](#a-public-portal--multi-dimensional-discovery)
  - [B. Interactive Responsive Sandboxed Reader](#b-interactive-responsive-sandboxed-reader)
  - [C. Admin Dashboard, Uploads & Zip Ingestion](#c-admin-dashboard-uploads--zip-ingestion)
  - [D. Sub-Team Publishing & Validation CLI](#d-sub-team-publishing--validation-cli)
  - [E. REST API Reference & cURL Commands](#e-rest-api-reference--curl-commands)
  - [F. Automated Testing Suite](#f-automated-testing-suite)
- [Production Deployment](#-production-deployment)
- [Branching & Contribution Strategy](#-branching--contribution-strategy)
- [Implementation Roadmap](#-implementation-roadmap)
- [License](#-license)

---

## 🌟 Overview

Educational institutions publish dozens of magazines every academic year across departments, cultural committees, and student hostels. Historically, these exist as fragmented PDFs, disconnected microsites, or lost static files.

The **College Unified Magazine Portal** solves this fragmentation through an elegant **Host-Plugin (Micro-Frontend)** architecture:

- The **Core Host Application** provides browsing, multi-dimensional filtering, live search, access control, and an embedded responsive reader.
- Autonomous **Sub-Teams** (departments, editorial clubs, hostels) design and code their magazines independently with standard HTML, CSS, JavaScript, and media assets without modifying host codebase.
- Dynamic filesystem scanning and strict directory conventions eliminate the need for an external database for content discovery.

---

## ✨ Key Features

- **🏛️ Universal Multi-Session Showcase:** Browse publications across multiple academic years (`2024-2025`, `2025-2026`) with category filtering (All, Annual, Bhavans/Hostels, Departments) and live search.
- **📖 Sandboxed Responsive Reader:** Sandboxed `<iframe>` reader interface featuring mobile, tablet, and desktop viewport simulations, full-screen reading mode, external popout window, and expandable metadata drawer.
- **🔌 Micro-Frontend Plugin Engine:** Sub-teams develop isolated magazine microsites independently without interfering with host styling or logic.
- **⚡ Zero-Database In-Memory Discovery:** Lightning-fast filesystem auto-discovery with intelligent in-memory caching that indexes newly merged editions instantly via standardized `meta.json` manifests.
- **🔒 Hardened Admin Portal:** Session-based authentication with bcrypt hashing, CSRF protection, rate limiting, and an admin management dashboard for publishing and managing editions.
- **📦 Direct ZIP Upload & Extraction Engine:** Upload magazine editions directly from the Admin UI as ZIP archives with automatic structure inspection, path traversal protection, and instant index ingestion.
- **🛠️ Student Pre-Flight Validation CLI:** Built-in validation tool (`tools/validate_edition.py`) allowing sub-teams to test and verify their editions locally against the "Hard Collar" contract before submission.
- **🌐 Comprehensive REST API:** JSON API for retrieving editions, filtering by categories/years, and performing administrative index re-scanning.

---

## 💡 System Architecture

The host application is completely decoupled from individual magazine publications:

```text
+-------------------------------------------------------------------------+
|                  CORE HOST APPLICATION (Flask / Jinja2)                 |
|                                                                         |
|  +--------------------+  +----------------------+  +-----------------+  |
|  |  Public Showcase   |  |  Interactive Reader  |  |   Admin Panel   |  |
|  |  & Filter Engine   |  |  (Sandboxed Iframe)  |  |  & Management   |  |
|  +---------+----------+  +----------+-----------+  +--------+--------+  |
|            |                        |                       |           |
|            +-------------------+----+-----------------------+           |
|                                |                                        |
|                     [ Filesystem Scanner & Cache ]                      |
|                                |                                        |
+--------------------------------|----------------------------------------+
                                 | Dynamic Resolution
                                 v
+-------------------------------------------------------------------------+
|                    MAGAZINE PLUGINS (Micro-Frontends)                   |
|                                                                         |
|  magazines/                                                             |
|  ├── 2025-2026/                                                         |
|  │   ├── shraddha-bhavan/    --> [index.html + meta.json + assets/]     |
|  │   └── vidyamandira-annual/--> [index.html + meta.json + assets/]     |
|  └── 2024-2025/                                                         |
|      └── cse-chronicle/      --> [index.html + meta.json + assets/]     |
+-------------------------------------------------------------------------+
```

### The "Hard Collar" Contract

Every sub-team publication must adhere to the standardized directory contract:

1. **Mandatory Entry Point:** An `index.html` file must exist at the root of the edition directory.
2. **Standardized Manifest:** A valid `meta.json` file specifying `id`, `title`, `year`, `category`, `cover_image`, `description`, and contributor details.
3. **Asset Isolation:** All CSS, JS, fonts, and images must be referenced using **relative paths** (`./style.css`, `images/cover.jpg`).
4. **Security Isolation:** Editions run inside sandboxed iframes with strict Content Security Policy (`CSP`) headers preventing host DOM, session, or cookie compromise.

### Zero-Database Dynamic Indexing

The portal discovers editions directly from the filesystem layout:

- Structure: `magazines/<academic-year>/<slug>/`
- An in-memory cache is built at startup and updated dynamically when new editions are uploaded or re-scanned.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| **Backend** | Python 3.10+, Flask 3.0+ | Micro-framework, routing, template rendering, and security |
| **Frontend** | HTML5, CSS3, Vanilla ES6+ | High-performance responsive UI with zero heavy frontend framework bloat |
| **Authentication** | Flask Sessions + bcrypt | Secure password hashing, session tokens, and role-based permissions |
| **Security** | Flask-WTF, Flask-Limiter, CSP | CSRF validation, brute-force rate-limiting, and sandboxed iframes |
| **CLI & Tools** | Python Click / argparse | Management CLI (`manage.py`) & Validation script (`validate_edition.py`) |
| **Testing** | pytest, pytest-cov | Automated test suite verifying routes, auth, scanner, and API |
| **Production** | Gunicorn + Nginx + SSL | High-concurrency production serving and reverse proxy |

---

## 📂 Repository Structure

```text
college-magazine-portal/
├── admin_routes.py             # Admin panel endpoints, upload handler & dashboard
├── api_routes.py               # REST API endpoints (/api/editions, /api/years, etc.)
├── app.py                      # Flask application factory, public routing & error handlers
├── auth.py                     # Authentication logic, bcrypt password hashing & session management
├── config.py                   # Configuration classes & environment variable loading
├── manage.py                   # CLI administration utility (create-admin, list-admins, rescan)
├── scanner.py                  # Dynamic filesystem scanner, cache & contract validator
├── uploader.py                 # ZIP upload processing, safe unzipping & contract inspection
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment configuration
│
├── files/                      # Comprehensive Pre-Development Documentation Suite
│   ├── SRS.md                  # Software Requirements Specification
│   ├── PRD.md                  # Product Requirements Document
│   ├── ARCHITECTURE.md         # System Architecture & Diagrams
│   ├── API_DESIGN.md           # REST API Specifications & Schemas
│   ├── SECURITY.md             # Security Architecture & Auth Matrix
│   ├── DATA_DESIGN.md          # Metadata Specifications & Schemas
│   ├── UI_UX_GUIDELINES.md     # Design System & Styling Tokens
│   ├── TEST_PLAN.md            # Testing Strategy & QA Test Cases
│   ├── DEPLOYMENT_GUIDE.md     # Production Deployment & Operations
│   ├── CONTRIBUTING.md         # Sub-Team Contributor Guide
│   ├── RISK_REGISTER.md        # Risk Analysis & Mitigation
│   ├── PROJECT_CHARTER.md      # Scope, Objectives & Milestones
│   ├── ROADMAP.md              # Sprint Plan & Implementation Phases
│   └── README.md               # Documentation Inventory & Reading Order
│
├── magazines/                  # Micro-Frontend Editions Directory (Plugins)
│   └── 2025-2026/
│       └── shraddha-bhavan/    # Live verified student publication
│           ├── index.html      # Edition entry point
│           ├── meta.json       # Canonical metadata manifest
│           ├── style.css       # Edition styles
│           └── images/         # Edition images and assets
│
├── static/                     # Host Portal Static Assets
│   ├── css/                    # Host design tokens, reset, typography, layout & reader styles
│   └── js/                     # Client-side filtering, live search, drawer & reader viewport scripts
│
├── templates/                  # Host Portal Jinja2 Templates
│   ├── base.html               # Master layout with responsive navbar & footer
│   ├── index.html              # Homepage with hero, year switcher, categories & search
│   ├── annual.html             # Annual magazines dedicated gallery
│   ├── bhavans.html            # Bhavan / Hostel publications gallery
│   ├── departments.html        # Departmental journals gallery
│   ├── reader.html             # Sandboxed reader with viewport switcher & drawer
│   ├── 404.html & 500.html     # Custom branded error pages
│   └── admin/                  # Admin login & dashboard templates
│
├── tests/                      # Automated Test Suite (pytest)
│   ├── test_scanner.py         # Scanner unit tests & contract enforcement
│   ├── test_auth.py            # Password hashing, login & session tests
│   └── test_api.py             # Public & admin REST API endpoint tests
│
└── tools/                      # Developer & Contributor Utilities
    └── validate_edition.py     # Sub-team CLI pre-flight edition validation tool
```

---

## 📚 Documentation Suite

All foundational specifications and design artifacts are located in the [`files/`](files/) directory:

| Document | Focus Area | Link |
| --- | --- | --- |
| **Software Requirements Specification** | Complete functional, non-functional, and interface requirements | [`files/SRS.md`](files/SRS.md) |
| **Product Requirements Document** | User personas, feature breakdown, and MVP definitions | [`files/PRD.md`](files/PRD.md) |
| **Architecture Specification** | Host-Plugin micro-frontend design and data flow | [`files/ARCHITECTURE.md`](files/ARCHITECTURE.md) |
| **API Design** | REST API endpoints and payload schemas | [`files/API_DESIGN.md`](files/API_DESIGN.md) |
| **Security Architecture** | Authentication, CSRF, rate-limiting, and RBAC matrix | [`files/SECURITY.md`](files/SECURITY.md) |
| **Data Design** | Canonical `meta.json` schema and filesystem layout | [`files/DATA_DESIGN.md`](files/DATA_DESIGN.md) |
| **UI/UX Guidelines** | Color tokens, typography, reader container specs | [`files/UI_UX_GUIDELINES.md`](files/UI_UX_GUIDELINES.md) |
| **Test Plan** | Test cases, automated testing matrix, exit criteria | [`files/TEST_PLAN.md`](files/TEST_PLAN.md) |
| **Deployment Guide** | Nginx, Gunicorn, systemd, SSL, and monitoring | [`files/DEPLOYMENT_GUIDE.md`](files/DEPLOYMENT_GUIDE.md) |
| **Contributor Guide** | Sub-team workflow and hard collar compliance rules | [`files/CONTRIBUTING.md`](files/CONTRIBUTING.md) |
| **Risk Register** | Risk assessment and contingency planning | [`files/RISK_REGISTER.md`](files/RISK_REGISTER.md) |
| **Project Charter** | Goals, constraints, stakeholders, and timeline | [`files/PROJECT_CHARTER.md`](files/PROJECT_CHARTER.md) |
| **Development Roadmap** | 5-phase sprint plan and deliverables | [`files/ROADMAP.md`](files/ROADMAP.md) |

---

## 🚀 Quickstart & Complete Experience Guide

Follow these steps to run the portal locally and experience the full platform:

### 1. Prerequisites

- **Python:** 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.13, 3.14)
- **Git:** 2.30+
- **pip** package manager

### 2. Installation & Virtual Environment

Clone the repository and set up an isolated virtual environment:

```bash
# Clone repository
git clone https://github.com/ShreyansDey/college-magazine-portal.git
cd college-magazine-portal

# Checkout the development branch
git checkout development

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (Command Prompt):
.\venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate

# Upgrade pip and install all required dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```ini
# Core Configuration
FLASK_ENV=development
SECRET_KEY=super-secret-development-key-change-in-production

# Portal Directories
MAGAZINES_DIR=magazines
ADMINS_FILE=admins.json

# Security & Uploads
MAX_CONTENT_LENGTH=104857600  # 100 MB max zip upload
RATELIMIT_STORAGE_URL=memory://
```

### 4. Creating Administrator Accounts (`manage.py`)

The portal includes a dedicated CLI management utility (`manage.py`) to manage administrative credentials without needing a database:

```bash
# Create an admin account interactively:
python manage.py create-admin --username admin --role superadmin

# Or list all registered admin users:
python manage.py list-admins

# Trigger a manual filesystem scan:
python manage.py rescan
```

### 5. Launching the Portal Engine

Start the Flask development server:

```bash
python app.py
```

The server will initialize on:
👉 **`http://127.0.0.1:5000`**

---

## 🌟 Experiencing Every Feature (Full Walkthrough)

### A. Public Portal & Multi-Dimensional Discovery

1. Open your browser and navigate to `http://127.0.0.1:5000`.
2. **Academic Sessions:** Switch between academic years (e.g., `2024–2025` and `2025–2026`). The portal dynamically queries and displays publications matching that session.
3. **Category Tabs:** Filter instantly between **All Publications**, **Annual College Magazines**, **Departmental Journals**, and **Bhavan / Hostel Editions**.
4. **Live Search:** Type into the live search input (e.g., `shraddha`, `science`, `annual`) to see client-side instantaneous filtering.
5. **Dedicated Category Pages:** Visit `/annual`, `/departments`, and `/bhavans` for dedicated section galleries.

### B. Interactive Responsive Sandboxed Reader

Click on any magazine card or "Read Magazine" button (e.g., `http://127.0.0.1:5000/read/2025-2026/shraddha-bhavan`):

- **Responsive Viewport Switcher:** Use the top toolbar to switch between:
  - 🖥️ **Desktop Mode** (100% width)
  - 📱 **Tablet View** (768px simulation container)
  - 📲 **Mobile View** (375px simulation container)
- **Fullscreen Experience:** Click the Fullscreen button or toggle with `F11` for distraction-free reading.
- **External Window Popout:** Open the magazine directly in a dedicated tab.
- **Info Drawer:** Toggle the metadata drawer to view edition details, editors, publication date, and description.
- **Sandboxed Security:** The edition runs inside `<iframe sandbox="allow-scripts allow-same-origin allow-popups">` with Content Security Policy protecting the host platform.

### C. Admin Dashboard, Uploads & Zip Ingestion

1. Navigate to `http://127.0.0.1:5000/admin/login`.
2. Log in using the credentials created via `python manage.py create-admin`.
3. In the **Admin Dashboard** (`/admin/dashboard`):
   - **Live Metrics:** View total editions, active academic sessions, and category breakdown.
   - **Download Starter Kit:** Click **"Download Starter Kit"** to get a ready-to-use template ZIP containing `index.html`, `meta.json`, `style.css`, and folder scaffolding.
   - **Publish New Edition via ZIP:**
     1. Select Academic Year (e.g., `2025-2026`).
     2. Choose Category (`annual`, `bhavan`, `department`).
     3. Enter Edition Slug (e.g., `physics-journal`).
     4. Upload the ZIP file.
     5. The engine inspects the ZIP for `index.html`, verifies safe file paths, safely extracts it into `magazines/<year>/<slug>`, and automatically updates the live index!
   - **Rescan Filesystem:** Click the **"Rescan Editions"** button to force-refresh the cache anytime.

### D. Sub-Team Publishing & Validation CLI

Student teams build their magazines inside a single folder. Before submitting a PR or uploading, they run the automated pre-flight validator:

```bash
# Validate an edition folder locally:
python tools/validate_edition.py magazines/2025-2026/shraddha-bhavan
```

**Validator Checks Performed:**

- ✅ Validates that `index.html` exists at root.
- ✅ Validates that `meta.json` exists and contains mandatory fields (`title`, `year`, `category`).
- ✅ Validates relative asset referencing (no absolute `/` paths that break micro-frontend serving).
- ✅ Validates image files and cover art existence.

### E. REST API Reference & cURL Commands

The portal provides clean REST API endpoints for external integrations:

#### 1. Fetch all editions (with optional query parameters)

```bash
curl -X GET "http://127.0.0.1:5000/api/editions?year=2025-2026&category=bhavan"
```

#### 2. Fetch available academic years

```bash
curl -X GET "http://127.0.0.1:5000/api/years"
```

#### 3. Fetch all publication categories

```bash
curl -X GET "http://127.0.0.1:5000/api/categories"
```

#### 4. Trigger administrative index rescan (Requires Session Auth)

```bash
curl -X POST "http://127.0.0.1:5000/api/admin/rescan"
```

### F. Automated Testing Suite

The repository includes a comprehensive `pytest` suite testing all core modules:

```bash
# Run the complete test suite
pytest -v

# Or run using the virtual environment python:
python -m pytest tests/
```

**Current Test Matrix (19/19 Passing):**

- `tests/test_scanner.py`: Scanner discovery, cache invalidation, metadata parsing, sorting, and contract enforcement.
- `tests/test_auth.py`: Password hashing, admin validation, session authentication, and access control.
- `tests/test_api.py`: Public JSON endpoints, query parameter filtering, and admin API routes.

---

## 🚢 Production Deployment

For production deployment on Linux (Ubuntu/Debian) with Gunicorn and Nginx:

1. **Install Gunicorn:**

   ```bash
   pip install gunicorn
   ```

2. **Run Gunicorn WSGI Server:**

   ```bash
   gunicorn -w 4 -b 127.0.0.1:5000 "app:app"
   ```

3. **Sample Nginx Reverse Proxy Configuration:**

   ```nginx
   server {
       listen 80;
       server_name magazines.college.edu;

       client_max_body_size 100M;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static/ {
           alias /var/www/college-magazine-portal/static/;
           expires 30d;
           add_header Cache-Control "public, no-transform";
       }
   }
   ```

See [`files/DEPLOYMENT_GUIDE.md`](files/DEPLOYMENT_GUIDE.md) for complete production setup including systemd service files, SSL certification with Let's Encrypt, and log rotation.

---

## 🌿 Branching & Contribution Strategy

- **`development` (Default Branch):** Primary integration branch where active feature development and sub-team magazine submissions are reviewed and merged.
- **`main` / `production`:** Production-ready releases tagged with semantic versions.
- **Sub-Team Edition Branches:** `edition/<year>-<magazine-slug>` (e.g., `edition/2025-26-cse-journal`).

### Sub-Team Contribution Flow

1. Branch from `development`: `git checkout -b edition/2025-26-my-magazine`
2. Add your publication folder under `magazines/<academic-year>/<magazine-slug>/`
3. Validate locally: `python tools/validate_edition.py magazines/<academic-year>/<magazine-slug>`
4. Submit a Pull Request targeting `development`.

---

## 🗺️ Implementation Roadmap

- [x] **Phase 0:** Project Planning, Architecture & Comprehensive Documentation Suite
- [x] **Phase 1:** Core Portal Host Engine & Filesystem Dynamic Discovery
- [x] **Phase 2:** Responsive Showcase UI, Filtering & Sandboxed Reader Container
- [x] **Phase 3:** Admin Authentication & Management Dashboard (Uploads, Rescan, Starter Kit)
- [x] **Phase 4:** Sub-Team Validation CLI & Automated Test Suite (19/19 Tests Passing)
- [x] **Phase 5:** Production Hardening, Security Headers & Deployment Documentation

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

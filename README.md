# 📚 College Unified Magazine Portal

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask_3.0%2B-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Micro--Frontend-teal)](#-system-architecture)
[![Branch](https://img.shields.io/badge/Default_Branch-development-orange)](https://github.com/ShreyansDey/college-magazine-portal/tree/development)

A centralized, scalable micro-frontend web platform engineered to aggregate, organize, and showcase all student publications across academic years—including **Annual College Magazines**, **Departmental Journals**, and **Bhavan (Hostel) Magazines**.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
  - [The "Hard Collar" Contract](#the-hard-collar-contract)
  - [Zero-Database Design](#zero-database-design)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Documentation Suite](#-documentation-suite)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Running the Application](#running-the-application)
- [Sub-Team Publishing Workflow](#-sub-team-publishing-workflow)
- [Branching & Contribution Strategy](#-branching--contribution-strategy)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🌟 Overview

Institutions publish multiple magazines every academic year across departments, clubs, and hostels. Traditionally, these exist as fragmented PDFs, disconnected microsites, or outdated static pages.

The **College Unified Magazine Portal** solves this fragmentation through a **Host-Plugin (Micro-Frontend)** architecture:
- The **Core Host Application** handles browsing, discovery, search, filtering, access control, and universal embedded reading.
- Independent **Sub-Teams** (departments, editorial clubs, hostels) design and build their magazines autonomously using standard web technologies (HTML, CSS, JS, assets) without touching host code.
- Dynamic filesystem scanning and strict directory conventions eliminate the need for an external database for content discovery.

---

## ✨ Key Features

- **🏛️ Universal Publication Directory:** Multi-dimensional filtering by academic year, category (Annual, Departmental, Hostel), and search by title or tag.
- **📖 Embedded Responsive Reader:** Sandboxed `<iframe>` reader interface offering full-screen reading, responsive viewport switching, metadata drawer, and direct external sharing links.
- **🔌 Micro-Frontend Plugin Engine:** Sub-teams develop their own custom magazine microsites independently within isolated folders.
- **⚡ Zero-Database Content Indexing:** In-memory caching and filesystem auto-discovery dynamically indexes newly merged editions instantly via standardized `meta.json` manifests.
- **🔒 Secure Admin Portal:** Session-based authentication with bcrypt hashing, CSRF protection, and rate limiting for managing featured editions and reloading cached manifests.
- **🛡️ Sandboxed Content Delivery:** Sandboxed iframe attributes and strict routing security prevent sub-team code from compromising the host application.

---

## 💡 System Architecture

The system decouples the core host portal from individual magazine publications:

```
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
|  │   ├── cse-aura/           --> [index.html + meta.json + assets/]     |
|  │   └── college-annual/     --> [index.html + meta.json + assets/]     |
|  └── 2024-2025/                                                         |
|      └── hostel-vibes/       --> [index.html + meta.json + assets/]     |
+-------------------------------------------------------------------------+
```

### The "Hard Collar" Contract

Every sub-team must adhere to the standardized directory contract:

1. **Entry Point:** Every magazine must provide an `index.html` at its root directory.
2. **Metadata Manifest:** A valid `meta.json` file specifying title, year, category, department, cover image, and description.
3. **Asset Isolation:** All assets (CSS, JS, images, fonts) must be referenced via relative paths within the edition folder.
4. **No External Host Coupling:** Sub-team code must never attempt to access or modify host DOM, cookies, or sessions.

### Zero-Database Design

The portal reads metadata directly from the filesystem hierarchy:
- Primary storage: `magazines/<academic-year>/<slug>/meta.json`
- In-memory index built on startup and refreshed on demand or via admin webhook.
- Content updates occur cleanly via Git Pull Requests.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Python 3.10+, Flask 3.0+ | Server-side routing, discovery engine, template rendering |
| **Frontend** | HTML5, Modern CSS, Vanilla JS | High-performance host UI with zero heavy framework overhead |
| **Micro-Frontends** | Standard HTML / CSS / JS | Pluggable, autonomous sub-team magazine editions |
| **Authentication** | Flask Sessions + bcrypt | Protected admin panel with secure password hashing |
| **Security** | Flask-WTF, Flask-Limiter | CSRF validation, brute-force rate-limiting, sandboxing |
| **Production** | Gunicorn + Nginx + SSL | High-concurrency production serving and reverse proxy |

---

## 📂 Repository Structure

```
college-magazine-portal/
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
├── magazines/                  # Micro-Frontend Editions Directory (Plugins)
│   └── [academic-year]/
│       └── [magazine-slug]/
│           ├── index.html      # Mandatory entry point
│           ├── meta.json       # Canonical metadata file
│           └── assets/         # Edition-specific styles, scripts & media
├── static/                     # Host Portal Static Assets (CSS, JS, Logos)
├── templates/                  # Host Portal Jinja2 Templates
├── app.py                      # Flask Application Entry Point
├── config.py                   # Configuration & Environment Variables
├── requirements.txt            # Python Dependencies
├── .gitignore                  # Git Ignore Rules
└── README.md                   # Repository Overview (This File)
```

---

## 📚 Documentation Suite

All foundational specifications and design artifacts are located in the [`files/`](files/) directory:

| Document | Focus Area | Link |
|---|---|---|
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

## 🚀 Getting Started

### Prerequisites

- **Python:** 3.10 or higher
- **Git:** 2.30 or higher
- **pip** package manager

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ShreyansDey/college-magazine-portal.git
   cd college-magazine-portal
   ```

2. **Switch to the development branch:**
   ```bash
   git checkout development
   ```

3. **Create and activate a virtual environment:**
   ```bash
   # On Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
# Start the Flask development server
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## ✍️ Sub-Team Publishing Workflow

Department and hostel editorial teams publish new magazine editions via Git:

1. **Create an edition branch:**
   ```bash
   git checkout -b feature/cse-journal-2025-26
   ```
2. **Add your magazine directory:**
   ```
   magazines/2025-2026/cse-aura/
   ├── index.html
   ├── meta.json
   └── assets/
   ```
3. **Validate metadata and paths:** Ensure all links are relative and `meta.json` adheres to the specification in [`files/DATA_DESIGN.md`](files/DATA_DESIGN.md).
4. **Open a Pull Request:** Target the **`development`** branch for review and automated contract checks.

---

## 🌿 Branching & Contribution Strategy

- **`development` (Default Branch):** Primary integration branch where active feature development and magazine submissions are reviewed and merged.
- **`main` / `production`:** Production-ready releases tagged with semantic versions.
- **Feature Branches:** `feature/<feature-name>` or `edition/<year>-<magazine-name>`.

---

## 🗺️ Roadmap

- [x] **Phase 0:** Project Planning, Architecture & Comprehensive Documentation Suite
- [ ] **Phase 1:** Core Portal Host Engine & Filesystem Discovery
- [ ] **Phase 2:** Responsive Showcase UI, Filtering & Sandboxed Reader Container
- [ ] **Phase 3:** Admin Authentication & Management Dashboard
- [ ] **Phase 4:** Sub-Team Validation CLI & Automated PR Checks
- [ ] **Phase 5:** Production Hardening, Nginx Reverse Proxy & Deployment

See [`files/ROADMAP.md`](files/ROADMAP.md) for full phase details and task assignments.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

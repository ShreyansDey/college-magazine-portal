# System Architecture Document (SAD)

## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Draft                         |
| **Date**            | 2026-10-07                    |

---

## 1. Architecture Overview

The College Unified Magazine Portal is built on a **Micro-Frontend (MFE) Plugin Architecture** hosted by a lightweight Python Flask backend. The system is designed to be filesystem-driven, requiring no relational database for its core operation.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                           │
│  ┌───────────────────┐       ┌─────────────────────────────┐   │
│  │  Portal UI        │       │  <iframe> Reader Pane        │   │
│  │  (templates/      │       │  Loads: /static/magazines/  │   │
│  │   index.html)     │       │  <year>/<cat>/<id>/index.html│  │
│  └────────┬──────────┘       └──────────────┬──────────────┘   │
│           │ Fetch API                        │ HTTP GET         │
└───────────┼──────────────────────────────────┼──────────────────┘
            │                                  │
┌───────────▼──────────────────────────────────▼──────────────────┐
│                     FLASK APPLICATION (app.py)                   │
│                                                                  │
│  ┌──────────────────┐  ┌────────────────┐  ┌─────────────────┐ │
│  │  Scanner Module  │  │  REST API       │  │  Admin Routes   │ │
│  │  - Walks dirs    │  │  GET /api/      │  │  /admin/*       │ │
│  │  - Reads meta.json│ │    editions     │  │  (Auth-gated)   │ │
│  │  - Builds index  │  │  POST /api/     │  │                 │ │
│  └────────┬─────────┘  │    admin/rescan│  └────────┬────────┘ │
│           │            └────────────────┘           │          │
│           └─────────────┐                ┌──────────┘          │
│                 ┌───────▼────────────────▼──────┐              │
│                 │    In-Memory Edition Index     │              │
│                 └───────────────────────────────┘              │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────▼───────────────┐
              │        FILESYSTEM              │
              │                               │
              │  static/magazines/            │
              │  └── <YEAR>/                  │
              │      ├── annual/              │
              │      │   ├── index.html       │
              │      │   └── meta.json        │
              │      ├── departmental/        │
              │      │   └── <dept_id>/       │
              │      │       ├── index.html   │
              │      │       └── meta.json    │
              │      └── bhavan/              │
              │          └── <bhavan_id>/     │
              │              ├── index.html   │
              │              └── meta.json    │
              └───────────────────────────────┘
```

---

## 2. Component Descriptions

### 2.1 Flask Application (`app.py`)

| Sub-Component       | Responsibility                                                         |
|---------------------|------------------------------------------------------------------------|
| **Scanner Module**  | Walks `static/magazines/`, validates `meta.json`, builds edition index |
| **REST API**        | Exposes `/api/editions` (public) and `/api/admin/*` (protected)       |
| **Admin Routes**    | Serves admin dashboard; RBAC-protected via session                    |
| **Static Server**   | Serves all files under `/static/` including magazine plugins          |
| **Template Renderer** | Renders `templates/index.html` with Jinja2                          |

### 2.2 Frontend Portal (`templates/index.html` + `static/js/portal.js`)

| Sub-Component       | Responsibility                                                         |
|---------------------|------------------------------------------------------------------------|
| **Edition Grid**    | Fetches `/api/editions` and renders edition cards dynamically         |
| **Filter UI**       | Year, category, department, and bhavan filter controls                |
| **iframe Reader**   | Loads selected edition at `/static/magazines/<year>/<cat>/<id>/index.html` |
| **Search Module**   | Client-side filtering of the fetched edition list                     |

### 2.3 Magazine Plugin (Sub-Team Deliverable)

| Property            | Value                                                                  |
|---------------------|------------------------------------------------------------------------|
| **Entry Point**     | `index.html` (mandatory — Hard Collar Contract)                       |
| **Technology**      | Standard HTML, CSS, JavaScript (no server-side code)                 |
| **Isolation**       | Self-contained; must not reference assets from other plugins          |
| **Metadata File**   | `meta.json` at directory root (required for discovery)               |
| **Max Size**        | 50 MB per edition (uncompressed)                                      |

### 2.4 Data Layer (Filesystem + meta.json)

No relational database is used. All persistent metadata lives in `meta.json` files co-located with each edition. The in-memory index is rebuilt on startup and on admin-triggered rescan.

---

## 3. Directory Structure

```
college-magazine-portal/
│
├── app.py                      # Flask app: routes, scanner, admin
├── .env                        # Secrets (NOT committed to git)
├── .env.example                # Template for .env
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
│
├── templates/
│   ├── index.html              # Public portal UI
│   ├── admin/
│   │   ├── login.html          # Admin login page
│   │   ├── dashboard.html      # Edition management
│   │   └── accounts.html       # Admin account management (Super-Admin)
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
├── static/
│   ├── css/
│   │   └── style.css           # Global portal styles
│   ├── js/
│   │   └── portal.js           # Frontend logic, Fetch API calls
│   ├── images/
│   │   └── logo.png            # College logo and portal assets
│   │
│   └── magazines/              # Plugin repository root
│       ├── TEMPLATE/           # Starter template for sub-teams
│       │   ├── index.html
│       │   └── meta.json
│       └── 2026/
│           ├── annual/
│           │   ├── index.html
│           │   └── meta.json
│           ├── departmental/
│           │   ├── cs/
│           │   │   ├── index.html
│           │   │   └── meta.json
│           │   └── physics/
│           │       ├── index.html
│           │       └── meta.json
│           └── bhavan/
│               ├── bhavan1/
│               │   ├── index.html
│               │   └── meta.json
│               └── ... (bhavan2 through bhavan5)
│
├── files/                      # Project documentation
│   ├── SRS.md
│   ├── PRD.md
│   ├── ARCHITECTURE.md         # This document
│   ├── API_DESIGN.md
│   ├── SECURITY.md
│   ├── TEST_PLAN.md
│   ├── RISK_REGISTER.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── UI_UX_GUIDELINES.md
│
└── .gitignore
```

---

## 4. Technology Stack

| Layer          | Technology              | Rationale                                              |
|----------------|-------------------------|--------------------------------------------------------|
| Backend        | Python 3.10+ / Flask 3  | Lightweight, minimal setup, excellent static file serving |
| Templating     | Jinja2 (built into Flask) | Simple, secure HTML rendering                        |
| Frontend       | HTML5, Vanilla CSS, Vanilla JS | Maximum compatibility, no build tools needed  |
| Data Storage   | Filesystem + JSON       | Zero external dependencies; works on any OS           |
| Auth           | Flask sessions + bcrypt | Secure, stateless sessions with hashed passwords      |
| CSRF           | Flask-WTF               | Industry-standard CSRF protection for Flask           |
| Rate Limiting  | Flask-Limiter           | Protect login endpoint from brute force               |
| Process Manager| Gunicorn (production)   | WSGI-compatible, handles concurrent requests          |
| Reverse Proxy  | Nginx (production)      | SSL termination, static file acceleration             |

---

## 5. Request Flow Diagrams

### 5.1 Public Visitor — Read an Edition

```
Visitor Opens Portal
      │
      ▼
GET / → Flask renders templates/index.html
      │
      ▼
Browser JS → GET /api/editions
      │
      ▼
Flask Scanner returns JSON list of published editions
      │
      ▼
Browser renders edition cards
      │
Visitor clicks "Read"
      │
      ▼
Browser sets iframe.src = /static/magazines/<year>/<cat>/<id>/index.html
      │
      ▼
Flask serves static file → Browser renders magazine inside iframe
```

### 5.2 Admin — Publish an Edition

```
Admin navigates to /admin/dashboard
      │
      ▼
Flask checks session → Valid → Render dashboard.html
      │
Admin clicks "Publish" on an edition
      │
      ▼
POST /api/admin/editions/<id>/publish  [CSRF token included]
      │
      ▼
Flask validates session + CSRF token
      │
      ▼
Flask updates meta.json: published = true
      │
      ▼
Flask triggers in-memory re-index
      │
      ▼
Returns 200 OK → Dashboard updates UI
```

---

## 6. Micro-Frontend Contract (Hard Collar)

Every sub-team MUST comply with the following:

### 6.1 Directory Convention

```
static/magazines/<YEAR>/<CATEGORY>/<SUB_ID>/
    ├── index.html          ← REQUIRED (Hard Collar entry point)
    ├── meta.json           ← REQUIRED (discovery metadata)
    └── <any other assets>  ← Optional (images, CSS, JS, fonts)
```

### 6.2 Path Variables

| Variable    | Format             | Example         |
|-------------|-------------------|-----------------|
| `YEAR`      | 4-digit integer   | `2026`          |
| `CATEGORY`  | `annual` / `departmental` / `bhavan` | `departmental` |
| `SUB_ID`    | lowercase, hyphens OK | `cs`, `bhavan1`, `physics` |

### 6.3 Asset Referencing

All asset paths inside the plugin MUST be **relative**, not absolute:

- ✅ `<img src="images/cover.jpg">`
- ❌ `<img src="/images/cover.jpg">`

---

## 7. Security Architecture

> Full details in `SECURITY.md`.

| Layer              | Control                                                           |
|--------------------|-------------------------------------------------------------------|
| Transport          | HTTPS enforced in production via Nginx + SSL certificate         |
| Authentication     | Session-based with bcrypt password hashing                       |
| Authorization      | Route decorators check session role before serving admin pages   |
| CSRF               | Flask-WTF CSRF token validated on every state-changing request   |
| Rate Limiting      | Flask-Limiter on `/admin/login`: 5 requests / 15 minutes / IP   |
| Input Validation   | All meta.json fields validated against schema on scan            |
| Path Traversal     | Scanner uses `os.path.realpath()` and validates within allowed root |
| HTTP Headers       | CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy |

---

## 8. Deployment Architecture (Production)

```
Internet
    │
    ▼
┌───────────────────────┐
│      Nginx             │  ← SSL termination, static file acceleration
│  (Reverse Proxy)       │  ← Serves /static/* directly (bypasses Flask)
└───────────┬───────────┘
            │ Proxy pass (non-static)
            ▼
┌───────────────────────┐
│      Gunicorn          │  ← WSGI server, multiple workers
│  (WSGI Server)        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Flask Application   │  ← Business logic, API, admin
│      (app.py)         │
└───────────────────────┘
```

---

## 9. Scalability Considerations

| Concern                    | Current Approach (v1.0)       | Future Approach (v2.0)              |
|----------------------------|-------------------------------|-------------------------------------|
| Edition count              | In-memory JSON index          | Redis cache or SQLite for > 500 editions |
| Concurrent visitors        | Gunicorn multi-worker         | Horizontal scaling with load balancer |
| File storage               | Local filesystem              | Cloud Storage (S3 / GCS) with CDN   |
| Admin state persistence    | meta.json on disk             | SQLite admin database               |

---

## 10. Architecture Decision Records (ADR)

### ADR-001: No Database for Core Operation

**Decision:** Use `meta.json` files instead of a relational database.
**Rationale:** Simplifies setup (no DB install required), fits the Git PR workflow naturally, and is sufficient for the expected data volume (<500 editions in 10 years).
**Trade-off:** Admin writes to disk (not atomic); acceptable at this scale.

### ADR-002: iframe for Edition Embedding

**Decision:** Use `<iframe>` to embed sub-team editions.
**Rationale:** Perfect isolation — sub-team code cannot affect the portal. Simple implementation. No build step needed.
**Trade-off:** Some browser security restrictions (CORS, CSP) must be carefully configured.

### ADR-003: Flask over Django

**Decision:** Use Flask instead of Django.
**Rationale:** Lower overhead. The system doesn't need Django's ORM, admin, or auth modules — those are built custom. Flask is easier for student maintainers.

### ADR-004: Filesystem Scanner over Git API

**Decision:** Scan the local filesystem, not query the GitHub API.
**Rationale:** Works in offline/intranet environments. No API rate limits. Simpler code.

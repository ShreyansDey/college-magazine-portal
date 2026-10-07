# Development Roadmap & Sprint Plan
## College Unified Magazine Portal — v1.0

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Active                        |
| **Date**            | 2026-10-07                    |

---

## Phase 1 — Foundation (Week 1–2)

### Goals
- Repository scaffolded
- All documentation complete
- Backend scanner and API working
- Starter template for sub-teams

### Tasks

| ID    | Task                                                    | Owner          | Priority |
|-------|---------------------------------------------------------|----------------|----------|
| T-001 | Set up Git repository with branch protection rules      | Project Lead   | MUST     |
| T-002 | Create base directory structure as per ARCHITECTURE.md  | Backend Dev    | MUST     |
| T-003 | Write `app.py` skeleton with Flask routes               | Backend Dev    | MUST     |
| T-004 | Implement filesystem scanner module                     | Backend Dev    | MUST     |
| T-005 | Implement `meta.json` schema validator                  | Backend Dev    | MUST     |
| T-006 | Implement `GET /api/editions` endpoint                  | Backend Dev    | MUST     |
| T-007 | Implement `GET /api/years` and `/api/categories`        | Backend Dev    | MUST     |
| T-008 | Create `requirements.txt` with all dependencies         | Backend Dev    | MUST     |
| T-009 | Create `.env.example` file                              | Backend Dev    | MUST     |
| T-010 | Create `TEMPLATE/` starter edition directory            | Backend Dev    | MUST     |
| T-011 | Add `validate_edition.py` helper script in `tools/`     | Backend Dev    | SHOULD   |
| T-012 | Write pre-commit hook that rejects missing `meta.json`  | Backend Dev    | SHOULD   |

**Exit Criteria:** `GET /api/editions` returns correct data for test fixtures.

---

## Phase 2 — Public Portal UI (Week 3–4)

### Goals
- Landing page fully functional
- Edition cards, filters, and iframe reader working
- Responsive on all devices

### Tasks

| ID    | Task                                                    | Owner          | Priority |
|-------|---------------------------------------------------------|----------------|----------|
| T-020 | Create `style.css` with design system (tokens, grid, typography) | Frontend Dev | MUST |
| T-021 | Build landing page HTML structure (`templates/index.html`) | Frontend Dev | MUST |
| T-022 | Build edition card component (cover, title, badge, button) | Frontend Dev | MUST |
| T-023 | Implement `portal.js`: fetch `/api/editions` and render cards | Frontend Dev | MUST |
| T-024 | Implement category tab filter (Annual / Departmental / Bhavan) | Frontend Dev | MUST |
| T-025 | Implement year dropdown filter                          | Frontend Dev  | MUST     |
| T-026 | Implement department/bhavan sub-filter                  | Frontend Dev  | MUST     |
| T-027 | Build iframe reader pane with title bar, close, fullscreen | Frontend Dev | MUST   |
| T-028 | Add iframe loading spinner / skeleton loader            | Frontend Dev  | SHOULD   |
| T-029 | Implement client-side search bar                        | Frontend Dev  | SHOULD   |
| T-030 | Implement card appear animations (staggered fade-in)    | Frontend Dev  | SHOULD   |
| T-031 | Implement responsive layout (mobile, tablet, desktop)   | Frontend Dev  | MUST     |
| T-032 | Add empty state component ("No editions yet")           | Frontend Dev  | MUST     |
| T-033 | Add college header (logo, name, nav)                    | Frontend Dev  | MUST     |
| T-034 | Add footer with college info and year                   | Frontend Dev  | MUST     |

**Exit Criteria:** Visitor can browse, filter, and read test editions in iframe; responsive on Chrome mobile emulation.

---

## Phase 3 — Admin Dashboard (Week 5)

### Goals
- Admin login and session management working
- Dashboard shows all editions with publish controls
- Metadata edit form functional

### Tasks

| ID    | Task                                                    | Owner          | Priority |
|-------|---------------------------------------------------------|----------------|----------|
| T-040 | Set up Flask session management with `SECRET_KEY`       | Backend Dev    | MUST     |
| T-041 | Implement `manage.py create-admin` CLI command          | Backend Dev    | MUST     |
| T-042 | Build admin login page (`templates/admin/login.html`)   | Frontend Dev   | MUST     |
| T-043 | Implement `POST /admin/login` with bcrypt verification  | Backend Dev    | MUST     |
| T-044 | Implement `POST /admin/logout`                          | Backend Dev    | MUST     |
| T-045 | Add `@login_required` and `@super_admin_required` decorators | Backend Dev | MUST  |
| T-046 | Build admin dashboard HTML (`templates/admin/dashboard.html`) | Frontend Dev | MUST |
| T-047 | Implement `GET /api/admin/editions` (all editions)      | Backend Dev    | MUST     |
| T-048 | Implement `PATCH /api/admin/editions/:id` (update metadata) | Backend Dev | MUST  |
| T-049 | Implement `POST /api/admin/rescan` endpoint             | Backend Dev    | SHOULD   |
| T-050 | Build account management page (Super-Admin only)        | Frontend Dev   | MUST     |
| T-051 | Implement `GET/POST/DELETE /api/admin/accounts`         | Backend Dev    | MUST     |
| T-052 | Add dashboard publish/unpublish toggle with live update | Frontend Dev   | MUST     |
| T-053 | Add metadata edit modal/form in dashboard               | Frontend Dev   | MUST     |

**Exit Criteria:** Admin can log in, publish/unpublish editions, and edit metadata without server restart.

---

## Phase 4 — Security Hardening (Week 6)

### Goals
- All security requirements from SECURITY.md implemented
- Pre-launch security checklist 100% complete

### Tasks

| ID    | Task                                                    | Owner          | Priority |
|-------|---------------------------------------------------------|----------------|----------|
| T-060 | Integrate Flask-WTF CSRF protection on all admin forms  | Backend Dev    | MUST     |
| T-061 | Add CSRF token to all admin JS Fetch calls              | Frontend Dev   | MUST     |
| T-062 | Configure Flask-Limiter on `/admin/login` (5/15min)     | Backend Dev    | MUST     |
| T-063 | Add `@app.after_request` hook for all security headers  | Backend Dev    | MUST     |
| T-064 | Configure Content Security Policy (CSP) header          | Backend Dev    | MUST     |
| T-065 | Implement `is_safe_path()` in scanner for path traversal | Backend Dev   | MUST     |
| T-066 | Add `sandbox` attribute to iframe reader               | Frontend Dev   | MUST     |
| T-067 | Set session cookie flags: HttpOnly, Secure, SameSite   | Backend Dev    | MUST     |
| T-068 | Verify `.env` and `data/admins.json` are in `.gitignore` | All           | MUST     |
| T-069 | Test: 6th login attempt returns 429                     | QA             | MUST     |
| T-070 | Test: CSRF-less PATCH returns 400                       | QA             | MUST     |
| T-071 | Test: `/api/admin/editions` without session returns 401 | QA             | MUST     |
| T-072 | Run `SECURITY.md` pre-launch checklist; sign off       | Security Lead  | MUST     |

**Exit Criteria:** All 12 items in SECURITY.md pre-launch checklist pass.

---

## Phase 5 — Testing & Launch (Week 7)

### Goals
- All unit and integration tests pass
- Performance meets thresholds
- Production deployed
- Sub-teams have submitted their editions

### Tasks

| ID    | Task                                                    | Owner          | Priority |
|-------|---------------------------------------------------------|----------------|----------|
| T-080 | Write unit tests for scanner module (`tests/test_scanner.py`) | Backend Dev | MUST  |
| T-081 | Write unit tests for auth module (`tests/test_auth.py`) | Backend Dev    | MUST     |
| T-082 | Write API integration tests (`tests/test_api.py`)       | Backend Dev    | MUST     |
| T-083 | Create test fixture set (`tests/fixtures/magazines/`)   | Backend Dev    | MUST     |
| T-084 | Cross-browser UI testing (Chrome, Firefox, Edge)        | QA             | MUST     |
| T-085 | Mobile responsive testing (320px, 768px, 1024px)        | QA             | MUST     |
| T-086 | Accessibility check with WAVE tool                      | QA             | MUST     |
| T-087 | Performance test: 200 concurrent users with Locust      | Dev            | SHOULD   |
| T-088 | Set up production server (install Python, Nginx, etc.)  | DevOps         | MUST     |
| T-089 | Deploy application with Gunicorn + systemd              | DevOps         | MUST     |
| T-090 | Configure Nginx reverse proxy                           | DevOps         | MUST     |
| T-091 | Set up HTTPS with Let's Encrypt Certbot                 | DevOps         | MUST     |
| T-092 | Send CONTRIBUTING.md to all sub-teams; set PR deadline  | Project Lead   | MUST     |
| T-093 | Review and merge all sub-team PRs                       | Admin          | MUST     |
| T-094 | Publish editions via admin dashboard                    | Admin          | MUST     |
| T-095 | Announce launch to college                              | Project Lead   | MUST     |

**Exit Criteria:** Portal live, at least 3 editions published across all 3 categories, security checklist signed off.

---

## Post-Launch (Week 8–10)

| Task                                                    | Owner          |
|---------------------------------------------------------|----------------|
| Monitor error logs for 1 week post-launch               | DevOps         |
| Collect feedback from students and faculty              | Project Lead   |
| Fix any critical/high bugs from feedback                | Dev Team       |
| Document lessons learned                                | All            |
| Plan v1.1 features (search, fullscreen, analytics)      | Project Lead   |

---

## Backlog (v1.1+)

| Feature                               | Version |
|---------------------------------------|---------|
| Full-text search across editions      | v1.1    |
| Fullscreen iframe toggle              | v1.1    |
| Downloadable edition starter ZIP      | v1.1    |
| Breadcrumb navigation in reader       | v1.1    |
| Analytics (view counts per edition)   | v2.0    |
| Social share buttons                  | v2.0    |
| Dark mode toggle                      | v2.0    |
| Email notifications on PR merge       | v2.0    |
| SQLite migration for data layer       | v2.0    |

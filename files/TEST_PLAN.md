# Test Plan
## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Draft                         |
| **Date**            | 2026-10-07                    |

---

## 1. Testing Objectives

- Verify all functional requirements in the SRS are met.
- Confirm the system is secure against common web vulnerabilities.
- Validate performance under expected and peak load.
- Ensure a smooth experience on all target browsers and screen sizes.

---

## 2. Scope

### In Scope
- Flask backend (scanner, API endpoints, admin routes)
- Public portal UI (landing page, filters, iframe reader)
- Admin dashboard (login, edition management, RBAC)
- Security controls (CSRF, rate limiting, headers, path traversal)
- Responsive behavior (mobile, tablet, desktop)
- Error handling and graceful degradation

### Out of Scope
- Internal content of sub-team magazine plugins (sub-team responsibility)
- Third-party library internals
- Browser developer tools usage

---

## 3. Test Types & Strategy

| Test Type         | Tool / Method                        | Who Runs It           |
|-------------------|--------------------------------------|------------------------|
| Unit Tests        | `pytest` + `unittest.mock`           | Core Dev Team          |
| Integration Tests | `pytest` + Flask test client         | Core Dev Team          |
| API Tests         | `pytest` / Postman / Insomnia        | Core Dev Team / QA     |
| Security Tests    | Manual checklist + OWASP ZAP (basic) | Security-aware Dev     |
| UI Tests          | Manual + browser DevTools            | QA / Any team member   |
| Performance Tests | `locust` or `wrk`                    | Core Dev (before launch)|
| Cross-browser     | Chrome, Firefox, Edge, Safari (manual) | QA                   |
| Responsive        | Browser DevTools device emulation    | QA                     |
| Accessibility     | WAVE browser extension               | QA                     |

---

## 4. Unit Tests

### 4.1 Scanner Module

| Test ID    | Test Case                                                           | Expected Result                              |
|------------|---------------------------------------------------------------------|----------------------------------------------|
| UT-SCAN-01 | Scanner finds valid edition directory with meta.json               | Edition added to index                       |
| UT-SCAN-02 | Scanner skips directory without meta.json                          | Warning logged; directory skipped           |
| UT-SCAN-03 | Scanner skips edition with `published: false`                      | Not included in public feed                  |
| UT-SCAN-04 | Scanner rejects meta.json with missing required field (`title`)    | Error logged; edition skipped               |
| UT-SCAN-05 | Scanner rejects meta.json with invalid category value              | Error logged; edition skipped               |
| UT-SCAN-06 | Scanner detects path traversal attempt (`../../etc/passwd`)        | Path rejected; warning logged               |
| UT-SCAN-07 | Scanner correctly parses year from directory name                  | `year` field matches directory               |
| UT-SCAN-08 | Scanner builds correct `path` URL for each edition                 | Path matches `/static/magazines/<year>/...` |

### 4.2 Authentication Module

| Test ID    | Test Case                                                           | Expected Result                              |
|------------|---------------------------------------------------------------------|----------------------------------------------|
| UT-AUTH-01 | Login with correct credentials                                      | Session created; redirect to dashboard       |
| UT-AUTH-02 | Login with wrong password                                           | Generic error returned; no session created   |
| UT-AUTH-03 | Login with non-existent username                                    | Same generic error (no hint which field)     |
| UT-AUTH-04 | Password hash verification using bcrypt                            | Correct comparison result                    |
| UT-AUTH-05 | Session expiry after 60 minutes                                     | Session invalid; redirect to login           |
| UT-AUTH-06 | Accessing `/admin/dashboard` without session                       | Redirect to `/admin/login`                   |
| UT-AUTH-07 | Accessing `/api/admin/accounts` with admin (not super-admin) role  | 403 Forbidden                                |
| UT-AUTH-08 | Super-admin accessing `/api/admin/accounts`                        | 200 OK with account list                     |

### 4.3 API Module

| Test ID    | Test Case                                                           | Expected Result                              |
|------------|---------------------------------------------------------------------|----------------------------------------------|
| UT-API-01  | `GET /api/editions` returns only published editions                 | `published: true` for all items             |
| UT-API-02  | `GET /api/editions?year=2026` filters by year                      | Only 2026 editions returned                  |
| UT-API-03  | `GET /api/editions?category=invalid` returns 400                   | HTTP 400 with error message                  |
| UT-API-04  | `GET /api/editions/:id` with valid published ID                    | HTTP 200 with edition data                   |
| UT-API-05  | `GET /api/editions/:id` with non-existent ID                       | HTTP 404                                     |
| UT-API-06  | `GET /api/editions/:id` for an unpublished edition (public)        | HTTP 404 (not visible publicly)              |
| UT-API-07  | `GET /api/years` returns sorted descending list                    | `[2026, 2025]`                              |
| UT-API-08  | `PATCH /api/admin/editions/:id` without CSRF token                 | HTTP 400 CSRF validation failure             |
| UT-API-09  | `POST /api/admin/rescan` updates in-memory index                   | New edition appears in subsequent GET        |

---

## 5. Integration Tests

| Test ID    | Test Case                                                           | Expected Result                              |
|------------|---------------------------------------------------------------------|----------------------------------------------|
| IT-01      | Full scan → API → UI flow with 3 test editions                     | All 3 appear in `/api/editions`             |
| IT-02      | Admin login → publish edition → verify appears in public API       | Edition visible after publish                |
| IT-03      | Admin login → unpublish → verify absent from public API            | Edition hidden after unpublish               |
| IT-04      | Admin login → edit title → verify meta.json updated on disk        | File reflects new title                      |
| IT-05      | Add new edition directory while server running → rescan → appears  | Rescan picks up new edition                  |
| IT-06      | Malformed meta.json does not crash the scanner                     | Server continues running; error logged       |

---

## 6. Security Tests

| Test ID    | Test Case                                                           | Expected Result                              |
|------------|---------------------------------------------------------------------|----------------------------------------------|
| SEC-T-01   | Submit login form 6 times in 15 minutes                            | 6th attempt returns HTTP 429                 |
| SEC-T-02   | Submit PATCH request without CSRF token                            | HTTP 400 rejected                            |
| SEC-T-03   | Check all admin pages for `HttpOnly` session cookie flag           | Flag present                                 |
| SEC-T-04   | Check `Secure` flag on session cookie (production HTTPS)           | Flag present                                 |
| SEC-T-05   | Check `Content-Security-Policy` header on all responses            | CSP header present with correct directives  |
| SEC-T-06   | Check `X-Frame-Options` header on admin pages                      | `SAMEORIGIN` present                        |
| SEC-T-07   | Attempt path traversal via crafted URL: `../../etc/passwd`         | 404 or 403; no file content returned        |
| SEC-T-08   | Verify admin password stored as bcrypt hash in admins.json         | Hash starts with `$2b$`                     |
| SEC-T-09   | Access `/api/admin/editions` without session cookie                | HTTP 401                                    |
| SEC-T-10   | XSS payload in search input: `<script>alert(1)</script>`           | Input escaped; no script executed            |
| SEC-T-11   | Direct URL access to another admin's meta.json via browser         | Served as static file (acceptable; not sensitive) |
| SEC-T-12   | Verify `.env` is not accessible via HTTP `GET /.env`               | 404 or blocked                               |

---

## 7. UI / UX Tests

| Test ID    | Test Case                                                           | Expected Result                              |
|------------|---------------------------------------------------------------------|----------------------------------------------|
| UI-01      | Landing page renders on Chrome, Firefox, Edge, Safari              | Consistent rendering across browsers        |
| UI-02      | Edition cards render correctly on 320px wide mobile               | No overflow or broken layout                |
| UI-03      | Year filter dropdown updates edition list dynamically              | Cards update without page reload             |
| UI-04      | Clicking "Read" opens edition in iframe                            | iframe loads correct `index.html`           |
| UI-05      | Loading spinner appears while iframe is loading                    | Spinner visible then hidden after load       |
| UI-06      | Empty state message shown when no editions match filter            | "No editions published yet" visible          |
| UI-07      | Fullscreen button expands iframe to full window                    | iframe fills viewport                        |
| UI-08      | Admin login form displays error on wrong credentials               | Error message appears without page crash     |
| UI-09      | Admin dashboard shows both published and unpublished editions       | Both visible with correct status badge      |
| UI-10      | Publish toggle on dashboard updates without full page reload        | Status changes in UI immediately             |

---

## 8. Performance Tests

### 8.1 Load Test Scenarios (using `locust`)

| Scenario               | Users | Duration | Threshold                              |
|------------------------|-------|----------|----------------------------------------|
| Browse landing page    | 200   | 2 min    | Avg response < 500ms, error rate < 1% |
| Fetch editions API     | 200   | 2 min    | Avg response < 200ms                   |
| Open iframe reader     | 50    | 2 min    | Avg response < 1s for static files    |

### 8.2 Acceptance Criteria
- Zero 5xx errors under 200 concurrent users on browse + API scenarios.
- Scanner completes indexing 100 editions in under 500ms on startup.

---

## 9. Accessibility Tests

| Test ID    | Check                                           | Tool / Method                 |
|------------|-------------------------------------------------|-------------------------------|
| ACC-01     | All images have `alt` attributes                | HTML inspection               |
| ACC-02     | Keyboard navigation reaches all interactive elements | Keyboard-only test          |
| ACC-03     | Color contrast ratio ≥ 4.5:1 for text          | WAVE / browser contrast checker |
| ACC-04     | Focus indicators visible on all focusable elements | Keyboard tab walk           |
| ACC-05     | ARIA labels present on icon-only buttons        | HTML inspection               |

---

## 10. Test Data

Create a test fixture set under `tests/fixtures/magazines/`:

```
tests/fixtures/magazines/
├── 2026/
│   ├── annual/
│   │   ├── index.html    (minimal valid HTML)
│   │   └── meta.json     (valid, published: true)
│   ├── departmental/
│   │   ├── cs/
│   │   │   ├── index.html
│   │   │   └── meta.json (published: true)
│   │   └── physics/
│   │       ├── index.html
│   │       └── meta.json (published: false)
│   └── bhavan/
│       └── bhavan1/
│           ├── index.html
│           └── meta.json (valid, published: true)
├── malformed/
│   └── bad_edition/
│       └── meta.json     (missing required fields)
└── no_meta/
    └── orphan_dir/
        └── index.html    (no meta.json)
```

---

## 11. Test Execution & Reporting

| Phase         | When                    | Report Format                          |
|---------------|-------------------------|-----------------------------------------|
| Unit Tests    | Every commit (CI)       | `pytest` HTML report                   |
| Integration   | Pre-PR merge            | `pytest` HTML report                   |
| Security      | Before v1.0 launch      | Manual checklist sign-off              |
| UI Tests      | Before v1.0 launch      | Screenshot evidence + notes            |
| Performance   | Before v1.0 launch      | Locust HTML report                     |

---

## 12. Exit Criteria

The system is ready for launch when:
- [ ] All MUST-priority functional requirements verified by tests
- [ ] All security checklist items pass (from `SECURITY.md`)
- [ ] Zero High or Critical defects open
- [ ] Performance thresholds met at 200 concurrent users
- [ ] UI tests pass on Chrome, Firefox, and Edge
- [ ] Accessibility score WCAG 2.1 AA (no critical violations)

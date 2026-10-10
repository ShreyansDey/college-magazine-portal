# Risk Register

## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Active                        |
| **Date**            | 2026-10-07                    |
| **Owner**           | Core Dev Team / Admin         |

---

## Risk Scoring Matrix

| Likelihood \ Impact | Low (1) | Medium (2) | High (3) |
|---------------------|---------|------------|----------|
| **High (3)**        | Medium (3) | High (6) | Critical (9) |
| **Medium (2)**      | Low (2)    | Medium (4)| High (6) |
| **Low (1)**         | Low (1)    | Low (2)   | Medium (3)|

**Score = Likelihood × Impact**

- 1–2: Low | 3–4: Medium | 6: High | 9: Critical

---

## Risk Register

### TECH RISKS

| ID     | Risk Description                                                  | Likelihood | Impact | Score   | Mitigation Strategy                                                                 | Owner          |
|--------|-------------------------------------------------------------------|------------|--------|---------|-------------------------------------------------------------------------------------|----------------|
| R-T-01 | Sub-team skips `meta.json` or uses wrong schema                  | High (3)   | Med (2)| 6 High  | Provide JSON schema + validator script; enforce during PR review                  | Core Dev Team  |
| R-T-02 | Large media files (>50MB) cause slow page loads                  | Med (2)    | High(3)| 6 High  | Document 50 MB limit; add pre-commit hook to warn; optimize cover images           | Sub-teams      |
| R-T-03 | Sub-team plugin breaks iframe embedding (CORS / CSP conflict)    | Med (2)    | High(3)| 6 High  | Provide CSP policy doc; test all editions in iframe before publish; sandbox attr   | Core Dev Team  |
| R-T-04 | Flask debug mode accidentally left ON in production              | Low (1)    | High(3)| 3 Med   | Add `FLASK_DEBUG=0` check on startup; document in DEPLOYMENT_GUIDE                | Dev / DevOps   |
| R-T-05 | Python version mismatch on server causes runtime errors          | Low (1)    | Med (2)| 2 Low   | Pin Python version in `README`; use `python_requires` in setup config             | DevOps         |
| R-T-06 | In-memory index lost on server restart (no DB)                  | Med (2)    | Low (1)| 2 Low   | Index auto-rebuilds on startup; acceptable for current scale                       | Core Dev Team  |
| R-T-07 | Filesystem scanner performance degrades with 500+ editions       | Low (1)    | Med (2)| 2 Low   | Benchmark at 200 editions; add caching or SQLite in v2.0 if needed                | Core Dev Team  |
| R-T-08 | Sub-team uses absolute asset paths (breaks inside iframe)        | High (3)   | Med (2)| 6 High  | Document relative paths in CONTRIBUTING.md; provide linting script                | Sub-teams      |

---

### SECURITY RISKS

| ID     | Risk Description                                                  | Likelihood | Impact | Score      | Mitigation Strategy                                                                | Owner        |
|--------|-------------------------------------------------------------------|------------|--------|------------|------------------------------------------------------------------------------------|--------------|
| R-S-01 | Admin password leaked (weak password or shoulder-surfing)         | Low (1)    | High(3)| 3 Med      | Enforce password policy; bcrypt hashing; rate limiting on login                   | Admin        |
| R-S-02 | `.env` file accidentally committed to git                         | Med (2)    | High(3)| 6 High     | `.env` in `.gitignore`; pre-commit hook; immediate rotation plan in SECURITY.md   | Dev Team     |
| R-S-03 | XSS injection via malicious sub-team plugin code                 | Low (1)    | High(3)| 3 Med      | iframe sandbox; CSP headers; admin code review before publishing                  | Admin        |
| R-S-04 | CSRF attack on admin endpoints                                   | Low (1)    | High(3)| 3 Med      | Flask-WTF CSRF token on all state-changing requests                               | Core Dev Team|
| R-S-05 | Brute-force attack on admin login                                | Med (2)    | High(3)| 6 High     | Flask-Limiter: 5 req/15 min/IP; generic error messages                            | Core Dev Team|
| R-S-06 | Path traversal via crafted magazine directory name               | Low (1)    | High(3)| 3 Med      | `os.path.realpath()` validation in scanner; `is_safe_path()` check               | Core Dev Team|
| R-S-07 | Session hijacking via insecure cookies                           | Low (1)    | High(3)| 3 Med      | `HttpOnly`, `Secure`, `SameSite=Lax` cookie flags; HTTPS in production           | Core Dev Team|
| R-S-08 | Server without HTTPS exposes admin session cookies               | Med (2)    | High(3)| 6 High     | Enforce HTTPS with Nginx + Let's Encrypt; HSTS header                             | DevOps       |

---

### PROJECT / OPERATIONAL RISKS

| ID     | Risk Description                                                  | Likelihood | Impact | Score    | Mitigation Strategy                                                                   | Owner        |
|--------|-------------------------------------------------------------------|------------|--------|----------|---------------------------------------------------------------------------------------|--------------|
| R-P-01 | Sub-teams miss submission deadline (no `index.html` by launch)   | High (3)   | Med (2)| 6 High   | Set hard submission deadline 1 week before launch; communicate Hard Collar early      | Admin        |
| R-P-02 | No one available to approve PRs (single point of failure)        | Med (2)    | High(3)| 6 High   | Designate at least 2 admins with repo merge access                                   | Admin        |
| R-P-03 | Server downtime during peak usage (e.g., college event)          | Low (1)    | High(3)| 3 Med    | Deploy with Gunicorn + Nginx; systemd auto-restart; test before major events         | DevOps       |
| R-P-04 | Data loss: magazine files deleted accidentally                   | Low (1)    | High(3)| 3 Med    | Weekly rsync backups; restrict server write access; branch protection on git         | DevOps       |
| R-P-05 | Key developer leaves mid-project                                 | Med (2)    | Med (2)| 4 Med    | Document all setup in README and this guide; maintain CONTRIBUTING.md                | Team Lead    |
| R-P-06 | Scope creep: sub-teams request features not in v1.0             | High (3)   | Low (1)| 3 Med    | Maintain backlog; communicate v1.0 scope clearly; log feature requests for v2.0     | Product Owner|
| R-P-07 | Hosting cost overruns (cloud deployment)                         | Low (1)    | Low (1)| 1 Low    | Start with free tier (Railway/Render) or on-premise; set cost alerts if using paid  | Admin        |

---

## Summary Dashboard

| Severity | Count | Risk IDs |
| ---------- | ------- | ---------- |
| Critical (9) | 0 | — |
| High (6) | 8 | R-T-01, R-T-02, R-T-03, R-T-08, R-S-02, R-S-05, R-S-08, R-P-01, R-P-02 |
| Medium (3–4) | 8 | R-T-04, R-T-07, R-S-01, R-S-03, R-S-04, R-S-06, R-S-07, R-P-03, R-P-04, R-P-05, R-P-06 |
| Low (1–2) | 4 | R-T-05, R-T-06, R-P-07 |

---

## Review Schedule

| Review Point             | When                                    |
|--------------------------|-----------------------------------------|
| Initial Risk Assessment  | Before development start               |
| Mid-Project Review       | At alpha release (v0.5)                |
| Pre-Launch Review        | 1 week before v1.0 launch              |
| Post-Launch Review       | 1 month after launch                   |

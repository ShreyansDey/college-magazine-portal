# Product Requirements Document (PRD)
## College Unified Magazine Portal

| Field               | Detail                          |
|---------------------|---------------------------------|
| **Document Version**| 1.0.0                           |
| **Status**          | Draft                           |
| **Date**            | 2026-10-07                      |
| **Product Owner**   | Magazine Portal Core Team       |
| **Stakeholders**    | College Admin, Faculty, Students|

---

## 1. Problem Statement

Student publications — Annual Magazines, Departmental Journals, and Bhavan (Hostel) Magazines — are currently scattered across USB drives, email attachments, and individual team websites. There is no unified, searchable, always-accessible place for students and faculty to browse all college publications.

**Core Problems:**
- Editions are hard to find after the academic year ends.
- Each team builds redundant infrastructure (hosting, viewer, etc.).
- No consistent presentation or branding.
- No administrative oversight of what's published.

---

## 2. Product Vision

> **"One portal to read every college magazine — past, present, and future."**

Build a centralized, beautifully designed web portal that acts as a permanent digital library for all student publications. Sub-teams focus on creating great content; the portal handles discovery, presentation, and long-term accessibility.

---

## 3. Goals & Success Metrics

| Goal                           | Success Metric                                                   |
|--------------------------------|------------------------------------------------------------------|
| Centralize all publications    | 100% of published editions accessible from the portal           |
| Reduce sub-team effort         | Sub-teams only write HTML/CSS/JS; no server setup needed        |
| Easy navigation                | Visitor reaches a specific edition in ≤ 3 clicks               |
| Reliability                    | ≥ 99% uptime during college hours                              |
| Admin control                  | Admin can publish/unpublish an edition in < 1 minute           |
| New year onboarding            | A new academic year directory can be added in < 5 minutes      |

---

## 4. Target Users & Personas

### 4.1 Priya — The Curious Student
- **Background:** 2nd-year undergraduate, wants to read last year's departmental magazine.
- **Goal:** Find and read a specific edition quickly.
- **Pain Point:** Doesn't know which website or drive to check.
- **Need:** Clear navigation by department and year.

### 4.2 Prof. Mehta — The Faculty Coordinator
- **Background:** Oversees the annual magazine committee.
- **Goal:** Share the annual magazine with the whole college community.
- **Pain Point:** No permanent, official link to share.
- **Need:** A stable URL they can share via email or WhatsApp.

### 4.3 Rohan — The Sub-Team Developer
- **Background:** CS department student, builds the CS magazine website.
- **Goal:** Publish the magazine without managing hosting.
- **Pain Point:** Doesn't know how to deploy to a server.
- **Need:** Submit code via PR to a common repo — portal handles the rest.

### 4.4 Admin Anjali — The Portal Administrator
- **Background:** Technical admin / senior student who maintains the portal.
- **Goal:** Review submitted editions and publish them when ready.
- **Pain Point:** Manual file copying and coordination across teams.
- **Need:** A dashboard to manage all editions in one place.

---

## 5. User Stories

### Public Visitor
- **US-01:** As a visitor, I want to see all published editions on the landing page so I can quickly browse.
- **US-02:** As a visitor, I want to filter editions by year and category so I find what I'm looking for fast.
- **US-03:** As a visitor, I want to read a magazine directly in the browser without downloading files.
- **US-04:** As a visitor, I want to search for an edition by name or department.
- **US-05:** As a visitor on mobile, I want the portal to be fully usable on my phone.

### Sub-Team Contributor
- **US-06:** As a contributor, I want clear instructions on how to structure my files and submit them.
- **US-07:** As a contributor, I want to know exactly what `meta.json` fields are required.
- **US-08:** As a contributor, I want a template/starter directory to reduce setup time.

### Admin
- **US-09:** As an admin, I want to log in securely to the admin dashboard.
- **US-10:** As an admin, I want to see all submitted editions (published and unpublished).
- **US-11:** As an admin, I want to publish or unpublish an edition with a single click.
- **US-12:** As an admin, I want to edit an edition's title, description, and cover image.
- **US-13:** As an admin, I want to manually trigger a re-scan of the magazine directory.
- **US-14:** As a Super-Admin, I want to create and manage other admin accounts.

---

## 6. Feature Breakdown

### 6.1 MVP (v1.0) — Must Ship

| # | Feature                        | Description                                                              |
|---|--------------------------------|--------------------------------------------------------------------------|
| 1 | Landing Page                   | Branded portal with Annual, Departmental, Bhavan sections               |
| 2 | Year Filter                    | Dropdown to filter editions by academic year                             |
| 3 | Edition Cards                  | Card UI with cover image, title, category, year, Read button            |
| 4 | Iframe Reader                  | Embedded reader that loads any edition's `index.html`                   |
| 5 | Auto-Scanner API               | Backend scans `static/magazines/` and returns JSON feed                 |
| 6 | meta.json Contract             | Defined schema + validator                                               |
| 7 | Admin Login                    | Secure login page with rate limiting and CSRF protection                |
| 8 | Admin Dashboard                | View, publish/unpublish, and edit edition metadata                      |
| 9 | Responsive Design              | Mobile, tablet, and desktop layouts                                      |
| 10 | Security Headers               | CSP, HSTS, X-Content-Type-Options on all responses                     |

### 6.2 v1.1 — Should Ship

| # | Feature                        | Description                                                              |
|---|--------------------------------|--------------------------------------------------------------------------|
| 11 | Search Bar                    | Client-side or server-side search across editions                        |
| 12 | Fullscreen Reader             | Expand iframe to full viewport                                           |
| 13 | Manual Rescan Endpoint        | POST /api/admin/rescan without server restart                           |
| 14 | Edition Starter Template      | Downloadable ZIP with sample directory structure                         |
| 15 | Breadcrumb Navigation         | Breadcrumbs in reader view (Portal > Dept > Year)                       |

### 6.3 v2.0 — Could Ship

| # | Feature                        | Description                                                              |
|---|--------------------------------|--------------------------------------------------------------------------|
| 16 | Analytics Dashboard           | View counts per edition                                                  |
| 17 | Email Notifications           | Notify admin when a new PR is merged                                    |
| 18 | Bulk Export                   | Download all editions as a ZIP archive                                  |
| 19 | Dark Mode                     | Toggle-able dark theme for the portal                                    |
| 20 | Social Share Buttons          | Share a specific edition link on WhatsApp / Email                       |

---

## 7. Information Architecture

```
Portal (/)
├── Landing Page
│   ├── Hero Section (College branding)
│   ├── Annual Section
│   │   └── [Year Filter] → Edition Cards → [Reader]
│   ├── Departmental Section
│   │   └── [Dept Filter] → [Year Filter] → Edition Cards → [Reader]
│   └── Bhavan Section
│       └── [Bhavan Filter (1–5)] → [Year Filter] → Edition Cards → [Reader]
│
├── Reader View (embedded, same page)
│
└── Admin (/admin)
    ├── Login (/admin/login)
    ├── Dashboard (/admin/dashboard)
    │   ├── Edition List
    │   ├── Publish/Unpublish Toggle
    │   ├── Edit Metadata
    │   └── Rescan Trigger
    └── Account Management (/admin/accounts) [Super-Admin only]
```

---

## 8. Design Principles

1. **Content-First:** Magazine editions are the hero. The portal chrome is minimal and unobtrusive.
2. **Zero Friction:** Visitors should never have to install anything, sign up, or download files to read.
3. **Sub-Team Sovereignty:** Sub-teams build exactly what they want inside their folder. The portal wraps it without interference.
4. **Admin Confidence:** Admins have full control over what is publicly visible at any time.
5. **Scalability by Design:** Adding a new year, department, or bhavan requires zero code change.

---

## 9. Release Plan

| Release | Target Date     | Key Features                                      |
|---------|-----------------|---------------------------------------------------|
| v0.1 (Alpha) | Week 2    | Flask skeleton, scanner, JSON API working        |
| v0.5 (Beta)  | Week 4    | Landing page UI, iframe reader, meta.json schema |
| v1.0 (Launch)| Week 7    | Admin dashboard, auth, security hardening        |
| v1.1         | Week 10   | Search, fullscreen reader, starter template      |

---

## 10. Out of Scope (v1.0)

- File upload via the admin dashboard (all changes go through Git PR)
- Multi-language support
- Comments or ratings on editions
- User accounts for visitors
- PDF rendering (editions are HTML-based)
- Email-based notifications

---

## 11. Open Questions

| # | Question                                                                 | Owner       |
|---|--------------------------------------------------------------------------|-------------|
| Q1 | Should the portal be deployed on-premise or on a cloud provider?        | Admin Team  |
| Q2 | How many departments need to be supported from day one?                 | Faculty     |
| Q3 | Is a custom domain available (e.g., magazine.college.edu)?             | IT Dept     |
| Q4 | Should the admin dashboard be accessible from outside the college LAN? | Admin Team  |
| Q5 | What is the maximum storage budget for magazine files?                  | IT Dept     |

---

## 12. Risks

| Risk                             | Likelihood | Impact | Mitigation                                      |
|----------------------------------|------------|--------|-------------------------------------------------|
| Sub-team skips meta.json        | High       | Medium | Validator rejects during PR review              |
| Large files slow page load      | Medium     | High   | Enforce 50 MB limit; document image compression |
| Broken iframe (CORS / CSP)     | Medium     | High   | Document CSP policy; test all editions pre-launch |
| Admin password leaked           | Low        | High   | bcrypt hashing, .env, rotate on compromise      |
| Server downtime during event    | Low        | High   | Deploy with a process manager (gunicorn+nginx)  |

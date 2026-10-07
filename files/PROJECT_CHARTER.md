# Project Charter
## College Unified Magazine Portal

| Field               | Detail                          |
|---------------------|---------------------------------|
| **Document Version**| 1.0.0                           |
| **Status**          | Draft                           |
| **Date**            | 2026-10-07                      |
| **Project Name**    | College Unified Magazine Portal |

---

## 1. Project Purpose & Justification

Student publications at our college — Annual Magazines, Departmental Journals, and Bhavan Magazines — currently lack a permanent, organized home. Files are scattered, links go dead, and past editions are lost. This project creates a **permanent digital library** that centralizes every student publication under a single, professionally designed portal.

**Business Need:** Preserve institutional memory and showcase student creativity sustainably.

---

## 2. Project Objectives

| # | Objective                                                                      | Success Criterion                             |
|---|--------------------------------------------------------------------------------|-----------------------------------------------|
| 1 | Centralize all student publications in one web portal                          | 100% of publications accessible from portal  |
| 2 | Reduce sub-team infrastructure burden to zero                                  | Sub-teams only write HTML/CSS/JS             |
| 3 | Enable admin control over what is publicly visible                             | Admin can publish/unpublish in < 1 minute    |
| 4 | Build a scalable, maintainable platform for future years                       | New year onboarded in < 5 minutes           |
| 5 | Launch a secure, accessible, production-ready system                           | Passes security checklist; WCAG 2.1 AA      |

---

## 3. Scope

### In Scope (v1.0)
- Flask-based portal backend with auto-scanner
- Public landing page with edition discovery
- Iframe-based magazine reader
- Admin dashboard (login, publish/unpublish, metadata edit)
- RBAC (Admin + Super-Admin)
- Security hardening (CSRF, rate limiting, CSP headers, bcrypt)
- Contributing guide for sub-teams
- Deployment guide (local + production)
- Documentation suite (SRS, PRD, API Design, Architecture, etc.)

### Out of Scope (v1.0)
- In-app file upload (all submissions via Git PR)
- Multi-language support
- Visitor accounts or ratings
- Email notifications
- Analytics dashboard
- PDF-only magazine support
- Mobile app

---

## 4. Stakeholders

| Stakeholder              | Role                                         | Involvement     |
|--------------------------|----------------------------------------------|-----------------|
| College Administration   | Sponsor; approves project direction          | Low — milestone reviews |
| Faculty Coordinators     | Oversee annual/department magazines          | Medium — content approval |
| Core Dev Team            | Build and maintain the portal               | High — daily    |
| Sub-Team Developers      | Build magazine plugins for each edition      | High — during development windows |
| Hostel Wardens / Bhavan Reps | Oversee bhavan magazine submissions    | Low — review only |
| Students (visitors)      | End users; readers of magazines             | None — recipients |
| IT / DevOps              | Server provisioning and maintenance         | Low — deployment only |

---

## 5. High-Level Milestones

| Milestone              | Target Week | Deliverable                                              |
|------------------------|-------------|----------------------------------------------------------|
| M1 — Project Start     | Week 0      | Project charter signed; team assigned; repo set up      |
| M2 — Architecture Done | Week 1      | All `files/` documentation complete; directory structure set |
| M3 — Backend Alpha     | Week 2      | Flask scanner, `/api/editions`, routes working          |
| M4 — Frontend Beta     | Week 4      | Landing page UI, filters, iframe reader, edition cards  |
| M5 — Admin Dashboard   | Week 5      | Login, publish/unpublish, metadata edit working         |
| M6 — Security Hardened | Week 6      | CSRF, rate limiting, security headers, HTTPS configured |
| M7 — v1.0 Launch       | Week 7      | Production deploy; all sub-teams have submitted editions |
| M8 — Post-Launch Review| Week 9      | Bug fixes, accessibility fixes, v1.1 planning           |

---

## 6. Team Structure

| Role                    | Responsibilities                                                      |
|-------------------------|-----------------------------------------------------------------------|
| **Project Lead**        | Coordinates milestones, resolves blockers, PR final approval         |
| **Backend Developer(s)**| Flask app, scanner, REST API, admin routes, security                 |
| **Frontend Developer(s)**| Portal UI, CSS, portal.js, admin dashboard UI                       |
| **Sub-Team Leads**      | Lead their dept/bhavan team; ensure Hard Collar compliance           |
| **Admin (Portal)**      | Reviews all submitted PRs; publishes editions; manages accounts      |
| **DevOps (optional)**   | Server setup, Nginx, SSL, CI/CD                                      |

---

## 7. Budget & Resources

| Resource                | Cost Estimate        |
|-------------------------|----------------------|
| Hosting (on-premise)    | Free (college server)|
| Hosting (cloud, free tier) | Free (Railway/Render) |
| Domain name (optional)  | ~$10–15/year         |
| SSL Certificate         | Free (Let's Encrypt) |
| Developer time          | Volunteer (student project) |
| External tools          | All open-source (no cost) |

---

## 8. Constraints

| Constraint | Description |
|------------|-------------|
| Technology | Python 3.10+, Flask, standard web tech only |
| Timeline   | v1.0 must launch before college's annual magazine release event |
| Repository | All code centralized in a single GitHub repository |
| Hard Collar | Every edition plugin MUST have `index.html` at root |
| No DB      | v1.0 uses no relational database (filesystem + JSON) |

---

## 9. Assumptions

- At least one person with server/hosting access is available as Super-Admin.
- All sub-teams have access to the GitHub repository.
- The college IT department can provide or support a server or cloud account.
- Sub-teams are capable of building a basic HTML website.
- An admin reviews and approves PRs within 48 hours of submission.

---

## 10. Success Criteria for v1.0

The project is considered successfully launched when:

- [ ] Portal is live and publicly accessible (LAN or internet)
- [ ] At least one edition from each category (annual, departmental, bhavan) is published
- [ ] Admin dashboard is functional (login, publish, edit)
- [ ] Security checklist from `SECURITY.md` is 100% complete
- [ ] CONTRIBUTING.md is distributed to all sub-teams
- [ ] No Critical or High priority bugs are open
- [ ] Page loads in < 2 seconds on the target network

---

## 11. Approval

| Role             | Name | Signature | Date |
|------------------|------|-----------|------|
| Project Lead     |      |           |      |
| Faculty Sponsor  |      |           |      |
| Core Dev Lead    |      |           |      |

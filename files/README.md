# 📁 Project Documentation Index

## College Unified Magazine Portal

This folder contains all pre-development documentation required before implementation begins.

---

## Document Inventory

| # | File | Description | Status |
| --- | ------ | ------------- | -------- |
| 1 | [SRS.md](SRS.md) | **Software Requirements Specification** — Full functional & non-functional requirements, security requirements, data schema, constraints | Approved |
| 2 | [PRD.md](PRD.md) | **Product Requirements Document** — Personas, user stories, feature breakdown (MVP vs future), release plan, open questions | Approved |
| 3 | [ARCHITECTURE.md](ARCHITECTURE.md) | **System Architecture Document** — Component diagrams, directory structure, tech stack, request flow, micro-frontend contract, ADRs | Approved |
| 4 | [API_DESIGN.md](API_DESIGN.md) | **API Design** — All REST endpoints (public & admin), request/response schemas, error codes, `meta.json` canonical schema | Approved |
| 5 | [SECURITY.md](SECURITY.md) | **Security & Auth Design** — Authentication flow, RBAC matrix, CSRF, rate limiting, HTTP headers, secrets management, pre-launch checklist | Approved |
| 6 | [DATA_DESIGN.md](DATA_DESIGN.md) | **Data Design & Metadata Schema** — `meta.json` & `admins.json` schemas, naming conventions, in-memory index structure, validation rules | Approved |
| 7 | [UI_UX_GUIDELINES.md](UI_UX_GUIDELINES.md) | **UI/UX Design Guidelines** — Color palette, typography, spacing system, component specs, animations, accessibility requirements | Approved |
| 8 | [TEST_PLAN.md](TEST_PLAN.md) | **Test Plan** — Unit, integration, security, UI, performance, and accessibility tests with test IDs and exit criteria | Approved |
| 9 | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | **Deployment Guide** — Local dev setup, production (Nginx + Gunicorn + SSL), updates, backups, monitoring, troubleshooting | Approved |
| 10 | [CONTRIBUTING.md](CONTRIBUTING.md) | **Sub-Team Developer Handbook** — Hard Collar contract, `meta.json` guide, asset path rules, Git workflow, PR checklist | Approved |
| 11 | [RISK_REGISTER.md](RISK_REGISTER.md) | **Risk Register** — Scored technical, security, and operational risks with mitigation strategies and review schedule | Active |
| 12 | [PROJECT_CHARTER.md](PROJECT_CHARTER.md) | **Project Charter** — Objectives, scope, stakeholders, milestones, team structure, budget, success criteria | Approved |
| 13 | [ROADMAP.md](ROADMAP.md) | **Development Roadmap & Sprint Plan** — 5-phase task breakdown, owners, priorities, exit criteria per phase, backlog | Completed |

---

## Reading Order

If you're **new to this project**, read documents in this order:

1. `PROJECT_CHARTER.md` — Understand the why and what
2. `PRD.md` — Understand the users and features
3. `SRS.md` — Understand the detailed requirements
4. `ARCHITECTURE.md` — Understand how it's built
5. `SECURITY.md` — Understand how it's secured
6. `API_DESIGN.md` — Understand the data contracts
7. `DATA_DESIGN.md` — Understand the data layer
8. `UI_UX_GUIDELINES.md` — Understand the visual design
9. `CONTRIBUTING.md` — If you are a sub-team developer
10. `DEPLOYMENT_GUIDE.md` — If you are deploying
11. `TEST_PLAN.md` — If you are doing QA
12. `RISK_REGISTER.md` — For project management
13. `ROADMAP.md` — For sprint planning

---

## Key Decisions (Quick Reference)

| Decision | Choice | Document |
| ---------- | -------- | ---------- |
| Backend | Python Flask ≥ 3.0 | ARCHITECTURE.md |
| Database | None — filesystem + `meta.json` | ARCHITECTURE.md, DATA_DESIGN.md |
| Auth | Session-based + bcrypt | SECURITY.md |
| Reader | `<iframe>` with sandbox | ARCHITECTURE.md |
| Plugin contract | Hard Collar: `index.html` required | SRS.md, CONTRIBUTING.md |
| Sub-team workflow | Git Pull Request | CONTRIBUTING.md |
| CSRF protection | Flask-WTF | SECURITY.md |
| Rate limiting | Flask-Limiter (5/15min on login) | SECURITY.md |
| Production server | Gunicorn + Nginx + Let's Encrypt | DEPLOYMENT_GUIDE.md |

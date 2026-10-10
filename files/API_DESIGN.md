# API Design Document

## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Draft                         |
| **Date**            | 2026-10-07                    |
| **Base URL (dev)**  | `http://localhost:5000`       |
| **Base URL (prod)** | `https://magazine.college.edu`|

---

## 1. Overview

The portal exposes a lightweight REST API with two route namespaces:

| Namespace      | Path Prefix     | Auth Required | Description                          |
|----------------|-----------------|---------------|--------------------------------------|
| Public API     | `/api/`         | No            | Read-only edition discovery feed     |
| Admin API      | `/api/admin/`   | Yes (Session) | Edition management, rescan           |
| Page Routes    | `/`, `/admin/*` | Varies        | HTML page responses (not covered here) |

---

## 2. Public API Endpoints

### 2.1 GET /api/editions

Returns a list of all **published** editions.

**Authentication:** None  
**Rate Limit:** 60 requests/minute/IP

**Query Parameters:**

| Parameter    | Type    | Required | Description                                           |
|--------------|---------|----------|-------------------------------------------------------|
| `year`       | integer | No       | Filter by academic year (e.g. `2026`)                |
| `category`   | string  | No       | Filter by `annual`, `departmental`, or `bhavan`      |
| `sub_id`     | string  | No       | Filter by department/bhavan ID (e.g. `cs`, `bhavan1`)|

**Example Request:**

```
GET /api/editions?year=2026&category=departmental
```

**Response 200 OK:**

```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "cs-2026",
      "title": "CS Department Journal 2026",
      "year": 2026,
      "category": "departmental",
      "sub_id": "cs",
      "description": "Annual journal of the Computer Science department.",
      "cover_image": "/static/magazines/2026/departmental/cs/cover.jpg",
      "path": "/static/magazines/2026/departmental/cs/index.html",
      "tags": ["technology", "research", "2026"],
      "published": true,
      "published_date": "2026-03-15",
      "author_team": "CS Magazine Team"
    },
    {
      "id": "physics-2026",
      "title": "Physics Explorer 2026",
      "year": 2026,
      "category": "departmental",
      "sub_id": "physics",
      "description": "Physics department annual magazine.",
      "cover_image": "/static/magazines/2026/departmental/physics/cover.jpg",
      "path": "/static/magazines/2026/departmental/physics/index.html",
      "tags": ["science", "2026"],
      "published": true,
      "published_date": "2026-04-01",
      "author_team": "Physics Mag Team"
    }
  ]
}
```

**Response 200 OK (empty):**

```json
{
  "status": "success",
  "count": 0,
  "data": []
}
```

**Response 400 Bad Request (invalid params):**

```json
{
  "status": "error",
  "message": "Invalid category value. Must be one of: annual, departmental, bhavan."
}
```

---

### 2.2 GET /api/editions/:id

Returns a single edition by its ID.

**Authentication:** None

**Path Parameters:**

| Parameter | Type   | Description                  |
|-----------|--------|------------------------------|
| `id`      | string | Unique edition ID (e.g. `cs-2026`) |

**Response 200 OK:**

```json
{
  "status": "success",
  "data": {
    "id": "cs-2026",
    "title": "CS Department Journal 2026",
    "year": 2026,
    "category": "departmental",
    "sub_id": "cs",
    "description": "Annual journal of the Computer Science department.",
    "cover_image": "/static/magazines/2026/departmental/cs/cover.jpg",
    "path": "/static/magazines/2026/departmental/cs/index.html",
    "tags": ["technology", "research"],
    "published": true,
    "published_date": "2026-03-15",
    "author_team": "CS Magazine Team"
  }
}
```

**Response 404 Not Found:**

```json
{
  "status": "error",
  "message": "Edition 'cs-2025' not found or not published."
}
```

---

### 2.3 GET /api/years

Returns a sorted list of all years that have at least one published edition.

**Authentication:** None

**Response 200 OK:**

```json
{
  "status": "success",
  "data": [2026, 2025, 2024]
}
```

---

### 2.4 GET /api/categories

Returns available categories and their sub-IDs with edition counts.

**Authentication:** None

**Response 200 OK:**

```json
{
  "status": "success",
  "data": {
    "annual": { "count": 1 },
    "departmental": {
      "count": 4,
      "sub_ids": ["cs", "physics", "maths", "chemistry"]
    },
    "bhavan": {
      "count": 3,
      "sub_ids": ["bhavan1", "bhavan2", "bhavan3"]
    }
  }
}
```

---

## 3. Admin API Endpoints

> All admin endpoints require a valid session cookie. Unauthorized requests receive a 401 response.

### 3.1 GET /api/admin/editions

Returns ALL editions including unpublished ones. Admin use only.

**Authentication:** Session cookie (Admin or Super-Admin role)

**Response 200 OK:**

```json
{
  "status": "success",
  "count": 5,
  "data": [
    {
      "id": "cs-2026",
      "title": "CS Department Journal 2026",
      "published": true,
      ...
    },
    {
      "id": "maths-2026",
      "title": "Mathematics Digest 2026",
      "published": false,
      ...
    }
  ]
}
```

---

### 3.2 PATCH /api/admin/editions/:id

Update edition metadata or publication status.

**Authentication:** Session cookie (Admin or Super-Admin role)  
**CSRF:** Token required in header `X-CSRFToken`  
**Content-Type:** `application/json`

**Request Body (all fields optional — partial update):**

```json
{
  "title": "Updated Title",
  "description": "Updated description text.",
  "cover_image": "/static/magazines/2026/departmental/cs/new_cover.jpg",
  "tags": ["technology", "AI"],
  "published": true,
  "published_date": "2026-03-20"
}
```

**Response 200 OK:**

```json
{
  "status": "success",
  "message": "Edition 'cs-2026' updated successfully.",
  "data": { "...updated meta.json contents..." }
}
```

**Response 400 Bad Request:**

```json
{
  "status": "error",
  "message": "Invalid field: 'year' cannot be modified via API."
}
```

**Response 401 Unauthorized:**

```json
{
  "status": "error",
  "message": "Authentication required."
}
```

**Response 404 Not Found:**

```json
{
  "status": "error",
  "message": "Edition 'cs-2025' not found."
}
```

---

### 3.3 POST /api/admin/rescan

Forces the backend to re-scan the `static/magazines/` directory and rebuild the in-memory index.

**Authentication:** Session cookie (Admin or Super-Admin role)  
**CSRF:** Token required  
**Request Body:** None

**Response 200 OK:**

```json
{
  "status": "success",
  "message": "Rescan complete. 7 editions indexed (5 published, 2 unpublished).",
  "scanned_at": "2026-10-07T15:30:00Z",
  "total": 7,
  "published": 5,
  "unpublished": 2,
  "errors": []
}
```

**Response 200 OK (with scan errors):**

```json
{
  "status": "partial",
  "message": "Rescan complete with warnings.",
  "total": 7,
  "published": 5,
  "unpublished": 1,
  "errors": [
    {
      "path": "static/magazines/2026/departmental/history/",
      "reason": "meta.json missing or malformed."
    }
  ]
}
```

---

### 3.4 GET /api/admin/accounts

Returns a list of all admin accounts. **Super-Admin only.**

**Authentication:** Session cookie (Super-Admin role only)

**Response 200 OK:**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "username": "anjali",
      "role": "super-admin",
      "created_at": "2026-01-10T10:00:00Z",
      "last_login": "2026-10-07T09:00:00Z"
    },
    {
      "id": 2,
      "username": "ravi",
      "role": "admin",
      "created_at": "2026-02-01T08:00:00Z",
      "last_login": "2026-10-06T14:00:00Z"
    }
  ]
}
```

---

### 3.5 POST /api/admin/accounts

Create a new admin account. **Super-Admin only.**

**Authentication:** Session cookie (Super-Admin role)  
**CSRF:** Token required  
**Content-Type:** `application/json`

**Request Body:**

```json
{
  "username": "neha",
  "password": "SecureP@ss123",
  "role": "admin"
}
```

**Validation Rules:**

- `username`: 3–30 characters, alphanumeric + underscore only
- `password`: min 8 characters, at least 1 uppercase, 1 digit, 1 special character
- `role`: must be `"admin"` (only super-admin can set super-admin role)

**Response 201 Created:**

```json
{
  "status": "success",
  "message": "Admin account 'neha' created.",
  "data": { "id": 3, "username": "neha", "role": "admin" }
}
```

**Response 409 Conflict:**

```json
{
  "status": "error",
  "message": "Username 'neha' already exists."
}
```

---

### 3.6 DELETE /api/admin/accounts/:id

Delete an admin account. **Super-Admin only.** Cannot delete own account.

**Authentication:** Session cookie (Super-Admin role)  
**CSRF:** Token required

**Response 200 OK:**

```json
{
  "status": "success",
  "message": "Admin account 'ravi' deleted."
}
```

**Response 403 Forbidden:**

```json
{
  "status": "error",
  "message": "Cannot delete your own account."
}
```

---

## 4. Authentication Endpoints (Page Routes)

These are full page responses, not JSON. Documented here for completeness.

| Method | Path             | Description                                  |
|--------|------------------|----------------------------------------------|
| GET    | `/admin/login`   | Renders login form                           |
| POST   | `/admin/login`   | Processes login; redirects to dashboard on success |
| POST   | `/admin/logout`  | Invalidates session; redirects to login      |

---

## 5. Error Codes Reference

| HTTP Status | Code    | Meaning                                           |
|-------------|---------|---------------------------------------------------|
| 200         | OK      | Success                                           |
| 201         | Created | Resource successfully created                    |
| 400         | Bad Request | Invalid query params or malformed request body |
| 401         | Unauthorized | Missing or invalid session cookie            |
| 403         | Forbidden | Valid session but insufficient role             |
| 404         | Not Found | Resource does not exist                        |
| 409         | Conflict | Duplicate resource (e.g. duplicate username)   |
| 429         | Too Many Requests | Rate limit exceeded                    |
| 500         | Server Error | Unhandled exception (see server logs)        |

---

## 6. meta.json Schema (Canonical)

Every edition directory MUST contain a `meta.json` conforming to this schema:

```json
{
  "$schema": "meta-schema.json",
  "id": {
    "type": "string",
    "pattern": "^[a-z0-9-]+$",
    "description": "Unique edition identifier, e.g. 'cs-2026'"
  },
  "title": {
    "type": "string",
    "maxLength": 100
  },
  "year": {
    "type": "integer",
    "minimum": 2000,
    "maximum": 2100
  },
  "category": {
    "type": "string",
    "enum": ["annual", "departmental", "bhavan"]
  },
  "sub_id": {
    "type": ["string", "null"],
    "description": "Dept ID (e.g. 'cs') or bhavan ID (e.g. 'bhavan1'). Null for annual."
  },
  "description": {
    "type": "string",
    "maxLength": 500
  },
  "cover_image": {
    "type": "string",
    "description": "Relative path to cover image from edition root"
  },
  "tags": {
    "type": "array",
    "items": { "type": "string" }
  },
  "published": {
    "type": "boolean"
  },
  "published_date": {
    "type": ["string", "null"],
    "format": "date"
  },
  "author_team": {
    "type": "string",
    "maxLength": 100
  }
}
```

### 6.1 Example meta.json

```json
{
  "id": "cs-2026",
  "title": "CS Department Journal 2026",
  "year": 2026,
  "category": "departmental",
  "sub_id": "cs",
  "description": "The annual publication of the CS Department showcasing student projects, research, and creative writing.",
  "cover_image": "cover.jpg",
  "tags": ["technology", "research", "AI", "2026"],
  "published": true,
  "published_date": "2026-03-15",
  "author_team": "CS Magazine Team 2026"
}
```

---

## 7. Admin Credential Storage Format

Admin credentials are stored in a JSON file at a path configured in `.env` (e.g., `data/admins.json`). This file is NEVER committed to git.

```json
[
  {
    "id": 1,
    "username": "anjali",
    "password_hash": "$2b$12$...",
    "role": "super-admin",
    "created_at": "2026-01-10T10:00:00Z",
    "last_login": "2026-10-07T09:00:00Z"
  }
]
```

> **Note:** In v2.0, this will be migrated to SQLite for ACID compliance.

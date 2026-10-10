# Data Design & Metadata Schema

## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Draft                         |
| **Date**            | 2026-10-07                    |

---

## 1. Overview

The portal uses a **filesystem-based data layer**. There is no relational database in v1.0. All persistent data lives in:

1. `meta.json` — One per edition, inside its directory. Stores edition metadata.
2. `data/admins.json` — One global file (outside `static/`). Stores admin accounts.
3. `.env` — Environment variables and secrets (never committed to git).

---

## 2. Edition Metadata — meta.json

### 2.1 Location Pattern

```
static/magazines/<YEAR>/<CATEGORY>/<SUB_ID>/meta.json
```

### 2.2 Full Schema

| Field           | Type              | Required | Rules                                                            |
|-----------------|-------------------|----------|------------------------------------------------------------------|
| `id`            | string            | ✅       | Lowercase, alphanumeric + hyphens only. Globally unique. Pattern: `^[a-z0-9-]+$` |
| `title`         | string            | ✅       | 1–100 characters                                                 |
| `year`          | integer           | ✅       | Between 2000 and 2100                                            |
| `category`      | string (enum)     | ✅       | Must be exactly `"annual"`, `"departmental"`, or `"bhavan"`     |
| `sub_id`        | string \| null    | ✅       | Required for departmental and bhavan; `null` for annual          |
| `description`   | string            | ✅       | 1–500 characters                                                 |
| `cover_image`   | string            | ✅       | Relative filename (e.g. `"cover.jpg"`); file must exist in same dir |
| `tags`          | array of strings  | ✅       | At least 1 tag; each tag max 30 characters                      |
| `published`     | boolean           | ✅       | `true` = visible publicly; `false` = hidden (admin sets this)  |
| `published_date`| string \| null    | No       | ISO 8601 date (YYYY-MM-DD) or `null`                            |
| `author_team`   | string            | ✅       | 1–100 characters                                                 |

### 2.3 Example meta.json Files

#### Annual Magazine

```json
{
  "id": "annual-2026",
  "title": "Prism 2026 — Annual College Magazine",
  "year": 2026,
  "category": "annual",
  "sub_id": null,
  "description": "The flagship annual magazine of our college, showcasing the best of student creativity across all departments.",
  "cover_image": "cover.jpg",
  "tags": ["annual", "college", "2026", "culture", "creativity"],
  "published": true,
  "published_date": "2026-02-14",
  "author_team": "Annual Magazine Editorial Board 2026"
}
```

#### Departmental Magazine

```json
{
  "id": "cs-2026",
  "title": "ByteStream 2026 — CS Department Journal",
  "year": 2026,
  "category": "departmental",
  "sub_id": "cs",
  "description": "Annual publication of the Computer Science department featuring research highlights, student projects, and tech culture.",
  "cover_image": "cover.jpg",
  "tags": ["technology", "research", "AI", "2026"],
  "published": false,
  "published_date": null,
  "author_team": "CS Magazine Team 2026"
}
```

#### Bhavan Magazine

```json
{
  "id": "bhavan1-2026",
  "title": "Ekta — Bhavan 1 Annual Magazine 2026",
  "year": 2026,
  "category": "bhavan",
  "sub_id": "bhavan1",
  "description": "Bhavan 1's annual magazine capturing hostel life, events, memories, and stories.",
  "cover_image": "cover.png",
  "tags": ["bhavan", "hostel", "life", "2026"],
  "published": true,
  "published_date": "2026-03-01",
  "author_team": "Bhavan 1 Magazine Committee"
}
```

---

## 3. Admin Credential Store — admins.json

### 3.1 Location

```
data/admins.json
```

> This file MUST be outside the `static/` directory so it cannot be served directly as a static file.
> It MUST be listed in `.gitignore`.

### 3.2 Schema

| Field           | Type    | Description                                             |
|-----------------|---------|---------------------------------------------------------|
| `id`            | integer | Auto-incrementing unique identifier                    |
| `username`      | string  | Unique username (3–30 chars, alphanumeric + underscore)|
| `password_hash` | string  | bcrypt hash of the password (starts with `$2b$`)      |
| `role`          | string  | `"admin"` or `"super-admin"`                           |
| `created_at`    | string  | ISO 8601 datetime                                       |
| `last_login`    | string \| null | ISO 8601 datetime or null if never logged in   |

### 3.3 Example admins.json

```json
[
  {
    "id": 1,
    "username": "anjali",
    "password_hash": "$2b$12$KIXYouRealHashGoesHereXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "role": "super-admin",
    "created_at": "2026-01-10T10:00:00Z",
    "last_login": "2026-10-07T09:00:00Z"
  },
  {
    "id": 2,
    "username": "ravi",
    "password_hash": "$2b$12$AnotherHashHereXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "role": "admin",
    "created_at": "2026-02-01T08:00:00Z",
    "last_login": null
  }
]
```

---

## 4. In-Memory Edition Index

The Flask scanner builds this data structure in memory on startup and on rescan:

```python
EDITION_INDEX = {
    "cs-2026": {
        "id": "cs-2026",
        "title": "ByteStream 2026",
        "year": 2026,
        "category": "departmental",
        "sub_id": "cs",
        "description": "...",
        "cover_image": "/static/magazines/2026/departmental/cs/cover.jpg",
        "path": "/static/magazines/2026/departmental/cs/index.html",
        "tags": ["technology"],
        "published": True,
        "published_date": "2026-03-15",
        "author_team": "CS Team"
    },
    "annual-2026": { ... },
    ...
}
```

Key differences from `meta.json`:

- `cover_image` is converted to a **full absolute URL path** (from relative filename)
- `path` field is **added** (computed from directory location)
- Python `bool` is used instead of JSON `boolean`

---

## 5. Naming Conventions

### 5.1 Edition IDs

| Category      | Convention              | Example         |
|---------------|------------------------|-----------------|
| Annual        | `annual-<year>`        | `annual-2026`   |
| Departmental  | `<dept>-<year>`        | `cs-2026`, `physics-2026` |
| Bhavan        | `bhavan<N>-<year>`     | `bhavan1-2026`, `bhavan3-2026` |

### 5.2 Sub-IDs (Department Codes)

| Department    | sub_id      |
|---------------|-------------|
| Computer Science | `cs`    |
| Physics       | `physics`   |
| Mathematics   | `maths`     |
| Chemistry     | `chemistry` |
| Biology       | `biology`   |
| Electronics   | `ece`       |
| Mechanical    | `mech`      |
| Civil         | `civil`     |
| *(Add more as needed)* | |

### 5.3 Bhavan Sub-IDs

| Hostel   | sub_id    |
|----------|-----------|
| Bhavan 1 | `bhavan1` |
| Bhavan 2 | `bhavan2` |
| Bhavan 3 | `bhavan3` |
| Bhavan 4 | `bhavan4` |
| Bhavan 5 | `bhavan5` |

---

## 6. Data Flow

```
Sub-team creates meta.json
        │
        ▼
PR merged into main branch
        │
        ▼
Flask starts (or admin triggers rescan)
        │
        ▼
Scanner walks static/magazines/
        │
        ▼
For each directory with meta.json:
  ├── Validate schema (jsonschema)
  ├── Check published: true
  └── Build entry in EDITION_INDEX
        │
        ▼
GET /api/editions → Returns EDITION_INDEX filtered to published=true
        │
        ▼
Admin PATCH /api/admin/editions/:id → Updates meta.json on disk + EDITION_INDEX in memory
```

---

## 7. Validation Rules Summary

| Check                        | On Scan | On Admin Edit | On PR Review |
|------------------------------|---------|---------------|--------------|
| `index.html` exists          | ✅      | N/A           | ✅           |
| `meta.json` exists           | ✅      | N/A           | ✅           |
| All required fields present  | ✅      | ✅            | ✅           |
| `id` is unique               | ✅      | ✅            | ✅           |
| `category` is valid enum     | ✅      | ✅            | ✅           |
| `year` is integer 2000–2100  | ✅      | ✅            | ✅           |
| `cover_image` file exists    | ✅      | ✅            | ✅           |
| Total size ≤ 50MB            | ❌      | N/A           | ✅           |
| No absolute paths in HTML    | ❌      | N/A           | ✅ (script) |

---

## 8. Future: Migration to SQLite (v2.0)

When the number of editions exceeds ~500, or when multi-admin concurrent writes become a concern, migrate to SQLite:

| Current (v1.0)          | Future (v2.0)          |
|-------------------------|------------------------|
| `meta.json` per edition | `editions` table       |
| `data/admins.json`      | `admins` table         |
| In-memory Python dict   | SQLite query           |
| File write for updates  | SQL UPDATE transaction |

The API layer remains unchanged; only the data access layer needs updating.

# Security & Authentication Design
## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Draft                         |
| **Date**            | 2026-10-07                    |
| **Classification**  | Internal — Handle with Care   |

---

## 1. Security Overview

The portal has two distinct security surfaces:

| Surface              | Risk Level | Controls Applied                                      |
|----------------------|------------|-------------------------------------------------------|
| Public Portal (read) | Low        | Input sanitization, CSP headers, iframe sandboxing   |
| Admin Dashboard      | High       | Authentication, RBAC, CSRF, rate limiting, HTTPS     |

---

## 2. Authentication Design

### 2.1 Authentication Method
The portal uses **session-based authentication** (server-side sessions via Flask). There is no token-based (JWT) auth in v1.0, keeping the implementation simple and stateful.

### 2.2 Password Policy

| Rule                          | Requirement                                |
|-------------------------------|--------------------------------------------|
| Minimum length                | 8 characters                               |
| Must include                  | 1 uppercase, 1 lowercase, 1 digit, 1 special character (`!@#$%^&*`) |
| Maximum length                | 128 characters                             |
| Hashing algorithm             | **bcrypt** (work factor: 12)               |
| Storage                       | Only the hash is stored; plain text is NEVER stored |
| Transmission                  | Password submitted over HTTPS only; never logged |

### 2.3 Session Management

| Property             | Value                                     |
|----------------------|-------------------------------------------|
| Session type         | Server-side (Flask session with signed cookie) |
| Session expiry       | 60 minutes of inactivity                  |
| Cookie flags         | `HttpOnly=True`, `Secure=True` (production), `SameSite=Lax` |
| Secret key           | 32+ random bytes, stored in `.env`        |
| Secret key rotation  | Rotate annually or on suspected compromise |

### 2.4 Login Flow

```
1. Admin navigates to /admin/login
2. GET /admin/login → Flask renders login form with CSRF token
3. Admin submits username + password
4. POST /admin/login:
   a. Validate CSRF token
   b. Check rate limit (5 req / 15 min / IP)
   c. Look up username in admin store
   d. If found: bcrypt.check_password_hash(stored_hash, submitted_password)
   e. If match: create session { user_id, username, role, login_time }
   f. Redirect to /admin/dashboard
   g. If not match: increment fail counter; return generic "Invalid credentials" error
5. On each admin request: validate session exists and is not expired
```

> **Security Note:** Always return the SAME error message for wrong username and wrong password. Never hint which field is wrong.

### 2.5 Logout Flow

```
1. Admin clicks "Logout"
2. POST /admin/logout (CSRF token included)
3. Flask: session.clear()
4. Redirect to /admin/login
```

---

## 3. Authorization — Role-Based Access Control (RBAC)

### 3.1 Roles

| Role         | Description                                               |
|--------------|-----------------------------------------------------------|
| `visitor`    | Unauthenticated; read-only access to published editions  |
| `admin`      | Authenticated; can manage editions and metadata          |
| `super-admin`| Authenticated; all admin abilities + account management  |

### 3.2 Permission Matrix

| Action                              | Visitor | Admin | Super-Admin |
|-------------------------------------|---------|-------|-------------|
| Browse published editions           | ✅      | ✅    | ✅          |
| Read editions in iframe             | ✅      | ✅    | ✅          |
| Search editions                     | ✅      | ✅    | ✅          |
| View all editions (incl. unpublished)| ❌     | ✅    | ✅          |
| Publish / Unpublish an edition      | ❌      | ✅    | ✅          |
| Edit edition metadata               | ❌      | ✅    | ✅          |
| Trigger manual rescan               | ❌      | ✅    | ✅          |
| Create new admin account            | ❌      | ❌    | ✅          |
| Delete admin account                | ❌      | ❌    | ✅          |
| Edit another admin's account        | ❌      | ❌    | ✅          |

### 3.3 Route Protection Pattern (Flask)

```python
from functools import wraps
from flask import session, redirect, url_for, abort

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

def super_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'super-admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated
```

---

## 4. CSRF Protection

All state-changing requests (POST, PATCH, DELETE) MUST include a CSRF token.

### 4.1 Implementation
- Use `Flask-WTF` (`flask_wtf.csrf.CSRFProtect`).
- CSRF token is embedded in every admin form as a hidden field.
- For AJAX/Fetch requests, the token is sent in the `X-CSRFToken` header.
- Token is validated server-side before processing the request.

### 4.2 Frontend Pattern (JavaScript)
```javascript
// Read CSRF token from meta tag
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

fetch('/api/admin/editions/cs-2026', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken
  },
  body: JSON.stringify({ published: true })
});
```

### 4.3 Backend Pattern (Flask)
```html
<!-- In base admin template -->
<meta name="csrf-token" content="{{ csrf_token() }}">
```

---

## 5. Rate Limiting

Use `Flask-Limiter` to protect sensitive endpoints.

### 5.1 Rate Limit Rules

| Endpoint            | Limit                   | Response on breach              |
|---------------------|-------------------------|---------------------------------|
| `POST /admin/login` | 5 requests / 15 min / IP | HTTP 429 + lockout message    |
| `GET /api/editions` | 60 requests / min / IP  | HTTP 429                        |
| All admin API       | 100 requests / min / IP | HTTP 429                        |

### 5.2 Configuration
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/admin/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")
def admin_login():
    ...
```

---

## 6. HTTP Security Headers

All responses from the Flask application MUST include the following headers. Configure in a `@app.after_request` hook:

### 6.1 Headers Table

| Header                    | Value                                                                        | Purpose                                |
|---------------------------|------------------------------------------------------------------------------|----------------------------------------|
| `Content-Security-Policy` | See §6.2                                                                    | Prevent XSS                           |
| `X-Content-Type-Options`  | `nosniff`                                                                    | Prevent MIME sniffing                  |
| `X-Frame-Options`         | `SAMEORIGIN` (admin pages) / `DENY` (all others except reader)              | Prevent clickjacking                   |
| `Referrer-Policy`         | `strict-origin-when-cross-origin`                                            | Limit referrer info leakage            |
| `Strict-Transport-Security`| `max-age=63072000; includeSubDomains` (production HTTPS only)               | Enforce HTTPS                          |
| `Permissions-Policy`      | `camera=(), microphone=(), geolocation=()`                                   | Restrict browser feature access        |

### 6.2 Content Security Policy (CSP)

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data:;
  frame-src 'self';
  connect-src 'self';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
```

> **Note:** `frame-src 'self'` allows the portal to embed its own `/static/magazines/` content in the `<iframe>`. Sub-team content must not load external scripts that would violate this CSP.

### 6.3 Flask Implementation
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "frame-src 'self';"
    )
    return response
```

---

## 7. Sensitive Data & Secrets Management

### 7.1 .env File

The following secrets MUST be stored in `.env` and NEVER committed to git:

```env
# Flask Secret Key (generate with: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=<32+ random hex characters>

# Admin credential store path
ADMIN_STORE_PATH=data/admins.json

# Environment
FLASK_ENV=production

# (Optional) SMTP for future email notifications
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASS=
```

### 7.2 .gitignore Entries (Mandatory)

```gitignore
# Secrets
.env
data/admins.json
data/

# Python
__pycache__/
*.pyc
*.pyo
venv/
.venv/

# OS
.DS_Store
Thumbs.db
```

### 7.3 .env.example (Committed to Git)

```env
SECRET_KEY=replace-with-a-secure-random-key
ADMIN_STORE_PATH=data/admins.json
FLASK_ENV=development
```

---

## 8. Path Traversal Prevention

The scanner must never allow a crafted path to escape the `static/magazines/` directory.

### 8.1 Safe Path Validation Pattern

```python
import os

MAGAZINE_ROOT = os.path.realpath('static/magazines')

def is_safe_path(path: str) -> bool:
    """Check that the resolved path is within MAGAZINE_ROOT."""
    resolved = os.path.realpath(path)
    return resolved.startswith(MAGAZINE_ROOT)
```

All file reads performed by the scanner MUST pass through `is_safe_path()`. Any path that fails this check MUST be skipped and logged as a security warning.

---

## 9. Input Validation & Sanitization

### 9.1 meta.json Validation
- All fields validated against the canonical JSON schema on every scan.
- Reject editions with missing required fields or wrong data types.
- Log the error with the offending file path.

### 9.2 Admin Form Input
- All text inputs sanitized using `markupsafe.escape()` before being written to `meta.json`.
- Maximum field lengths enforced both client-side (HTML `maxlength`) and server-side.

### 9.3 URL Parameters
- `year` parameter must be a valid 4-digit integer (2000–2100).
- `category` must be one of the allowed enum values.
- Any other unexpected parameter is ignored.

---

## 10. Iframe Sandboxing

The `<iframe>` used to embed edition plugins should include a `sandbox` attribute to restrict plugin capabilities:

```html
<iframe
  id="edition-reader"
  src=""
  sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
  loading="lazy"
  title="Magazine Reader">
</iframe>
```

| Sandbox Flag          | Reason Allowed                                          |
|-----------------------|---------------------------------------------------------|
| `allow-scripts`       | Sub-team sites use JavaScript                          |
| `allow-same-origin`   | Allows the plugin to load its own sub-resources        |
| `allow-forms`         | Some editions may have interactive forms               |
| `allow-popups`        | Allow links to open in a new tab                       |

> **Omitted flags:** `allow-top-navigation` and `allow-modals` are intentionally omitted to prevent plugins from redirecting the parent portal or spawning JavaScript dialogs.

---

## 11. Incident Response Plan

| Incident                    | Immediate Action                                                  |
|-----------------------------|-------------------------------------------------------------------|
| Admin password leaked       | Disable account in `admins.json`, rotate `SECRET_KEY`, force re-login |
| `.env` accidentally committed | Immediately rotate all secrets, force-push to remove from git history, notify all contributors |
| XSS discovered in plugin    | Unpublish the edition immediately; fix CSP if needed; notify sub-team |
| Server compromise           | Take server offline, audit logs, reset all credentials           |

---

## 12. Security Checklist (Pre-Launch)

- [ ] `SECRET_KEY` is a 32+ byte random value stored in `.env`
- [ ] `.env` and `data/admins.json` are in `.gitignore`
- [ ] All admin passwords are bcrypt-hashed (work factor ≥ 12)
- [ ] CSRF protection enabled via Flask-WTF
- [ ] Rate limiting enabled on `/admin/login`
- [ ] All HTTP security headers configured
- [ ] HTTPS configured via Nginx in production
- [ ] Path traversal prevention active in scanner
- [ ] iframe sandbox attribute set on reader
- [ ] No debug mode (`FLASK_DEBUG=0`) in production
- [ ] No default credentials (change immediately after first deploy)
- [ ] Logs do not contain passwords or session tokens

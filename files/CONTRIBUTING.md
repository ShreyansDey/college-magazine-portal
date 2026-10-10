# Contributing Guide — Sub-Team Developer Handbook

## College Unified Magazine Portal

> **READ THIS ENTIRE DOCUMENT BEFORE TOUCHING ANY FILES.**
> Non-compliance will result in your PR being rejected.

---

## 1. Welcome, Sub-Team Developer

You are building a magazine "plugin" — a self-contained mini-website — that will be automatically discovered and displayed by the College Unified Magazine Portal. Your job is simple:

- Build a great magazine site using HTML, CSS, and JavaScript.
- Put it in the right folder with the right files.
- Submit a Pull Request (PR).

The portal takes care of everything else — hosting, discovery, navigation, and embedding.

---

## 2. Your Assignment

When you receive your assignment, you will be told:

| Info              | Example                      |
|-------------------|------------------------------|
| **Category**      | `departmental`               |
| **Your ID**       | `cs` (department) or `bhavan3` (hostel) |
| **Year**          | `2026`                       |
| **Your Directory**| `static/magazines/2026/departmental/cs/` |

This directory is **yours**. Do not touch any other directory.

---

## 3. The Hard Collar Contract (MANDATORY)

Your directory MUST contain exactly these two files at its root:

```
static/magazines/2026/departmental/cs/
├── index.html     ← MANDATORY: Main entry point of your magazine
├── meta.json      ← MANDATORY: Metadata for the portal to discover you
└── (your other files, folders, assets — anything you need)
```

**Without `index.html` and `meta.json`, your submission WILL BE REJECTED.**

---

## 4. The meta.json File

Create a file named `meta.json` in your root directory. Copy this template and fill in your details:

```json
{
  "id": "cs-2026",
  "title": "CS Department Journal 2026",
  "year": 2026,
  "category": "departmental",
  "sub_id": "cs",
  "description": "A brief description of your magazine (max 500 characters).",
  "cover_image": "cover.jpg",
  "tags": ["technology", "research"],
  "published": false,
  "published_date": null,
  "author_team": "CS Magazine Team 2026"
}
```

### Field Reference

| Field          | Type    | Required | Your Input                                                |
|----------------|---------|----------|-----------------------------------------------------------|
| `id`           | string  | ✅       | `<sub_id>-<year>` — must be unique, lowercase, hyphens OK |
| `title`        | string  | ✅       | Your magazine's full title                                |
| `year`         | integer | ✅       | Academic year (e.g. `2026`)                              |
| `category`     | string  | ✅       | `annual`, `departmental`, or `bhavan` — exactly as shown |
| `sub_id`       | string  | ✅       | Your assigned ID (e.g. `cs`, `bhavan3`). `null` for annual |
| `description`  | string  | ✅       | Short description of the magazine (max 500 chars)        |
| `cover_image`  | string  | ✅       | Filename of your cover image (must be in your directory) |
| `tags`         | array   | ✅       | Keywords array, e.g. `["art", "science"]`               |
| `published`    | boolean | ✅       | **Set to `false`** — admin will change this on approval  |
| `published_date`| string | No       | Leave `null` — admin sets this                           |
| `author_team`  | string  | ✅       | Your team's name                                         |

> ⚠️ **Important:** Set `"published": false` in your PR. The admin will set it to `true` after review.

---

## 5. Asset Path Rules (CRITICAL)

All paths inside your `index.html` MUST be **relative**, not absolute.

### ✅ Correct (Relative Paths)

```html
<link rel="stylesheet" href="css/style.css">
<script src="js/main.js"></script>
<img src="images/cover.jpg" alt="Cover">
<a href="pages/about.html">About</a>
```

### ❌ Wrong (Absolute Paths — Will Break)

```html
<link rel="stylesheet" href="/css/style.css">
<img src="/static/magazines/2026/departmental/cs/images/cover.jpg">
```

**Why?** Your magazine is embedded inside an `<iframe>`. The portal serves your files at a path like `/static/magazines/2026/departmental/cs/`. Absolute paths will break because they'll point to the portal's root, not your directory.

---

## 6. Allowed Technologies

| Technology              | Allowed? | Notes                                           |
|-------------------------|----------|-------------------------------------------------|
| HTML5                   | ✅ Yes   | Standard HTML                                   |
| CSS3 / SCSS (compiled)  | ✅ Yes   | Commit compiled CSS only                        |
| Vanilla JavaScript      | ✅ Yes   |                                                 |
| React / Vue / Alpine.js | ✅ Yes   | Commit the **built/compiled** files only        |
| Fonts (Google Fonts CDN)| ✅ Yes   | External CDN links allowed                      |
| Images (local)          | ✅ Yes   | Must be inside your directory                   |
| External APIs / Fetch   | ✅ Yes   | Must not require CORS credentials               |
| PHP / Python / Node.js  | ❌ No    | Server-side code not supported                  |
| `<script>` with eval()  | ❌ No    | Will fail CSP security policy                   |
| Inline event handlers   | ⚠️ Avoid | `onclick=""` etc. may fail CSP                  |

---

## 7. Cover Image Guidelines

- **Format:** JPG or PNG preferred; WebP also accepted
- **Recommended size:** 800×1100px (portrait, magazine cover ratio)
- **Max file size:** 2 MB for the cover image
- **Placement:** Must be inside your directory (e.g., `cover.jpg` at root)
- **Reference in meta.json:** Use just the filename — `"cover_image": "cover.jpg"`

---

## 8. File Size Limits

| Limit                | Value       |
|----------------------|-------------|
| Total edition size   | 50 MB       |
| Single cover image   | 2 MB        |
| Single JS/CSS file   | 5 MB        |
| Single video (if any)| 20 MB       |

If you need to include large assets, compress them. Videos should be self-hosted in your directory, not linked from YouTube (embeds are fine with `<iframe>` for videos).

---

## 9. Git Workflow — Step by Step

### Step 1 — Fork & Clone (if not yet done)

```bash
git clone https://github.com/<org>/college-magazine-portal.git
cd college-magazine-portal
```

### Step 2 — Create Your Branch

Name your branch: `<category>/<sub-id>/<year>`

```bash
git checkout -b departmental/cs/2026
```

### Step 3 — Build Your Magazine

Work inside your assigned directory only:

```
static/magazines/2026/departmental/cs/
```

### Step 4 — Validate Before Submitting

Run the validation script (if provided):

```bash
python tools/validate_edition.py static/magazines/2026/departmental/cs/
```

This checks:

- `index.html` exists
- `meta.json` exists and is valid
- `published` is `false`
- No absolute paths in `index.html`
- No files over size limits

### Step 5 — Commit Your Work

```bash
git add static/magazines/2026/departmental/cs/
git commit -m "feat: add CS department magazine 2026"
git push origin departmental/cs/2026
```

### Step 6 — Open a Pull Request

- Go to the GitHub repository.
- Click **"Compare & pull request"** for your branch.
- Title: `[Departmental] CS Magazine 2026`
- Description: Brief description + your team's contact.
- Request review from the admin.

---

## 10. PR Review Checklist (Admin Reviews These)

Your PR will be rejected if any of the following fail:

- [ ] Branch name follows convention: `<category>/<sub-id>/<year>`
- [ ] `index.html` exists at directory root
- [ ] `meta.json` exists at directory root and is valid JSON
- [ ] `meta.json` fields: `id`, `title`, `year`, `category`, `sub_id`, `description`, `cover_image`, `tags`, `author_team` all present
- [ ] `meta.json`: `published` is `false`
- [ ] All asset paths in `index.html` are relative
- [ ] No files modified outside your assigned directory
- [ ] Total directory size ≤ 50 MB
- [ ] Cover image file referenced in `meta.json` exists in the directory
- [ ] No server-side code included

---

## 11. Getting Help

| Issue                              | Contact                            |
|------------------------------------|------------------------------------|
| Assignment / which directory to use | Magazine Portal Admin             |
| Technical questions (git, HTML, CSS) | Core Dev Team / Discussion board |
| PR review taking too long          | Tag admin in your PR               |
| Found a bug in the portal itself   | Open an Issue on GitHub           |

---

## 12. Quick Reference — Starter Template

Your starter directory template is at:

```
static/magazines/TEMPLATE/
├── index.html   (minimal valid HTML page)
└── meta.json    (pre-filled template)
```

Copy it as a starting point:

```bash
cp -r static/magazines/TEMPLATE/ static/magazines/2026/departmental/cs/
```

Then customize!

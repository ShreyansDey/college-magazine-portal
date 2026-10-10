# UI/UX Design Guidelines

## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Draft                         |
| **Date**            | 2026-10-07                    |

---

## 1. Design Philosophy

| Principle           | Description                                                                   |
|---------------------|-------------------------------------------------------------------------------|
| **Content-First**   | Magazines are the hero. UI chrome is minimal and unobtrusive.                |
| **Zero Friction**   | A visitor should find and open any magazine in 3 clicks or fewer.            |
| **Familiar Patterns** | Use conventions readers know: library/catalog UI, bookshelf metaphors.      |
| **Accessible**      | All functionality must be keyboard-accessible and screen-reader-friendly.   |
| **Scalable Design** | Adding 50 more editions should not require design changes.                   |

---

## 2. Color Palette

### 2.1 Primary Brand Colors

| Token                  | Hex       | Usage                                       |
|------------------------|-----------|---------------------------------------------|
| `--color-primary`      | `#1A3C5E` | Headings, primary buttons, active states   |
| `--color-primary-light`| `#2D6A9F` | Hover states, links                        |
| `--color-accent`       | `#E8A020` | CTAs, highlights, year badges              |
| `--color-accent-light` | `#F5C86A` | Hover on accent elements                   |

### 2.2 Neutral Colors

| Token                  | Hex       | Usage                                       |
|------------------------|-----------|---------------------------------------------|
| `--color-background`   | `#F4F6F9` | Page background                            |
| `--color-surface`      | `#FFFFFF` | Card backgrounds, modals                   |
| `--color-surface-alt`  | `#EEF1F7` | Alternate row, sidebar backgrounds        |
| `--color-border`       | `#D1D9E0` | Card borders, dividers                     |
| `--color-text-primary` | `#1C2B3A` | Body text                                  |
| `--color-text-secondary`| `#5A6A7A` | Subtitles, helper text                    |
| `--color-text-muted`   | `#8A9AAB` | Placeholder text, disabled labels         |

### 2.3 Semantic Colors

| Token                  | Hex       | Usage                         |
|------------------------|-----------|-------------------------------|
| `--color-success`      | `#2E7D32` | Published badge, success toast|
| `--color-warning`      | `#E65100` | Unpublished badge, warnings   |
| `--color-error`        | `#C62828` | Error messages, delete actions|
| `--color-info`         | `#0277BD` | Info banners                  |

---

## 3. Typography

### 3.1 Font Stack

```css
/* Headings */
font-family: 'Playfair Display', 'Georgia', serif;

/* Body & UI */
font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;

/* Code / Monospace */
font-family: 'JetBrains Mono', 'Courier New', monospace;
```

Import from Google Fonts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
```

### 3.2 Type Scale

| Role              | Size     | Weight | Font              |
|-------------------|----------|--------|-------------------|
| Display / Hero    | 3rem     | 800    | Playfair Display  |
| H1 (Page title)   | 2rem     | 700    | Playfair Display  |
| H2 (Section)      | 1.5rem   | 700    | Playfair Display  |
| H3 (Card title)   | 1.125rem | 600    | Inter             |
| Body              | 1rem     | 400    | Inter             |
| Small / Caption   | 0.875rem | 400    | Inter             |
| Badge / Label     | 0.75rem  | 600    | Inter (uppercase) |

---

## 4. Spacing System

Use a base-8 spacing scale:

| Token          | Value  | Usage                           |
|----------------|--------|---------------------------------|
| `--space-1`    | 4px    | Tight internal padding          |
| `--space-2`    | 8px    | Button padding, small gaps      |
| `--space-3`    | 12px   | Card internal padding (compact) |
| `--space-4`    | 16px   | Standard element gap            |
| `--space-6`    | 24px   | Section dividers, card padding  |
| `--space-8`    | 32px   | Large section gaps              |
| `--space-12`   | 48px   | Page section margins            |
| `--space-16`   | 64px   | Hero padding                    |

---

## 5. Component Specifications

### 5.1 Edition Card

```
┌─────────────────────────────┐
│                             │  ← Cover image (aspect ratio 3:4)
│    COVER IMAGE              │     Height: 260px
│                             │     object-fit: cover
├─────────────────────────────┤
│  [Category Badge] [Year]    │  ← Row: badge + year tag
│  Edition Title              │  ← H3, max 2 lines, ellipsis
│  Author Team                │  ← small, muted color
│                             │
│  [  📖  Read Magazine  ]    │  ← CTA button, full width
└─────────────────────────────┘
```

| Property         | Value                                    |
|------------------|------------------------------------------|
| Card width       | 280px (grid-based, responsive)           |
| Border radius    | 12px                                     |
| Box shadow       | `0 2px 12px rgba(0,0,0,0.08)`           |
| Hover shadow     | `0 8px 24px rgba(0,0,0,0.15)` + `translateY(-4px)` |
| Transition       | `all 0.25s ease`                         |

### 5.2 Category Badge

```css
.badge {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.badge-annual       { background: #E3F2FD; color: #0D47A1; }
.badge-departmental { background: #F3E5F5; color: #6A1B9A; }
.badge-bhavan       { background: #E8F5E9; color: #1B5E20; }
```

### 5.3 Primary Button

```css
.btn-primary {
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.1s ease;
}
.btn-primary:hover { background: var(--color-primary-light); }
.btn-primary:active { transform: scale(0.98); }
.btn-primary:focus-visible { outline: 3px solid var(--color-accent); outline-offset: 2px; }
```

### 5.4 Filter Controls

- Year filter: `<select>` styled dropdown or segmented pill buttons
- Category filter: Tab bar (Annual | Departmental | Bhavan)
- Department / Bhavan filter: Secondary dropdown, visible only when "Departmental" or "Bhavan" tab is active

---

## 6. Page Layout

### 6.1 Landing Page Structure

```
┌──────────────────────────────────────────────────────┐
│                    HEADER / NAV                       │
│  [College Logo]          [Portal Name]   [Year]      │
├──────────────────────────────────────────────────────┤
│                    HERO SECTION                       │
│  Display title + subtitle + total edition count       │
├──────────────────────────────────────────────────────┤
│                   FILTER BAR                          │
│  [Annual] [Departmental] [Bhavan]    [Search box]    │
│           [Dept dropdown] [Year dropdown]             │
├──────────────────────────────────────────────────────┤
│                  EDITION GRID                         │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐            │
│  │ Card │  │ Card │  │ Card │  │ Card │            │
│  └──────┘  └──────┘  └──────┘  └──────┘            │
├──────────────────────────────────────────────────────┤
│                  READER PANE                          │
│  [Breadcrumb: Portal > CS Dept > 2026]               │
│  [Title bar]                    [✕ Close] [⛶ Full]  │
│  ┌────────────────────────────────────────────────┐  │
│  │                   <iframe>                      │  │
│  │              (magazine loads here)              │  │
│  └────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────┤
│                    FOOTER                             │
│  © 2026 College Name  |  Built by Magazine Portal Team│
└──────────────────────────────────────────────────────┘
```

### 6.2 Grid Layout

```css
.edition-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-6);
  padding: var(--space-8) 0;
}
```

### 6.3 Responsive Breakpoints

| Breakpoint   | Width        | Cards per Row |
|--------------|-------------|---------------|
| Mobile       | < 640px     | 1             |
| Tablet       | 640–1024px  | 2             |
| Desktop      | 1024–1440px | 3–4           |
| Wide         | > 1440px    | 4–5           |

---

## 7. Reader Pane (iframe Viewer)

| Property           | Value                                              |
|--------------------|---------------------------------------------------|
| Height             | `calc(100vh - 200px)` or min 600px               |
| Width              | 100% of content area                              |
| Border             | None (borderless)                                 |
| Slide-in animation | `translateY(40px) → translateY(0)` + fade-in     |
| Loading state      | Skeleton loader or spinner overlay until iframe fires `onload` |
| Close behavior     | Smooth fade out + return focus to the edition card |

---

## 8. Admin Dashboard UI

### 8.1 Layout

- Sidebar navigation (Edition List, Account Management, Settings)
- Main content area (table of editions)
- Status badges: `Published` (green), `Unpublished` (orange)
- Actions per row: Edit (pencil icon), Publish Toggle, Preview

### 8.2 Admin Color Overrides

| Token                     | Value     | Admin Context             |
|---------------------------|-----------|---------------------------|
| `--admin-sidebar-bg`      | `#1A2537` | Dark sidebar              |
| `--admin-sidebar-text`    | `#B0BEC5` | Sidebar nav links         |
| `--admin-sidebar-active`  | `#FFFFFF` | Active nav item           |
| `--admin-accent`          | `#3B82F6` | Admin CTA buttons         |

---

## 9. Micro-Animations Specification

| Interaction                     | Animation                                              | Duration |
|---------------------------------|--------------------------------------------------------|----------|
| Card hover                      | `translateY(-4px)` + shadow deepen                    | 250ms    |
| Edition card appear (on load)   | Staggered fade-in + slide-up from cards               | 400ms each, 50ms stagger |
| Filter change                   | Cards fade out → filter → fade in                     | 200ms    |
| Iframe slide-in (on edition click) | Slide up from below + fade in                       | 300ms    |
| Button click                    | `scale(0.98)` press effect                            | 100ms    |
| Toast notification              | Slide in from top-right → auto-dismiss after 3s      | 300ms    |

---

## 10. Accessibility Requirements

| Rule                    | Implementation                                                |
|-------------------------|---------------------------------------------------------------|
| Color contrast          | All text/background combos meet WCAG AA (4.5:1 minimum)     |
| Focus indicators        | Visible 3px outline (not removed with `outline: none`)       |
| Keyboard navigation     | Tab through all interactive elements in logical order        |
| Skip link               | "Skip to main content" link at top of page                   |
| Alt text                | All cover images have descriptive `alt` attributes           |
| ARIA roles              | `<nav>`, `<main>`, `<aside>` landmark regions used           |
| Screen reader           | Edition cards have `aria-label` with full edition title      |
| iframe title            | `<iframe title="Magazine Reader: [Edition Name]">`           |

---

## 11. Icon Guidelines

- Use a single icon library consistently — recommended: **Feather Icons** or **Phosphor Icons** (both MIT licensed, SVG-based, lightweight).
- Icons should be 20×20px for UI actions, 24×24px for navigation.
- Every icon-only button MUST have an `aria-label` attribute.
- Do not use emojis as functional UI icons (only decorative use is okay).

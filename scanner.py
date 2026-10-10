"""
scanner.py - Filesystem discovery and caching engine for Magazine Micro-Frontends.
Maintains the official institutional registry of all 20 college publications:
  - 1 College Annual Patrika
  - 5 Residential Hostel Bhavans
  - 14 Academic Departmental Journals
Integrates with filesystem editions in 'magazines/' for published micro-frontends.
"""

import os
import re
import json
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MAGAZINES_DIR = os.path.join(BASE_DIR, 'magazines')

_cache = []

# -----------------------------------------------------------------------------
# Canonical Registry of All 20 Official College Publications
# -----------------------------------------------------------------------------
OFFICIAL_PUBLICATIONS_REGISTRY = [
    # 1 Flagship Annual Patrika
    {
        'slug': 'vidyamandira-patrika',
        'academic_year': '2025-2026',
        'title': 'Vidyamandira Patrika',
        'category': 'Annual',
        'department': 'College Editorial Board',
        'description': 'The premier annual literary, philosophical, and scientific journal of Ramakrishna Mission Vidyamandira, embodying collegiate scholarship and character-building.',
        'tags': ['annual', 'patrika', 'literature', 'heritage', 'philosophy'],
        'featured': True,
        'published_at': '2026-01-12',
        'status': 'in-compilation'
    },

    # 5 Official Residential Hostel Bhavans
    {
        'slug': 'shree-bhavan',
        'academic_year': '2025-2026',
        'title': 'Shree Bhavan Patrika',
        'bengali': 'শ্রী ভবন',
        'category': 'Hostel',
        'department': 'Shree Bhavan',
        'description': 'Annual hostel gazette celebrating fraternal brotherhood, evening prayer chanting, and resident creative writing.',
        'tags': ['shree-bhavan', 'hostel', 'literature', 'creative'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'shraddha-bhavan',
        'academic_year': '2025-2026',
        'title': 'Shraddha Bhavan Patrika',
        'bengali': 'শ্রদ্ধা ভবন',
        'category': 'Hostel',
        'department': 'Shraddha Bhavan',
        'description': 'Residential hall gazette cultivating deep reverence, self-reliance, and contemplative writing.',
        'tags': ['shraddha-bhavan', 'hostel', 'essays', 'reverence'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'vivek-bhavan',
        'academic_year': '2025-2026',
        'title': 'Vivek Bhavan Patrika',
        'bengali': 'বিবেক ভবন',
        'category': 'Hostel',
        'department': 'Vivek Bhavan',
        'description': 'Hostel gazette named after Swami Vivekananda, featuring intellectual discourses and sports chronicles.',
        'tags': ['vivek-bhavan', 'hostel', 'vivekananda', 'youth'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'vinay-bhavan',
        'academic_year': '2025-2026',
        'title': 'Vinay Bhavan Patrika',
        'bengali': 'বিনয় ভবন',
        'category': 'Hostel',
        'department': 'Vinay Bhavan',
        'description': 'Annual hostel gazette exemplifying humility, character-building, and festival chronicles.',
        'tags': ['vinay-bhavan', 'hostel', 'service', 'culture'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'vidya-bhavan',
        'academic_year': '2025-2026',
        'title': 'Vidya Bhavan Patrika',
        'bengali': 'বিদ্যা ভবন',
        'category': 'Hostel',
        'department': 'Vidya Bhavan',
        'description': 'Residential hall gazette highlighting creative literature and scientific debates.',
        'tags': ['vidya-bhavan', 'hostel', 'debates', 'science'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },

    # 14 Official Academic Departments
    {
        'slug': 'cse-aura',
        'academic_year': '2025-2026',
        'title': 'CSE Aura',
        'category': 'Departmental',
        'department': 'Department of Computer Science and Electronics',
        'description': 'Advancements in Artificial Intelligence, distributed computing, algorithms, and student technical research.',
        'tags': ['computer-science', 'ai', 'algorithms', 'technology'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'physics-spectrum',
        'academic_year': '2025-2026',
        'title': 'Physics Spectrum',
        'category': 'Departmental',
        'department': 'Department of Physics',
        'description': 'Exploring quantum mechanics, classical electrodynamics, astrophysics, and laboratory monographs.',
        'tags': ['physics', 'quantum', 'science', 'astrophysics'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'rasayan-patrika',
        'academic_year': '2025-2026',
        'title': 'Rasayan Patrika',
        'category': 'Departmental',
        'department': 'Department of Chemistry',
        'description': 'Organic and inorganic synthesis, molecular dynamics, crystal structure analysis, and spectroscopic research.',
        'tags': ['chemistry', 'research', 'synthesis', 'spectroscopy'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'ganit-manjusha',
        'academic_year': '2025-2026',
        'title': 'Ganit Manjusha',
        'category': 'Departmental',
        'department': 'Department of Mathematics',
        'description': 'Pure and applied mathematics, algebra, analysis, topology, and discrete mathematical modeling.',
        'tags': ['mathematics', 'algebra', 'analysis', 'topology'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'biospectra',
        'academic_year': '2025-2026',
        'title': 'Biospectra',
        'category': 'Departmental',
        'department': 'Department of Microbiology',
        'description': 'Microbial genetics, immunology, environmental microbiology, and molecular biology.',
        'tags': ['microbiology', 'genetics', 'immunology', 'biology'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'fauna-chronicles',
        'academic_year': '2025-2026',
        'title': 'Fauna Chronicles',
        'category': 'Departmental',
        'department': 'Department of Zoology',
        'description': 'Biodiversity research, evolutionary biology, animal behavior, and comparative physiology.',
        'tags': ['zoology', 'biodiversity', 'ecology', 'physiology'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'arthik-samiksha',
        'academic_year': '2025-2026',
        'title': 'Arthik Samiksha',
        'category': 'Departmental',
        'department': 'Department of Economics',
        'description': 'Econometrics, macroeconomic policy, Indian economic development, and public finance.',
        'tags': ['economics', 'econometrics', 'policy', 'development'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'rasayan-shilpa',
        'academic_year': '2025-2026',
        'title': 'Rasayan Shilpa',
        'category': 'Departmental',
        'department': 'Department of Industrial Chemistry',
        'description': 'Applied chemistry, chemical technology, polymer synthesis, and material sciences (offering M.Sc Applied Chemistry).',
        'tags': ['industrial-chemistry', 'applied-chemistry', 'chemical-tech', 'materials'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'anwesha',
        'academic_year': '2025-2026',
        'title': 'Anwesha',
        'category': 'Departmental',
        'department': 'Department of Bengali',
        'description': 'Bengali literature, Rabindranath Tagore studies, poetry, cultural essays, and linguistics.',
        'tags': ['bengali', 'literature', 'tagore', 'culture'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'literary-horizons',
        'academic_year': '2025-2026',
        'title': 'Literary Horizons',
        'category': 'Departmental',
        'department': 'Department of English',
        'description': 'Literary criticism, world literature, poetry, and student creative writing monographs.',
        'tags': ['english', 'literature', 'criticism', 'poetry'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'surabharati',
        'academic_year': '2025-2026',
        'title': 'Surabharati',
        'category': 'Departmental',
        'department': 'Department of Sanskrit',
        'description': 'Vedic literature, Classical Sanskrit poetry, Indian philosophical schools, and grammar.',
        'tags': ['sanskrit', 'vedic', 'philosophy', 'grammar'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'itihas-darpan',
        'academic_year': '2025-2026',
        'title': 'Itihas Darpan',
        'category': 'Departmental',
        'department': 'Department of History',
        'description': 'Indian historical epochs, regional history of Bengal, and archival research studies.',
        'tags': ['history', 'bengal', 'archives', 'heritage'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'tattva-bodha',
        'academic_year': '2025-2026',
        'title': 'Tattva Bodha',
        'category': 'Departmental',
        'department': 'Department of Philosophy',
        'description': 'Advaita Vedanta, epistemology, Western logic, and Indian philosophical systems.',
        'tags': ['philosophy', 'vedanta', 'epistemology', 'logic'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    },
    {
        'slug': 'lokneeti',
        'academic_year': '2025-2026',
        'title': 'Lokneeti',
        'category': 'Departmental',
        'department': 'Department of Political Science',
        'description': 'Indian constitutional studies, comparative politics, political theory, and governance.',
        'tags': ['political-science', 'constitution', 'governance', 'policy'],
        'featured': False,
        'published_at': '2026',
        'status': 'in-compilation'
    }
]

# 5 Official Residential Bhavans of Ramakrishna Mission Vidyamandira
OFFICIAL_BHAVANS = [
    {
        'slug': 'shree-bhavan',
        'name': 'Shree Bhavan',
        'bengali': 'শ্রী ভবন',
        'motto': 'Shraddha & Seva',
        'established': '1941',
        'description': 'One of the founding residential halls of Vidyamandira, fostering fraternal brotherhood, evening prayer chanting, and literary wall magazines.'
    },
    {
        'slug': 'shraddha-bhavan',
        'name': 'Shraddha Bhavan',
        'bengali': 'শ্রদ্ধা ভবন',
        'motto': 'Reverence & Knowledge',
        'established': '1945',
        'description': 'Residential hall dedicated to cultivating deep reverence, self-reliance, and contemplative writing among student scholars.'
    },
    {
        'slug': 'vivek-bhavan',
        'name': 'Vivek Bhavan',
        'bengali': 'বিবেক ভবন',
        'motto': 'Strength & Truth',
        'established': '1955',
        'description': 'Named after Swami Vivekananda, serving as an energetic center for intellectual discussions, athletic chronicles, and cultural gazettes.'
    },
    {
        'slug': 'vinay-bhavan',
        'name': 'Vinay Bhavan',
        'bengali': 'বিনয় ভবন',
        'motto': 'Humility & Character',
        'established': '1962',
        'description': 'Exemplifying humility and scholarly perseverance, publishing annual hostel gazettes and festival memorial issues.'
    },
    {
        'slug': 'vidya-bhavan',
        'name': 'Vidya Bhavan',
        'bengali': 'বিদ্যা ভবন',
        'motto': 'Wisdom & Light',
        'established': '1970',
        'description': 'Residential hall celebrating creative literature, scientific debates, and residential fraternal bonding.'
    }
]

# 14 Official Academic Departments of Ramakrishna Mission Vidyamandira
# Categorized according to official college administration:
# 8 Science Departments + 6 Humanities & Social Science Departments
OFFICIAL_DEPARTMENTS = [
    # --- Science Departments (8) ---
    {
        'slug': 'physics',
        'name': 'Department of Physics',
        'faculty': 'Science',
        'journal_name': 'Physics Spectrum',
        'description': 'Exploring quantum mechanics, classical electrodynamics, astrophysics, and laboratory monographs.'
    },
    {
        'slug': 'chemistry',
        'name': 'Department of Chemistry',
        'faculty': 'Science',
        'journal_name': 'Rasayan Patrika',
        'description': 'Applied chemistry, organic synthesis, crystal structure analysis, and spectroscopy.'
    },
    {
        'slug': 'mathematics',
        'name': 'Department of Mathematics',
        'faculty': 'Science',
        'journal_name': 'Ganit Manjusha',
        'description': 'Pure and applied mathematics, algebra, analysis, topology, and discrete mathematical modeling.'
    },
    {
        'slug': 'microbiology',
        'name': 'Department of Microbiology',
        'faculty': 'Science',
        'journal_name': 'Biospectra',
        'description': 'Microbial genetics, immunology, environmental microbiology, and molecular biology.'
    },
    {
        'slug': 'computer-science',
        'name': 'Department of Computer Science and Electronics',
        'faculty': 'Science',
        'journal_name': 'CSE Aura',
        'description': 'Advancements in Artificial Intelligence, distributed computing, algorithms, and electronics research.'
    },
    {
        'slug': 'industrial-chemistry',
        'name': 'Department of Industrial Chemistry',
        'faculty': 'Science',
        'journal_name': 'Rasayan Shilpa',
        'description': 'Specialized research in applied chemistry, chemical technology, polymer synthesis, and material sciences (offering M.Sc Applied Chemistry).'
    },
    {
        'slug': 'economics',
        'name': 'Department of Economics',
        'faculty': 'Science',
        'journal_name': 'Arthik Samiksha',
        'description': 'Econometrics, macroeconomic policy, Indian economic development, and public finance.'
    },
    {
        'slug': 'zoology',
        'name': 'Department of Zoology',
        'faculty': 'Science',
        'journal_name': 'Fauna Chronicles',
        'description': 'Biodiversity research, evolutionary biology, animal behavior, and comparative physiology.'
    },

    # --- Humanities & Social Science Departments (6) ---
    {
        'slug': 'bengali',
        'name': 'Department of Bengali',
        'faculty': 'Humanities & Social Sciences',
        'journal_name': 'Anwesha',
        'description': 'Bengali literature, Rabindranath Tagore studies, poetry, cultural essays, and linguistics.'
    },
    {
        'slug': 'english',
        'name': 'Department of English',
        'faculty': 'Humanities & Social Sciences',
        'journal_name': 'Literary Horizons',
        'description': 'Literary criticism, world literature, poetry, and student creative writing.'
    },
    {
        'slug': 'sanskrit',
        'name': 'Department of Sanskrit',
        'faculty': 'Humanities & Social Sciences',
        'journal_name': 'Surabharati',
        'description': 'Vedic literature, Classical Sanskrit poetry, Indian philosophical schools, and grammar.'
    },
    {
        'slug': 'history',
        'name': 'Department of History',
        'faculty': 'Humanities & Social Sciences',
        'journal_name': 'Itihas Darpan',
        'description': 'Indian historical epochs, regional history of Bengal, and archival research studies.'
    },
    {
        'slug': 'philosophy',
        'name': 'Department of Philosophy',
        'faculty': 'Humanities & Social Sciences',
        'journal_name': 'Tattva Bodha',
        'description': 'Advaita Vedanta, epistemology, Western logic, and Indian philosophical systems.'
    },
    {
        'slug': 'political-science',
        'name': 'Department of Political Science',
        'faculty': 'Humanities & Social Sciences',
        'journal_name': 'Lokneeti',
        'description': 'Indian constitutional studies, comparative politics, political theory, and governance.'
    }
]

def scan_magazines(force_reload=False):
    """
    Scans the magazines directory and populates the complete institutional catalogue.
    Ensures all 20 official college publications (1 Annual, 5 Bhavans, 14 Departments)
    are available with standardized metadata.
    """
    global _cache

    # 1. Build map of canonical publications
    catalog_map = {}
    for item in OFFICIAL_PUBLICATIONS_REGISTRY:
        key = f"{item['academic_year']}:{item['slug']}"
        catalog_map[key] = {
            'slug': item['slug'],
            'academic_year': item['academic_year'],
            'title': item['title'],
            'category': item['category'],
            'department': item['department'],
            'description': item['description'],
            'cover_image': '',
            'cover_url': '',
            'tags': list(item['tags']),
            'featured': item.get('featured', False),
            'published_at': item.get('published_at', '2026'),
            'status': item.get('status', 'in-compilation'),
            'uploaded_by_admin': False,
            'has_reader': False,
            'entrypoint': f"/magazines/{item['academic_year']}/{item['slug']}/index.html",
            'read_url': f"/read/{item['academic_year']}/{item['slug']}"
        }

    # 2. Check filesystem for uploaded editions and override/enrich
    if os.path.exists(MAGAZINES_DIR):
        for year_entry in sorted(os.listdir(MAGAZINES_DIR), reverse=True):
            if not re.match(r'^\d{4}-\d{4}$', year_entry):
                continue
            year_path = os.path.join(MAGAZINES_DIR, year_entry)
            if not os.path.isdir(year_path):
                continue

            for slug_entry in sorted(os.listdir(year_path)):
                # Ignore sarada-bhavan if remnant exists
                if slug_entry == 'sarada-bhavan':
                    continue

                edition_path = os.path.join(year_path, slug_entry)
                if not os.path.isdir(edition_path):
                    continue

                meta_file = os.path.join(edition_path, 'meta.json')
                meta = {}
                if os.path.exists(meta_file):
                    try:
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            meta = json.load(f)
                    except Exception as e:
                        logger.error(f"Error parsing {meta_file}: {e}")

                key = f"{year_entry}:{slug_entry}"
                target = catalog_map.get(key)
                if not target:
                    # An archive or additional edition found on disk
                    target = {
                        'slug': slug_entry,
                        'academic_year': meta.get('academic_year', year_entry),
                        'title': meta.get('title', slug_entry.replace('-', ' ').title()),
                        'category': meta.get('category', 'Departmental'),
                        'department': meta.get('department', 'Student Editorial Committee'),
                        'description': meta.get('description', 'Student publication at Ramakrishna Mission Vidyamandira.'),
                        'cover_image': '',
                        'cover_url': '',
                        'tags': meta.get('tags', []),
                        'featured': meta.get('featured', False),
                        'published_at': meta.get('published_at', ''),
                        'status': 'in-compilation',
                        'entrypoint': f"/magazines/{year_entry}/{slug_entry}/index.html",
                        'read_url': f"/read/{year_entry}/{slug_entry}"
                    }
                    catalog_map[key] = target

                # Apply meta overrides if present
                if meta.get('title'):
                    target['title'] = meta['title']
                if meta.get('description'):
                    target['description'] = meta['description']
                if meta.get('department'):
                    target['department'] = meta['department']
                if meta.get('tags'):
                    target['tags'] = meta['tags']

                # Check admin upload flag from meta.json
                target['uploaded_by_admin'] = bool(meta.get('uploaded_by_admin', False))

                # Check if real micro-frontend index.html exists and is not a dummy placeholder
                index_file = os.path.join(edition_path, 'index.html')
                has_valid_reader = False
                if os.path.exists(index_file) and os.path.getsize(index_file) > 0:
                    try:
                        with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
                            snippet = f.read(500)
                        if 'Pre-press In Compilation' not in snippet:
                            has_valid_reader = True
                    except Exception:
                        has_valid_reader = True

                if has_valid_reader:
                    target['has_reader'] = True
                    target['status'] = 'published'
                else:
                    target['has_reader'] = False
                    target['status'] = 'in-compilation'

                # Check if real cover file exists on disk
                cover_name = meta.get('cover_image', 'cover.jpg')
                full_cover_file = os.path.join(edition_path, cover_name)
                if cover_name and os.path.exists(full_cover_file):
                    mtime_ts = int(os.path.getmtime(full_cover_file))
                    target['cover_image'] = cover_name
                    target['cover_url'] = f"/magazines/{year_entry}/{slug_entry}/{cover_name}?v={mtime_ts}"

    # Sort: Featured first, then Annual, Departmental, Hostel
    def sort_key(item):
        cat_order = {'Annual': 0, 'Departmental': 1, 'Hostel': 2}
        return (
            0 if item.get('featured') else 1,
            cat_order.get(item.get('category'), 3),
            item.get('title')
        )

    magazines = sorted(catalog_map.values(), key=sort_key)
    _cache = magazines
    return _cache

OFFICIAL_ACADEMIC_SESSIONS = ['2025-2026', '2024-2025']

def get_filter_options():
    """Extract distinct academic years and categories from available magazines."""
    magazines = scan_magazines()
    years_set = set(m['academic_year'] for m in magazines)
    for session in OFFICIAL_ACADEMIC_SESSIONS:
        years_set.add(session)
    years = sorted(list(years_set), reverse=True)
    categories = ['Annual', 'Departmental', 'Hostel']
    return years, categories

def get_bhavans():
    """Returns official Bhavans decorated with associated magazines."""
    magazines = scan_magazines()
    bhavans = []
    for b in OFFICIAL_BHAVANS:
        b_copy = dict(b)
        b_slug_clean = b['slug'].replace('-bhavan', '')
        b_mags = [
            m for m in magazines
            if m['category'] == 'Hostel' and (
                b['slug'] == m['slug'] or
                b_slug_clean in m['slug'] or
                b['name'].lower() in m['department'].lower() or
                b['name'].lower() in m['title'].lower()
            )
        ]
        b_copy['magazines'] = b_mags
        b_copy['count'] = len(b_mags)
        bhavans.append(b_copy)
    return bhavans

DEPT_SLUG_TO_MAG_SLUG = {
    'physics': 'physics-spectrum',
    'chemistry': 'rasayan-patrika',
    'mathematics': 'ganit-manjusha',
    'microbiology': 'biospectra',
    'computer-science': 'cse-aura',
    'industrial-chemistry': 'rasayan-shilpa',
    'economics': 'arthik-samiksha',
    'zoology': 'fauna-chronicles',
    'bengali': 'anwesha',
    'english': 'literary-horizons',
    'sanskrit': 'surabharati',
    'history': 'itihas-darpan',
    'philosophy': 'tattva-bodha',
    'political-science': 'lokneeti'
}

def get_departments():
    """Returns official Departments decorated with associated journals."""
    magazines = scan_magazines()
    departments = []
    for d in OFFICIAL_DEPARTMENTS:
        d_copy = dict(d)
        target_slug = DEPT_SLUG_TO_MAG_SLUG.get(d['slug'], '')
        d_mags = [
            m for m in magazines
            if m['category'] == 'Departmental' and (
                m['slug'] == target_slug or
                d['journal_name'].lower() in m['title'].lower() or
                d['slug'] == m['slug']
            )
        ]
        d_copy['magazines'] = d_mags
        d_copy['count'] = len(d_mags)
        departments.append(d_copy)
    return departments

def get_annual_publications():
    """Returns all College Annual Patrika publications."""
    magazines = scan_magazines()
    return [m for m in magazines if m['category'] == 'Annual']

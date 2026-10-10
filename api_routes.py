"""
api_routes.py - REST JSON API Endpoints for the Magazine Portal.
Implements the specifications defined in files/API_DESIGN.md:
  - Public read-only endpoints: /api/editions, /api/editions/<id>, /api/years, /api/categories
  - Admin management endpoints: /api/admin/editions, /api/admin/editions/<id>, /api/admin/rescan
  - Super-Admin accounts API: /api/admin/accounts
"""

import os
import json
import re
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, session
from scanner import (
    scan_magazines, get_filter_options, get_departments, get_bhavans,
    get_annual_publications, BASE_DIR, MAGAZINES_DIR
)
from auth import login_required, super_admin_required, list_all_admins, create_admin, delete_admin

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')

# -----------------------------------------------------------------------------
# 1. Public API Endpoints
# -----------------------------------------------------------------------------

@api_bp.route('/editions', methods=['GET'])
def get_editions():
    """
    GET /api/editions
    Returns a list of published magazines with optional filtering by:
      - year (e.g. '2025-2026' or '2026')
      - category ('annual', 'departmental', 'bhavan', 'hostel')
      - sub_id (e.g. 'cs', 'cse-aura', 'shree-bhavan')
    """
    year = request.args.get('year', '').strip()
    category = request.args.get('category', '').strip().lower()
    sub_id = request.args.get('sub_id', '').strip().lower()

    valid_categories = {'annual', 'departmental', 'bhavan', 'hostel'}
    if category and category not in valid_categories:
        return jsonify({
            'status': 'error',
            'message': 'Invalid category value. Must be one of: annual, departmental, bhavan, hostel.'
        }), 400

    magazines = scan_magazines()

    # Filter logic
    filtered = []
    for mag in magazines:
        # 1. Year filter
        if year:
            mag_year = mag.get('academic_year', '')
            if year not in mag_year:
                continue

        # 2. Category filter
        if category:
            cat_norm = mag.get('category', '').lower()
            if category in ('bhavan', 'hostel'):
                if cat_norm not in ('bhavan', 'hostel'):
                    continue
            elif cat_norm != category:
                continue

        # 3. Sub-id filter
        if sub_id:
            slug = mag.get('slug', '').lower()
            dept = mag.get('department', '').lower()
            if sub_id not in slug and sub_id not in dept:
                continue

        filtered.append(mag)

    return jsonify({
        'status': 'success',
        'count': len(filtered),
        'data': filtered
    }), 200


@api_bp.route('/editions/<edition_id>', methods=['GET'])
def get_edition_by_id(edition_id):
    """
    GET /api/editions/<id>
    Returns detailed metadata for a specific publication edition.
    Matches by slug or academic_year:slug compound identifier.
    """
    target = edition_id.strip().lower()
    magazines = scan_magazines()

    matched = None
    for mag in magazines:
        compound_id = f"{mag.get('slug', '')}-{mag.get('academic_year', '')}".lower()
        if mag.get('slug', '').lower() == target or compound_id == target:
            matched = mag
            break

    if not matched:
        return jsonify({
            'status': 'error',
            'message': f"Edition '{edition_id}' not found."
        }), 404

    return jsonify({
        'status': 'success',
        'data': matched
    }), 200


@api_bp.route('/years', methods=['GET'])
def get_years():
    """
    GET /api/years
    Returns a sorted list of all active academic sessions.
    """
    years, _ = get_filter_options()
    return jsonify({
        'status': 'success',
        'data': years
    }), 200


@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    GET /api/categories
    Returns available publication categories with publication counts and sub_ids.
    """
    magazines = scan_magazines()
    annual_count = sum(1 for m in magazines if m.get('category') == 'Annual')
    dept_count = sum(1 for m in magazines if m.get('category') == 'Departmental')
    bhavan_count = sum(1 for m in magazines if m.get('category') in ('Hostel', 'Bhavan'))

    dept_sub_ids = [d.get('slug') for d in get_departments()]
    bhavan_sub_ids = [b.get('slug') for b in get_bhavans()]

    return jsonify({
        'status': 'success',
        'data': {
            'annual': {
                'count': annual_count
            },
            'departmental': {
                'count': dept_count,
                'sub_ids': dept_sub_ids
            },
            'bhavan': {
                'count': bhavan_count,
                'sub_ids': bhavan_sub_ids
            }
        }
    }), 200


# -----------------------------------------------------------------------------
# 2. Admin API Endpoints (Session Authentication Required)
# -----------------------------------------------------------------------------

@api_bp.route('/admin/editions', methods=['GET'])
@login_required
def admin_get_editions():
    """
    GET /api/admin/editions
    Returns all publications and compilation status records.
    """
    magazines = scan_magazines()
    return jsonify({
        'status': 'success',
        'count': len(magazines),
        'data': magazines
    }), 200


@api_bp.route('/admin/editions/<edition_id>', methods=['PATCH'])
@login_required
def admin_patch_edition(edition_id):
    """
    PATCH /api/admin/editions/<id>
    Partially updates publication metadata (title, description, tags, etc.)
    and saves to its respective meta.json.
    """
    payload = request.get_json(silent=True) or {}

    # Reject attempts to modify immutable session year
    if 'year' in payload or 'academic_year' in payload:
        return jsonify({
            'status': 'error',
            'message': "Invalid field: 'year' cannot be modified via API."
        }), 400

    target = edition_id.strip().lower()
    magazines = scan_magazines()

    matched = None
    for mag in magazines:
        compound_id = f"{mag.get('slug', '')}-{mag.get('academic_year', '')}".lower()
        if mag.get('slug', '').lower() == target or compound_id == target:
            matched = mag
            break

    if not matched:
        return jsonify({
            'status': 'error',
            'message': f"Edition '{edition_id}' not found."
        }), 404

    # Locate edition folder
    year = matched.get('academic_year', '2025-2026')
    slug = matched.get('slug', '')
    edition_dir = os.path.join(MAGAZINES_DIR, year, slug)
    os.makedirs(edition_dir, exist_ok=True)
    meta_path = os.path.join(edition_dir, 'meta.json')

    # Read existing or create new
    meta_data = {}
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta_data = json.load(f)
        except Exception:
            meta_data = {}

    # Allowable fields to patch
    updatable_fields = ['title', 'description', 'department', 'category', 'tags', 'published', 'status', 'cover_image']
    for field in updatable_fields:
        if field in payload:
            meta_data[field] = payload[field]

    meta_data['academic_year'] = year
    meta_data['updated_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    try:
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, indent=2)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Failed to save metadata: {str(e)}"
        }), 500

    # Invalidate and reload cache
    scan_magazines(force_reload=True)

    return jsonify({
        'status': 'success',
        'message': f"Edition '{edition_id}' updated successfully.",
        'data': meta_data
    }), 200


@api_bp.route('/admin/rescan', methods=['POST'])
@login_required
def admin_rescan():
    """
    POST /api/admin/rescan
    Forces the scanner engine to reload all filesystem directories and refresh cache.
    """
    try:
        updated = scan_magazines(force_reload=True)
        published_count = sum(1 for m in updated if m.get('has_reader'))
        return jsonify({
            'status': 'success',
            'message': f"Rescan complete. {len(updated)} publications indexed ({published_count} published).",
            'scanned_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'total': len(updated),
            'published': published_count,
            'in_compilation': len(updated) - published_count
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Rescan failed: {str(e)}"
        }), 500


# -----------------------------------------------------------------------------
# 3. Super-Admin Accounts Management API (Super-Admin Role Required)
# -----------------------------------------------------------------------------

@api_bp.route('/admin/accounts', methods=['GET'])
@super_admin_required
def get_admin_accounts():
    """
    GET /api/admin/accounts
    Returns list of all administrators without password hashes. Super-admin only.
    """
    admins = list_all_admins()
    return jsonify({
        'status': 'success',
        'count': len(admins),
        'data': admins
    }), 200


@api_bp.route('/admin/accounts', methods=['POST'])
@super_admin_required
def create_admin_account():
    """
    POST /api/admin/accounts
    Creates a new administrator account with bcrypt hashed password. Super-admin only.
    """
    payload = request.get_json(silent=True) or {}
    username = payload.get('username', '').strip()
    password = payload.get('password', '').strip()
    role = payload.get('role', 'admin').strip().lower()

    if not username or not password:
        return jsonify({
            'status': 'error',
            'message': 'Username (email) and password are required.'
        }), 400

    if len(password) < 8:
        return jsonify({
            'status': 'error',
            'message': 'Password must be at least 8 characters long.'
        }), 400

    success, result = create_admin(username, password, role)
    if not success:
        return jsonify({
            'status': 'error',
            'message': result
        }), 400

    # Strip hash from response
    safe_result = dict(result)
    safe_result.pop('password_hash', None)

    return jsonify({
        'status': 'success',
        'message': f"Admin account '{username}' created successfully.",
        'data': safe_result
    }), 201


@api_bp.route('/admin/accounts/<identifier>', methods=['DELETE'])
@super_admin_required
def delete_admin_account(identifier):
    """
    DELETE /api/admin/accounts/<id_or_username>
    Removes an administrator account. Super-admin only.
    """
    current_admin = session.get('admin_email', '').strip().lower()
    if str(identifier).strip().lower() == current_admin:
        return jsonify({
            'status': 'error',
            'message': 'Security restriction: You cannot delete your own active administrator account.'
        }), 400

    success, message = delete_admin(identifier)
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 404

    return jsonify({
        'status': 'success',
        'message': message
    }), 200

"""
admin_routes.py - Admin Portal Blueprint: 2FA Authentication, Dashboard & ZIP Uploader.
"""

import os
import json
import time
import io
import shutil
import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from auth import (
    get_admin_by_email, verify_password, issue_otp_for_admin,
    verify_otp_for_admin, login_required, super_admin_required,
    ADMIN_STORE_PATH
)
from uploader import install_magazine_zip, generate_starter_kit
from scanner import scan_magazines, get_filter_options

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# In-memory IP rate limiter: { ip: [timestamp1, timestamp2, ...] }
_login_attempts = {}

def is_rate_limited(ip, max_attempts=5, window_seconds=900):
    now = time.time()
    attempts = _login_attempts.get(ip, [])
    # Filter attempts within window (15 minutes)
    valid_attempts = [t for t in attempts if now - t < window_seconds]
    _login_attempts[ip] = valid_attempts
    return len(valid_attempts) >= max_attempts

def record_failed_attempt(ip):
    now = time.time()
    attempts = _login_attempts.get(ip, [])
    attempts.append(now)
    _login_attempts[ip] = attempts

@admin_bp.route('/')
def index():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_bp.dashboard'))
    return redirect(url_for('admin_bp.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_bp.dashboard'))

    client_ip = request.remote_addr or '127.0.0.1'

    if request.method == 'POST':
        if is_rate_limited(client_ip):
            flash("Too many failed sign-in attempts. Please try again after 15 minutes.", "danger")
            return render_template('admin/login.html')

        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash("Please enter both email address and password.", "danger")
            return render_template('admin/login.html')

        admin = get_admin_by_email(email)
        if not admin or not verify_password(password, admin.get('password_hash', '')):
            record_failed_attempt(client_ip)
            # Use generic error message as required by files/SECURITY.md
            flash("Invalid email or password. Please verify your credentials.", "danger")
            return render_template('admin/login.html')

        # Credentials valid: issue 6-digit OTP
        success, msg = issue_otp_for_admin(email)
        session['pending_admin_email'] = email

        if success:
            flash("Security code sent! Please check your email inbox to complete sign-in.", "success")
        else:
            flash("Notice: Security code generated. Check email or console logs.", "info")

        return redirect(url_for('admin_bp.verify_otp'))

    return render_template('admin/login.html')

@admin_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    pending_email = session.get('pending_admin_email')
    if not pending_email:
        flash("Please log in with your credentials first.", "warning")
        return redirect(url_for('admin_bp.login'))

    # Mask email for display: e.g. sh***06@gmail.com
    parts = pending_email.split('@')
    name = parts[0]
    domain = parts[1] if len(parts) > 1 else ''
    masked = name[:2] + '***' + (name[-2:] if len(name) > 3 else '') + '@' + domain

    if request.method == 'POST':
        entered_code = request.form.get('otp', '').strip()

        # Handle concatenated multi-box inputs if sent as digits
        if not entered_code:
            digits = [request.form.get(f'digit{i}', '') for i in range(1, 7)]
            entered_code = ''.join(digits).strip()

        if not entered_code:
            flash("Please enter the 6-digit verification code.", "danger")
            return render_template('admin/verify_otp.html', masked_email=masked)

        valid, error = verify_otp_for_admin(pending_email, entered_code)
        if not valid:
            flash(error or "Invalid verification code.", "danger")
            return render_template('admin/verify_otp.html', masked_email=masked)

        # Successful verification: promote to active session
        admin = get_admin_by_email(pending_email)
        session.pop('pending_admin_email', None)
        session['admin_logged_in'] = True
        session['admin_email'] = pending_email
        session['admin_role'] = admin.get('role', 'admin')
        session['admin_user_id'] = admin.get('id', 1)
        session.permanent = True

        # Update last_login timestamp in data/admins.json
        try:
            if os.path.exists(ADMIN_STORE_PATH):
                with open(ADMIN_STORE_PATH, 'r', encoding='utf-8') as f:
                    admins = json.load(f)
                for a in admins:
                    if a.get('username', '').lower() == pending_email.lower():
                        a['last_login'] = datetime.utcnow().isoformat() + 'Z'
                with open(ADMIN_STORE_PATH, 'w', encoding='utf-8') as f:
                    json.dump(admins, f, indent=2)
        except Exception as e:
            print(f"[AUTH WARNING] Failed to update last_login: {e}")

        flash(f"Welcome back, {pending_email}! Signed in successfully.", "success")
        return redirect(url_for('admin_bp.dashboard'))

    return render_template('admin/verify_otp.html', masked_email=masked)

@admin_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    pending_email = session.get('pending_admin_email')
    if not pending_email:
        flash("Session expired. Please sign in again.", "warning")
        return redirect(url_for('admin_bp.login'))

    success, msg = issue_otp_for_admin(pending_email)
    flash("A fresh verification code has been dispatched to your email.", "info")
    return redirect(url_for('admin_bp.verify_otp'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    magazines = scan_magazines()
    years, categories = get_filter_options()

    # Partition magazines by category
    bhavan_mags = [m for m in magazines if m.get('category') == 'Hostel']
    dept_mags = [m for m in magazines if m.get('category') == 'Departmental']
    annual_mags = [m for m in magazines if m.get('category') == 'Annual']

    return render_template(
        'admin/dashboard.html',
        magazines=magazines,
        bhavan_mags=bhavan_mags,
        dept_mags=dept_mags,
        annual_mags=annual_mags,
        years=years,
        categories=categories,
        admin_email=session.get('admin_email'),
        admin_role=session.get('admin_role')
    )

@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload_magazine():
    if 'zip_file' not in request.files:
        flash("No archive file selected for upload.", "danger")
        return redirect(url_for('admin_bp.dashboard'))

    file = request.files['zip_file']
    if not file or file.filename == '':
        flash("Please select a valid .zip file.", "danger")
        return redirect(url_for('admin_bp.dashboard'))

    category = request.form.get('category', 'Departmental')
    academic_year = request.form.get('academic_year', '2025-2026')
    slug = request.form.get('slug', '').strip().lower()

    # Custom slug if provided
    custom_slug = request.form.get('custom_slug', '').strip().lower()
    if custom_slug:
        slug = custom_slug

    title = request.form.get('title', '').strip()
    department = request.form.get('department', '').strip()
    description = request.form.get('description', '').strip()

    if not slug:
        flash("Please specify a target publication identifier (slug).", "danger")
        return redirect(url_for('admin_bp.dashboard'))

    success, message, preview_url = install_magazine_zip(
        zip_file_storage=file,
        academic_year=academic_year,
        slug=slug,
        title=title,
        category=category,
        department=department,
        description=description
    )

    if success:
        flash(f"{message} View live at: {preview_url}", "success")
    else:
        flash(message, "danger")

    return redirect(url_for('admin_bp.dashboard'))

@admin_bp.route('/download-starter-kit')
@login_required
def download_starter_kit():
    """Provides student editorial teams with a clean starter ZIP kit."""
    zip_bytes = generate_starter_kit()
    return send_file(
        io.BytesIO(zip_bytes),
        mimetype='application/zip',
        as_attachment=True,
        download_name='vidyamandira-student-edition-template.zip'
    )

@admin_bp.route('/delete/<year>/<slug>', methods=['POST'])
@login_required
def delete_edition(year, slug):
    """
    Safely removes uploaded edition files from the filesystem and resets
    the publication status back to 'In Compilation'.
    """
    # Strict validation to prevent directory traversal
    if not re.match(r'^[a-zA-Z0-9_\-]+$', year) or not re.match(r'^[a-zA-Z0-9_\-]+$', slug):
        flash("Invalid edition identifiers specified.", "danger")
        return redirect(url_for('admin_bp.dashboard'))

    base_magazines_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'magazines'))
    target_dir = os.path.abspath(os.path.join(base_magazines_dir, year, slug))

    # Verify target directory is safely contained inside base_magazines_dir
    if not target_dir.startswith(base_magazines_dir):
        flash("Access violation: invalid directory path.", "danger")
        return redirect(url_for('admin_bp.dashboard'))

    if os.path.exists(target_dir):
        try:
            # Preserve cover.jpg and meta.json structure so cover is not lost
            cover_file = os.path.join(target_dir, 'cover.jpg')
            has_cover = os.path.exists(cover_file)

            meta_file = os.path.join(target_dir, 'meta.json')
            meta_data = {}
            if os.path.exists(meta_file):
                try:
                    with open(meta_file, 'r', encoding='utf-8') as mf:
                        meta_data = json.load(mf)
                except Exception:
                    pass

            # Remove all uploaded files and directories, preserving cover.jpg
            for item in os.listdir(target_dir):
                if item == 'cover.jpg':
                    continue
                item_path = os.path.join(target_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                else:
                    try:
                        os.remove(item_path)
                    except Exception:
                        pass

            # Reset status to in-compilation and remove upload flag
            if has_cover or meta_data:
                meta_data['status'] = 'in-compilation'
                meta_data['uploaded_by_admin'] = False
                if has_cover:
                    meta_data['cover_image'] = 'cover.jpg'
                with open(meta_file, 'w', encoding='utf-8') as mf:
                    json.dump(meta_data, mf, indent=2)
            else:
                shutil.rmtree(target_dir, ignore_errors=True)

            scan_magazines(force_reload=True)
            flash(f"Successfully removed uploaded files for '{slug}' ({year}). Reverted to 'In Compilation'.", "success")
        except Exception as e:
            flash(f"Failed to delete edition files: {str(e)}", "danger")
    else:
        flash(f"No custom uploaded files found on disk for '{slug}' ({year}).", "info")

    return redirect(url_for('admin_bp.dashboard'))

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out safely.", "info")
    return redirect(url_for('admin_bp.login'))

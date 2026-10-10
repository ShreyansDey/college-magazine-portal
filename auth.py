"""
auth.py - Authentication, Bcrypt Password Verification, and Email OTP Service.
Implements security controls specified in files/SECURITY.md.
"""

import os
import json
import secrets
import smtplib
import time
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
import bcrypt
from dotenv import load_dotenv
from flask import session, redirect, url_for, flash, abort, request

# Load environment variables from .env
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ADMIN_STORE_PATH = os.environ.get('ADMIN_STORE_PATH', os.path.join(BASE_DIR, 'data', 'admins.json'))
if not os.path.isabs(ADMIN_STORE_PATH):
    ADMIN_STORE_PATH = os.path.join(BASE_DIR, ADMIN_STORE_PATH)

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER', '').strip()
SMTP_PASS = os.environ.get('SMTP_PASS', '').replace(' ', '').strip()
OTP_EXPIRY_MINUTES = int(os.environ.get('OTP_EXPIRY_MINUTES', 10))

# In-memory store for pending OTP verification:
# format: { email: { "otp": "123456", "expires_at": timestamp, "attempts": 0 } }
_pending_otps = {}

def get_admin_by_email(email):
    """Retrieves an admin record from data/admins.json by email address."""
    if not os.path.exists(ADMIN_STORE_PATH):
        return None
    try:
        with open(ADMIN_STORE_PATH, 'r', encoding='utf-8') as f:
            admins = json.load(f)
            for admin in admins:
                if admin.get('username', '').strip().lower() == email.strip().lower():
                    return admin
    except Exception as e:
        print(f"[AUTH ERROR] Failed to read admin store: {e}")
    return None

def verify_password(plain_password, password_hash):
    """Verifies a plain text password against a stored bcrypt hash."""
    if not plain_password or not password_hash:
        return False
    try:
        hash_bytes = password_hash.encode('utf-8')
        # Check exact password
        if bcrypt.checkpw(plain_password.encode('utf-8'), hash_bytes):
            return True
        # Also check without spaces (e.g. Google App Password format)
        cleaned = plain_password.replace(' ', '')
        if cleaned != plain_password and bcrypt.checkpw(cleaned.encode('utf-8'), hash_bytes):
            return True
        return False
    except Exception as e:
        print(f"[AUTH ERROR] Bcrypt check failed: {e}")
        return False

def generate_otp():
    """Generates a secure 6-digit numeric OTP code."""
    return f"{secrets.randbelow(900000) + 100000}"

def send_otp_email(to_email, otp_code):
    """
    Sends the 6-digit OTP code to the administrator's email using Gmail SMTP.
    Returns (success: bool, message: str).
    """
    if not SMTP_USER or not SMTP_PASS:
        # Fallback in local development if credentials not provided
        print(f"[AUTH WARNING] SMTP credentials not set. Dev OTP: {otp_code}")
        return True, "Dev Mode: OTP logged to console."

    try:
        subject = f"Your Admin Verification Code: {otp_code} — RKM Vidyamandira"

        # HTML Email Template with collegiate styling
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 24px; }}
            .card {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 20px; }}
            .title {{ font-size: 20px; font-weight: 700; color: #0f172a; margin: 12px 0 4px 0; }}
            .sub {{ font-size: 13px; color: #64748b; margin: 0; }}
            .body-text {{ font-size: 14px; color: #334155; line-height: 1.6; margin: 24px 0; }}
            .otp-box {{ background: #fef3c7; border: 1px dashed #d97706; border-radius: 8px; text-align: center; padding: 18px; margin: 24px 0; }}
            .otp-code {{ font-size: 32px; font-weight: 800; letter-spacing: 6px; color: #b45309; font-family: monospace; }}
            .meta-text {{ font-size: 12px; color: #64748b; text-align: center; margin-top: 8px; }}
            .footer {{ border-top: 1px solid #f1f5f9; padding-top: 16px; margin-top: 24px; font-size: 11px; color: #94a3b8; text-align: center; }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="header">
              <h2 class="title">Ramakrishna Mission Vidyamandira</h2>
              <p class="sub">Unified College Magazine Portal • Administrator Access</p>
            </div>
            <p class="body-text">
              Hello Administrator,<br><br>
              A login request was initiated for your administrator account (<strong>{to_email}</strong>).
              Please use the verification code below to complete your sign-in:
            </p>
            <div class="otp-box">
              <div class="otp-code">{otp_code}</div>
              <div class="meta-text">Valid for {OTP_EXPIRY_MINUTES} minutes • Do not share this code</div>
            </div>
            <p class="body-text">
              If you did not request this verification code, please ignore this email or review your account security immediately.
            </p>
            <div class="footer">
              Ramakrishna Mission Vidyamandira, Belur Math, Howrah, West Bengal 711202<br>
              Automated Institutional Security Notification
            </div>
          </div>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"RKMV Publications Portal <{SMTP_USER}>"
        msg["To"] = to_email

        part = MIMEText(html_content, "html")
        msg.attach(part)

        # Connect to Gmail SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())

        print(f"[AUTH INFO] OTP sent successfully to {to_email}")
        return True, "Verification code sent to your registered email."
    except Exception as e:
        print(f"[AUTH ERROR] Failed to send email via SMTP: {e}")
        # In case of SMTP issues (e.g. temporary port timeout), log OTP locally so admin is never locked out
        print(f"[AUTH BACKUP CODE] Security code for {to_email}: {otp_code}")
        return False, f"Email delivery failed: {str(e)}"

def issue_otp_for_admin(email):
    """Generates an OTP, stores it with expiration, and sends via email."""
    otp = generate_otp()
    expires_at = time.time() + (OTP_EXPIRY_MINUTES * 60)
    _pending_otps[email.lower()] = {
        'otp': otp,
        'expires_at': expires_at,
        'attempts': 0
    }
    success, msg = send_otp_email(email, otp)
    return success, msg

def verify_otp_for_admin(email, entered_otp):
    """
    Validates an entered OTP.
    Returns (valid: bool, error_message: str or None).
    """
    email_key = email.lower()
    record = _pending_otps.get(email_key)
    if not record:
        return False, "No active verification code found. Please request a new code."

    # Check expiration
    if time.time() > record['expires_at']:
        del _pending_otps[email_key]
        return False, "The verification code has expired. Please request a new one."

    # Check attempt limit (max 5)
    record['attempts'] += 1
    if record['attempts'] > 5:
        del _pending_otps[email_key]
        return False, "Too many incorrect attempts. Please request a new verification code."

    # Compare code safely
    if secrets.compare_digest(record['otp'].strip(), entered_otp.strip()):
        # OTP is valid, remove it so it cannot be reused
        del _pending_otps[email_key]
        return True, None
    else:
        remaining = 5 - record['attempts']
        return False, f"Incorrect verification code. {remaining} attempt(s) remaining."

def login_required(f):
    """Decorator to require an active administrator session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in') or not session.get('admin_email'):
            flash("Please sign in to access the administrator portal.", "warning")
            return redirect(url_for('admin_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def super_admin_required(f):
    """Decorator to require a super-admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in') or not session.get('admin_email'):
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('admin_bp.login'))
        if session.get('admin_role') != 'super-admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def hash_password(plain_password):
    """Hashes a password with bcrypt using a cost factor of 12."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

def list_all_admins():
    """Returns a list of all admin records without sensitive password hashes."""
    if not os.path.exists(ADMIN_STORE_PATH):
        return []
    try:
        with open(ADMIN_STORE_PATH, 'r', encoding='utf-8') as f:
            admins = json.load(f)
            return [
                {
                    'id': a.get('id'),
                    'username': a.get('username'),
                    'role': a.get('role', 'admin'),
                    'created_at': a.get('created_at'),
                    'last_login': a.get('last_login')
                }
                for a in admins
            ]
    except Exception as e:
        print(f"[AUTH ERROR] Failed to list admins: {e}")
        return []

def create_admin(username, password, role='admin'):
    """Creates a new admin account and persists to ADMIN_STORE_PATH."""
    username = username.strip().lower()
    if not username:
        return False, "Username or email is required."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if role not in ('admin', 'super-admin'):
        role = 'admin'

    os.makedirs(os.path.dirname(ADMIN_STORE_PATH), exist_ok=True)
    admins = []
    if os.path.exists(ADMIN_STORE_PATH):
        try:
            with open(ADMIN_STORE_PATH, 'r', encoding='utf-8') as f:
                admins = json.load(f)
        except Exception:
            admins = []

    for a in admins:
        if a.get('username', '').strip().lower() == username:
            return False, f"Admin account '{username}' already exists."

    next_id = max([a.get('id', 0) for a in admins], default=0) + 1
    new_admin = {
        'id': next_id,
        'username': username,
        'password_hash': hash_password(password),
        'role': role,
        'created_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'last_login': None
    }
    admins.append(new_admin)

    try:
        with open(ADMIN_STORE_PATH, 'w', encoding='utf-8') as f:
            json.dump(admins, f, indent=2)
        return True, new_admin
    except Exception as e:
        return False, f"Failed to save admin account: {e}"

def delete_admin(identifier):
    """Deletes an admin account by id (int) or username/email (str)."""
    if not os.path.exists(ADMIN_STORE_PATH):
        return False, "Admin store does not exist."
    try:
        with open(ADMIN_STORE_PATH, 'r', encoding='utf-8') as f:
            admins = json.load(f)

        filtered = []
        found = False
        for a in admins:
            matches_id = str(a.get('id')) == str(identifier)
            matches_user = str(a.get('username', '')).lower() == str(identifier).lower()
            if matches_id or matches_user:
                found = True
            else:
                filtered.append(a)

        if not found:
            return False, f"Admin '{identifier}' not found."

        with open(ADMIN_STORE_PATH, 'w', encoding='utf-8') as f:
            json.dump(filtered, f, indent=2)
        return True, "Admin account removed successfully."
    except Exception as e:
        return False, f"Failed to delete admin: {e}"

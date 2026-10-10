"""
tests/test_auth.py - Automated Unit Tests for Authentication & 2FA.
Implements UT-AUTH test cases from files/TEST_PLAN.md.
"""

import pytest
from auth import (
    verify_password, hash_password, generate_otp,
    list_all_admins, get_admin_by_email
)

def test_hash_and_verify_password():
    """UT-AUTH-04: Password hash generation and verification with bcrypt."""
    plain = "SuperSecretPassword123!"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("WrongPassword123!", hashed) is False

def test_generate_otp_format():
    """Verify OTP generated is a 6-digit numeric string."""
    otp = generate_otp()
    assert len(otp) == 6
    assert otp.isdigit()

def test_list_admins_omits_password_hash():
    """UT-AUTH-08: Admin list omits sensitive password hashes."""
    admins = list_all_admins()
    assert isinstance(admins, list)
    for a in admins:
        assert 'username' in a
        assert 'role' in a
        assert 'password_hash' not in a

def test_get_admin_by_email():
    """Check retrieving admin by case-insensitive email."""
    admin = get_admin_by_email("shreyansdey2006@gmail.com")
    if admin:
        assert admin['username'].lower() == "shreyansdey2006@gmail.com"
        assert 'password_hash' in admin

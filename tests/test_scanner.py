"""
tests/test_scanner.py - Automated Unit Tests for the Discovery Scanner Engine.
Implements UT-SCAN test cases from files/TEST_PLAN.md.
"""

import pytest
from scanner import (
    scan_magazines, get_filter_options, get_departments,
    get_bhavans, get_annual_publications
)

def test_scan_magazines_returns_catalogue():
    """UT-SCAN-01: Scanner returns complete official publications registry."""
    magazines = scan_magazines()
    assert isinstance(magazines, list)
    assert len(magazines) >= 20, "Should have at least 20 official publications"

def test_magazines_categories():
    """UT-SCAN-02: Scanner catalogue contains Annual, Departmental, and Hostel publications."""
    magazines = scan_magazines()
    categories = set(m['category'] for m in magazines)
    assert 'Annual' in categories
    assert 'Departmental' in categories
    assert 'Hostel' in categories

def test_filter_options():
    """UT-SCAN-03: get_filter_options returns valid sorted academic sessions and categories."""
    years, categories = get_filter_options()
    assert len(years) >= 2
    assert '2025-2026' in years
    assert 'Annual' in categories
    assert 'Departmental' in categories
    assert 'Hostel' in categories

def test_departments_mapping():
    """UT-SCAN-04: Returns all 14 academic departments with journal associations."""
    depts = get_departments()
    assert len(depts) == 14
    for d in depts:
        assert 'name' in d
        assert 'slug' in d
        assert 'journal_name' in d
        assert 'magazines' in d

def test_bhavans_mapping():
    """UT-SCAN-05: Returns all 5 official residential Bhavans."""
    bhavans = get_bhavans()
    assert len(bhavans) == 5
    slugs = [b['slug'] for b in bhavans]
    assert 'shree-bhavan' in slugs
    assert 'shraddha-bhavan' in slugs
    assert 'vivek-bhavan' in slugs
    assert 'vinay-bhavan' in slugs
    assert 'vidya-bhavan' in slugs

def test_annual_publications():
    """UT-SCAN-06: Returns college flagship Vidyamandira Patrika."""
    annuals = get_annual_publications()
    assert len(annuals) >= 1
    assert any('vidyamandira-patrika' in a['slug'] for a in annuals)

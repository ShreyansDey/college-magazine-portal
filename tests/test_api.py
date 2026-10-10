"""
tests/test_api.py - Automated Integration Tests for REST API Endpoints.
Implements UT-API test cases from files/TEST_PLAN.md and files/API_DESIGN.md.
"""

import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_editions_public(client):
    """UT-API-01: GET /api/editions returns 200 with list of publications."""
    res = client.get('/api/editions')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    assert data['count'] >= 20
    assert len(data['data']) == data['count']

def test_get_editions_category_filter(client):
    """UT-API-02: GET /api/editions?category=departmental filters correctly."""
    res = client.get('/api/editions?category=departmental')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    for item in data['data']:
        assert item['category'] == 'Departmental'

def test_get_editions_invalid_category(client):
    """UT-API-03: GET /api/editions?category=invalid returns 400 Bad Request."""
    res = client.get('/api/editions?category=invalid-category')
    assert res.status_code == 400
    data = res.get_json()
    assert data['status'] == 'error'
    assert 'Invalid category value' in data['message']

def test_get_years(client):
    """UT-API-07: GET /api/years returns sorted descending academic sessions."""
    res = client.get('/api/years')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    assert '2025-2026' in data['data']

def test_get_categories(client):
    """GET /api/categories returns category breakdown and sub_ids."""
    res = client.get('/api/categories')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    cat_data = data['data']
    assert 'annual' in cat_data
    assert 'departmental' in cat_data
    assert 'bhavan' in cat_data
    assert len(cat_data['departmental']['sub_ids']) == 14
    assert len(cat_data['bhavan']['sub_ids']) == 5

def test_get_edition_by_id(client):
    """UT-API-04: GET /api/editions/<id> returns specific edition details."""
    res = client.get('/api/editions/vidyamandira-patrika')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    assert data['data']['slug'] == 'vidyamandira-patrika'

def test_get_edition_not_found(client):
    """UT-API-05: GET /api/editions/<id> for non-existent returns 404."""
    res = client.get('/api/editions/non-existent-publication-999')
    assert res.status_code == 404
    data = res.get_json()
    assert data['status'] == 'error'

def test_admin_api_unauthorized(client):
    """Unauthenticated request to admin API endpoints redirects or returns error."""
    res = client.get('/api/admin/editions')
    # Because @login_required redirects unauthenticated requests
    assert res.status_code in (302, 401)

def test_admin_rescan_authenticated(client):
    """UT-API-09: Authenticated admin can trigger POST /api/admin/rescan."""
    with client.session_transaction() as sess:
        sess['admin_logged_in'] = True
        sess['admin_email'] = 'test@vidyamandira.ac.in'
        sess['admin_role'] = 'admin'
    res = client.post('/api/admin/rescan')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    assert data['total'] >= 20

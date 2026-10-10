"""
app.py - Core Flask Application for Ramakrishna Mission Vidyamandira Magazine Portal.
"""

import os
import io
from flask import Flask, render_template, send_from_directory, abort, request, redirect, url_for, send_file
from dotenv import load_dotenv
from scanner import scan_magazines, get_filter_options, get_bhavans, get_departments, get_annual_publications
from admin_routes import admin_bp
from api_routes import api_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-vidyamandira-2026')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Register Administrator Blueprint (/admin) & Public API Blueprint (/api)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MAGAZINES_DIR = os.path.join(BASE_DIR, 'magazines')

@app.after_request
def set_security_headers(response):
    """Enforces essential HTTP security headers as specified in files/SECURITY.md."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https:; "
        "frame-src 'self';"
    )
    return response

@app.route('/')
def home():
    """Renders the main hero portal and magazine discovery catalogue."""
    magazines = scan_magazines()
    years, categories = get_filter_options()

    # Hero background slideshow images (Enhanced collegiate photography)
    hero_images = [
        'images/image4.jpg',
        'images/image5.jpg',
        'images/image1.jpg'
    ]

    return render_template(
        'index.html',
        magazines=magazines,
        years=years,
        categories=categories,
        hero_images=hero_images
    )

@app.route('/annual')
def annual():
    """Renders the classical collegiate editorial showcase for Vidyamandira Patrika."""
    annual_magazines = get_annual_publications()
    years, _ = get_filter_options()
    return render_template(
        'annual.html',
        annual_magazines=annual_magazines,
        years=years
    )

@app.route('/departments')
@app.route('/departments/<dept_slug>')
def departments(dept_slug=None):
    """Renders the modern research & academic dashboard for all 14 departments."""
    dept_list = get_departments()
    selected_dept = None
    if dept_slug:
        selected_dept = next((d for d in dept_list if d['slug'] == dept_slug), None)
    if not selected_dept and dept_list:
        selected_dept = dept_list[0]

    return render_template(
        'departments.html',
        departments=dept_list,
        selected_dept=selected_dept
    )

@app.route('/bhavans')
@app.route('/bhavans/<bhavan_slug>')
def bhavans(bhavan_slug=None):
    """Renders the residential community hub for the 5 collegiate Bhavans."""
    bhavan_list = get_bhavans()
    selected_bhavan = None
    if bhavan_slug:
        selected_bhavan = next((b for b in bhavan_list if b['slug'] == bhavan_slug), None)
    if not selected_bhavan and bhavan_list:
        selected_bhavan = bhavan_list[0]

    return render_template(
        'bhavans.html',
        bhavans=bhavan_list,
        selected_bhavan=selected_bhavan
    )

@app.route('/read/<year>/<slug>')
def reader(year, slug):
    """Renders the distraction-free iframe reader container for an edition."""
    magazines = scan_magazines()
    edition = next((m for m in magazines if m['academic_year'] == year and m['slug'] == slug), None)

    if not edition:
        abort(404)

    return render_template('reader.html', edition=edition)

@app.route('/magazines/<path:filepath>')
def serve_magazine_files(filepath):
    """Safely serves individual static micro-frontend files from the magazines directory."""
    return send_from_directory(MAGAZINES_DIR, filepath)

@app.route('/editorial-guidelines')
def editorial_guidelines():
    """Renders the institutional Editorial Board Guidelines & Chronicle."""
    return render_template('editorial_guidelines.html')

@app.route('/metadata-specs')
def metadata_specs():
    """Renders the technical Metadata Specifications & Directory Architecture guide."""
    return render_template('metadata_specs.html')

@app.route('/download-starter-kit')
def download_starter_kit():
    """Provides student editorial teams with the official clean starter ZIP kit."""
    from uploader import generate_starter_kit
    zip_bytes = generate_starter_kit()
    return send_file(
        io.BytesIO(zip_bytes),
        mimetype='application/zip',
        as_attachment=True,
        download_name='vidyamandira-student-edition-template.zip'
    )

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Local dev server
    app.run(host='0.0.0.0', port=5000, debug=True)

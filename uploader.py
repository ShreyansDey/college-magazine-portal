"""
uploader.py - Safe Micro-Frontend ZIP Extraction and Starter Template Generator.
Implements Path Traversal & Zip-Slip security specified in files/SECURITY.md.
"""

import os
import io
import json
import zipfile
import shutil
import tempfile
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MAGAZINES_DIR = os.path.join(BASE_DIR, 'magazines')

def is_safe_path(base_dir, target_path):
    """
    Prevents Zip Slip vulnerability: ensures target_path resolves strictly within base_dir.
    """
    abs_base = os.path.realpath(base_dir)
    abs_target = os.path.realpath(target_path)
    return abs_target.startswith(abs_base + os.sep) or abs_target == abs_base

def install_magazine_zip(zip_file_storage, academic_year, slug, title=None, category=None, department=None, description=None):
    """
    Safely unpacks an uploaded magazine ZIP archive into magazines/<academic_year>/<slug>/.
    Returns (success: bool, message: str, preview_url: str or None).
    """
    academic_year = str(academic_year).strip()
    slug = str(slug).strip().lower().replace(' ', '-')

    # Target directory
    target_dir = os.path.join(MAGAZINES_DIR, academic_year, slug)

    # Use a secure temporary directory for validation before touching production magazines
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_path = os.path.join(temp_dir, 'upload.zip')
        zip_file_storage.save(temp_zip_path)

        if not zipfile.is_zipfile(temp_zip_path):
            return False, "The uploaded file is not a valid ZIP archive.", None

        extract_temp = os.path.join(temp_dir, 'extracted')
        os.makedirs(extract_temp, exist_ok=True)

        try:
            with zipfile.ZipFile(temp_zip_path, 'r') as zf:
                # 1. Zip Slip / Path Traversal Validation
                for member in zf.infolist():
                    destination = os.path.join(extract_temp, member.filename)
                    if not is_safe_path(extract_temp, destination):
                        return False, f"Security Violation: Archive contains illegal relative path ({member.filename}).", None

                # Extract safely
                zf.extractall(extract_temp)
        except Exception as e:
            return False, f"Failed to unzip archive: {str(e)}", None

        # 2. Check for index.html structure
        # Check if extracted files are inside a single root folder
        extracted_items = [item for item in os.listdir(extract_temp) if not item.startswith('__MACOSX') and not item.startswith('.')]
        working_root = extract_temp
        if len(extracted_items) == 1:
            single_child = os.path.join(extract_temp, extracted_items[0])
            if os.path.isdir(single_child):
                working_root = single_child

        index_file = os.path.join(working_root, 'index.html')
        if not os.path.exists(index_file):
            # Case-insensitive check
            found_index = None
            for root, _, files in os.walk(working_root):
                for f in files:
                    if f.lower() == 'index.html':
                        found_index = os.path.join(root, f)
                        break
                if found_index:
                    break

            if not found_index:
                return False, "Validation Failed: No 'index.html' file found in archive. Student editions must include an 'index.html' entrypoint.", None

        # 3. Create destination directory and copy files
        os.makedirs(target_dir, exist_ok=True)

        for item in os.listdir(working_root):
            if item.startswith('__MACOSX') or item == '.DS_Store':
                continue
            s_path = os.path.join(working_root, item)
            d_path = os.path.join(target_dir, item)
            if os.path.isdir(s_path):
                shutil.copytree(s_path, d_path, dirs_exist_ok=True)
            else:
                shutil.copy2(s_path, d_path)

        # 4. Update or Create meta.json
        meta_file = os.path.join(target_dir, 'meta.json')
        meta = {}
        if os.path.exists(meta_file):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
            except Exception:
                pass

        if title:
            meta['title'] = title
        elif not meta.get('title'):
            meta['title'] = slug.replace('-', ' ').title()

        if category:
            meta['category'] = category
        elif not meta.get('category'):
            meta['category'] = 'Departmental'

        if department:
            meta['department'] = department
        elif not meta.get('department'):
            meta['department'] = meta['title']

        if description:
            meta['description'] = description
        elif not meta.get('description'):
            meta['description'] = f"Student publication for {academic_year} at Ramakrishna Mission Vidyamandira."

        meta['academic_year'] = academic_year
        meta['status'] = 'published'
        meta['uploaded_by_admin'] = True
        meta['published_at'] = datetime.now().strftime('%Y-%m-%d')
        if 'cover_image' not in meta or not meta['cover_image']:
            # Check if cover.jpg exists in upload
            if os.path.exists(os.path.join(target_dir, 'cover.jpg')):
                meta['cover_image'] = 'cover.jpg'

        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2)

    # 5. Invalidate Scanner Cache
    try:
        from scanner import scan_magazines
        scan_magazines(force_reload=True)
    except Exception as e:
        print(f"[SCANNER WARNING] Reload failed: {e}")

    preview_url = f"/read/{academic_year}/{slug}"
    return True, f"Successfully uploaded and published '{meta.get('title', slug)}' for Session {academic_year}!", preview_url

def generate_starter_kit():
    """
    Generates an in-memory ZIP starter kit template for student editorial councils.
    Packages the high-fashion Exhibition Magazine editorial template from magazines/starter-kit-template/.
    Returns bytes of the ZIP file.
    """
    buffer = io.BytesIO()
    template_dir = os.path.join(MAGAZINES_DIR, 'starter-kit-template')

    if os.path.exists(template_dir):
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(template_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, template_dir)
                    zf.write(full_path, rel_path)
    else:
        # Emergency minimal fallback if folder does not exist
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('index.html', '<!DOCTYPE html><html><body><h1>Student Magazine</h1></body></html>')
            zf.writestr('style.css', 'body { font-family: sans-serif; }')
            zf.writestr('HOW_TO_EDIT.txt', 'Open index.html and customize your articles.')

    buffer.seek(0)
    return buffer.getvalue()

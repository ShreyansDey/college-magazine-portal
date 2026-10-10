"""
validate_edition.py - Sub-Team Edition Pre-Flight Validation Tool.
Implements the verification rules defined in files/CONTRIBUTING.md and files/ROADMAP.md (Task T-011).

Validates either an extracted magazine directory or a student .zip archive before submission:
  1. Hard Collar Check: root index.html exists
  2. meta.json Schema Check: valid JSON with title, category, department
  3. Asset Path Check: flags absolute root-relative links (/style.css) that break in micro-frontends
  4. Cover Image: checks for cover.jpg artwork
"""

import sys
import os
import re
import json
import zipfile
import tempfile

def check_relative_links(html_content):
    """Flags absolute links like href="/..." or src="/..." that break inside subfolders."""
    bad_patterns = [
        (r'href\s*=\s*["\']/(?!/)', 'Absolute href attribute (e.g. href="/style.css") found. Use relative path href="style.css".'),
        (r'src\s*=\s*["\']/(?!/)', 'Absolute src attribute (e.g. src="/logo.png") found. Use relative path src="images/logo.png".')
    ]
    issues = []
    for pattern, msg in bad_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            issues.append(f"{msg} ({len(matches)} instance(s) detected)")
    return issues

def validate_directory(dir_path):
    errors = []
    warnings = []

    # 1. Hard Collar: index.html
    index_file = os.path.join(dir_path, 'index.html')
    if not os.path.exists(index_file):
        errors.append("MISSING MANDATORY ENTRYPOINT: 'index.html' not found in root directory.")
    else:
        try:
            with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            link_issues = check_relative_links(content)
            for issue in link_issues:
                warnings.append(f"RELATIVE LINK WARNING in index.html: {issue}")
        except Exception as e:
            warnings.append(f"Could not read index.html: {e}")

    # 2. meta.json
    meta_file = os.path.join(dir_path, 'meta.json')
    if not os.path.exists(meta_file):
        warnings.append("RECOMMENDED FILE MISSING: 'meta.json' not found. Portal will use default catalogue metadata.")
    else:
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not data.get('title'):
                warnings.append("meta.json: 'title' field is missing or empty.")
            if not data.get('department'):
                warnings.append("meta.json: 'department' field is missing or empty.")

            category = data.get('category', '')
            if category and category.lower() not in ('annual', 'departmental', 'hostel', 'bhavan'):
                errors.append(f"meta.json: Invalid category '{category}'. Must be Annual, Departmental, or Hostel.")

            year = data.get('academic_year', '')
            if year and not re.match(r'^\d{4}-\d{4}$', year):
                warnings.append(f"meta.json: 'academic_year' format '{year}' should be 'YYYY-YYYY' (e.g. 2025-2026).")
        except json.JSONDecodeError as e:
            errors.append(f"MALFORMED JSON: meta.json contains invalid JSON syntax: {e}")
        except Exception as e:
            warnings.append(f"Could not read meta.json: {e}")

    # 3. cover.jpg
    cover_file = os.path.join(dir_path, 'cover.jpg')
    if not os.path.exists(cover_file):
        warnings.append("COVER ARTWORK MISSING: 'cover.jpg' not found. Default college crest will be displayed.")

    return errors, warnings

def validate_target(target_path):
    print(f"\n[VALIDATING] {target_path}")
    print("=" * 60)

    if not os.path.exists(target_path):
        print(f"[ERROR] Path does not exist: {target_path}")
        return False

    if os.path.isfile(target_path) and target_path.lower().endswith('.zip'):
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(target_path, 'r') as zf:
                    zf.extractall(temp_dir)
            except Exception as e:
                print(f"[ERROR] Failed to unzip archive: {e}")
                return False

            # Check if wrapped in a single root folder
            items = [i for i in os.listdir(temp_dir) if not i.startswith('__MACOSX') and not i.startswith('.')]
            working_dir = temp_dir
            if len(items) == 1 and os.path.isdir(os.path.join(temp_dir, items[0])):
                working_dir = os.path.join(temp_dir, items[0])

            errors, warnings = validate_directory(working_dir)
    elif os.path.isdir(target_path):
        errors, warnings = validate_directory(target_path)
    else:
        print("[ERROR] Target must be a directory or a .zip file.")
        return False

    # Output results
    if errors:
        print("\n[CRITICAL ERRORS] (Submission will fail portal validation):")
        for err in errors:
            print(f"  * {err}")
    else:
        print("\n[PASS] Mandatory 'Hard Collar' contract satisfied!")

    if warnings:
        print("\n[WARNINGS & RECOMMENDATIONS]:")
        for w in warnings:
            print(f"  * {w}")
    else:
        print("\n[PERFECT] All recommended metadata and relative assets are in order!")

    print("=" * 60)
    return len(errors) == 0

def main():
    if len(sys.argv) < 2:
        print("""
Usage:
  python tools/validate_edition.py <path_to_directory_or_zip>

Example:
  python tools/validate_edition.py magazines/starter-kit-template
  python tools/validate_edition.py my_submission.zip
""")
        sys.exit(1)

    target = sys.argv[1]
    success = validate_target(target)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

"""
manage.py - Command Line Interface (CLI) management script.
Implements administrative commands specified in files/ROADMAP.md (Task T-041):
  - create-admin: Safely creates an initial Super-Admin or Admin account
  - list-admins: Displays all registered admin accounts
  - delete-admin: Deletes an admin account by email
  - rescan: Forces discovery engine to index magazines
"""

import sys
import getpass
from auth import create_admin, list_all_admins, delete_admin
from scanner import scan_magazines

def print_help():
    print("""
Ramakrishna Mission Vidyamandira - Magazine Portal Management CLI

Available Commands:
  python manage.py create-admin    Create a new administrator account
  python manage.py list-admins      Display all existing admin accounts
  python manage.py delete-admin     Delete an admin account by username
  python manage.py rescan           Force index all student editions
""")

def handle_create_admin():
    print("\n--- Create New Administrator Account ---")
    username = input("Enter Admin Email (Username): ").strip()
    if not username:
        print("[ERROR] Email is required.")
        return

    password = getpass.getpass("Enter Password (min 8 chars): ").strip()
    if len(password) < 8:
        print("[ERROR] Password must be at least 8 characters long.")
        return

    confirm_password = getpass.getpass("Confirm Password: ").strip()
    if password != confirm_password:
        print("[ERROR] Passwords do not match.")
        return

    role_input = input("Role (1: admin, 2: super-admin) [Default: 2]: ").strip()
    role = "super-admin" if role_input == "2" or role_input.lower() == "super-admin" else "admin"

    success, result = create_admin(username, password, role)
    if success:
        print(f"\n[SUCCESS] Administrator '{username}' created successfully with role '{role}'!")
    else:
        print(f"\n[ERROR] Failed to create admin: {result}")

def handle_list_admins():
    print("\n--- Registered Administrator Accounts ---")
    admins = list_all_admins()
    if not admins:
        print("No administrators found in data/admins.json.")
        return

    print(f"{'ID':<4} | {'Role':<14} | {'Username / Email':<32} | {'Created At'}")
    print("-" * 75)
    for a in admins:
        print(f"{a.get('id', '-'):<4} | {a.get('role', 'admin'):<14} | {a.get('username', '-'):<32} | {a.get('created_at', '-')}")
    print()

def handle_delete_admin():
    if len(sys.argv) < 3:
        target = input("Enter email or ID of admin to delete: ").strip()
    else:
        target = sys.argv[2].strip()

    if not target:
        print("[ERROR] Identifier is required.")
        return

    confirm = input(f"Are you sure you want to permanently delete admin '{target}'? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    success, msg = delete_admin(target)
    if success:
        print(f"[SUCCESS] {msg}")
    else:
        print(f"[ERROR] {msg}")

def handle_rescan():
    print("\n[INFO] Scanning filesystem for student magazine editions...")
    magazines = scan_magazines(force_reload=True)
    published = sum(1 for m in magazines if m.get('has_reader'))
    print(f"[SUCCESS] Scanned {len(magazines)} publications: {published} published micro-frontends active.")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd in ("create-admin", "createadmin", "adduser"):
        handle_create_admin()
    elif cmd in ("list-admins", "listadmins", "admins"):
        handle_list_admins()
    elif cmd in ("delete-admin", "deleteadmin", "deluser"):
        handle_delete_admin()
    elif cmd in ("rescan", "scan"):
        handle_rescan()
    else:
        print(f"Unknown command: '{cmd}'")
        print_help()

if __name__ == '__main__':
    main()

"""
Run this ONCE (locally, or once via a Render/Railway/etc. shell) to create
your admin login. It never stores a plaintext password anywhere -
Admin.set_password() hashes it before saving.

Usage:
    python create_admin.py
"""

import getpass
from app import app, db
from models.admin import Admin


def create_admin():
    with app.app_context():
        username = input("Choose an admin username: ").strip()
        password = getpass.getpass("Choose an admin password: ")
        confirm = getpass.getpass("Confirm password: ")

        if password != confirm:
            print("Passwords do not match. Try again.")
            return

        existing = Admin.query.filter_by(username=username).first()
        if existing:
            existing.set_password(password)
            db.session.commit()
            print(f"Password updated for existing admin '{username}'.")
            return

        admin = Admin(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin '{username}' created successfully.")


if __name__ == "__main__":
    create_admin()
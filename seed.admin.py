# seed_admin.py
import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    password = os.getenv("ADMIN_PASSWORD", "admin123")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print(f"⚠️ Admin user '{email}' already exists.")
    else:
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print(f"✅ Admin user '{email}' created successfully.")

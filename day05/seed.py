from database import db
from models import User


def seed_users():
    db.session.execute(db.delete(User))

    users = [
        User(name="Alex", role="admin", email="alex@example.com"),
        User(name="Maria", role="user", email="maria@example.com"),
        User(name="John", role="moderator", email="john@example.com"),
    ]

    db.session.add_all(users)
    db.session.commit()

    print(f"✅ Seeded {len(users)} users successfully!")

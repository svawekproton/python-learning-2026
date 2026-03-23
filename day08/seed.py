from app.database import SessionLocal, engine, Base
from app.models import User
from werkzeug.security import generate_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    user = User(
        name="Alex",
        email="alex@example.com",
        password_hash=generate_password_hash("password123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"✅ Created user '{user.name}' (id={user.id})")
finally:
    db.close()

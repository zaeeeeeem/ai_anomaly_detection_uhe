import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.security import get_password_hash


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an admin user")
    parser.add_argument("--email", default="admin1234@example.com")
    parser.add_argument("--username", default="admin1234")
    parser.add_argument("--password", default="admin123")
    parser.add_argument("--full-name", default="Admin User")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        existing = (
            db.query(User)
            .filter((User.email == args.email) | (User.username == args.username))
            .first()
        )
        if existing:
            print("Admin already exists:", existing.email)
            return

        admin = User(
            email=args.email,
            username=args.username,
            hashed_password=get_password_hash(args.password),
            full_name=args.full_name,
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print("Admin user created:", admin.email)
    finally:
        db.close()


if __name__ == "__main__":
    main()

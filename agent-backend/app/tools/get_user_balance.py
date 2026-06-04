from app.db.database import SessionLocal
from app.repositories.user_repository import UserRepository


def execute(username: str):

    db = SessionLocal()

    try:
        user = UserRepository.get_by_username(
            db=db,
            username=username
        )

        if not user:
            return {
                "found": False
            }

        return {
            "found": True,
            "username": user.username,
            "balance": float(user.balance)
        }

    finally:
        db.close()
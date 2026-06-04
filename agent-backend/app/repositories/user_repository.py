from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: str
    ) -> User | None:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_username(
        db: Session,
        username: str
    ) -> User | None:
        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    @staticmethod
    def list_all(
        db: Session
    ) -> list[User]:
        return (
            db.query(User)
            .all()
        )
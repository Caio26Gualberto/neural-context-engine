from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        payment_id: str
    ) -> Payment | None:
        return (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: str
    ) -> list[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.user_id == user_id)
            .all()
        )

    @staticmethod
    def list_all(
        db: Session
    ) -> list[Payment]:
        return (
            db.query(Payment)
            .all()
        )
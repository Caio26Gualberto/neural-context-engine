from app.db.database import SessionLocal
from app.repositories.payment_repository import PaymentRepository


def execute(payment_id: str):

    db = SessionLocal()

    try:

        payment = PaymentRepository.get_by_id(
            db=db,
            payment_id=payment_id
        )

        if not payment:
            return {
                "found": False
            }

        return {
            "found": True,
            "payment_id": str(payment.id),
            "status": payment.status,
            "amount": float(payment.amount)
        }

    finally:
        db.close()
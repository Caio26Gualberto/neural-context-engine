from sqlalchemy.orm import Session
from app.models.message import Message

class MessageRepository:

    @staticmethod
    def create(
        db: Session,
        conversation_id,
        role: str,
        content: str,
    ):
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()

        return message

    @staticmethod
    def find_by_conversation(
        db: Session,
        conversation_id,
    ):
        return (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at.asc())
            .all()
        )

    @staticmethod
    def delete_all_by_conversation(db: Session, conversation_id) -> int:
        deleted = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .delete(synchronize_session=False)
        )
        db.commit()
        return deleted
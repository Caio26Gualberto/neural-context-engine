from sqlalchemy.orm import Session
from app.models.conversation import Conversation

class ConversationRepository:

    @staticmethod
    def get_first(db: Session):
        return db.query(Conversation).first()

    @staticmethod
    def create(db: Session):
        conversation = Conversation()

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def delete(db: Session, conversation) -> None:
        db.delete(conversation)
        db.commit()
from sqlalchemy.orm import Session
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

class ConversationService:

    @staticmethod
    def get_or_create(db: Session):

        conversation = ConversationRepository.get_first(db)

        if conversation:
            return conversation

        return ConversationRepository.create(db)

    @staticmethod
    def build_history(
        db: Session,
        conversation_id,
    ):
        messages = MessageRepository.find_by_conversation(
            db,
            conversation_id,
        )

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]
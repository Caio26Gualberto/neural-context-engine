import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.agent_service import AgentService
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService
from app.db.database import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

router = APIRouter()


@router.delete("/conversation")
def clear_conversation():
    db = next(get_db())
    conversation = ConversationRepository.get_first(db)
    if not conversation:
        return {"deleted_messages": 0}
    deleted = MessageRepository.delete_all_by_conversation(db, conversation.id)
    ConversationRepository.delete(db, conversation)
    return {"deleted_messages": deleted}

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    db = next(get_db())
    context = AgentService.gather_context(payload.question)
    conversation = ConversationService.get_or_create(db)
    history = ConversationService.build_history(db, conversation.id)
    print("History:", history)
    answer = ChatService.answer(history=history, question=payload.question, context=context)
    MessageRepository.create(db, conversation_id=conversation.id, role="user", content=payload.question)
    MessageRepository.create(db, conversation_id=conversation.id, role="assistant", content=answer)
    return AskResponse(
        answer=answer
    )


@router.post("/ask/stream")
def ask_stream(payload: AskRequest):
    db = next(get_db())
    context = AgentService.gather_context(payload.question)
    conversation = ConversationService.get_or_create(db)
    history = ConversationService.build_history(db, conversation.id)
    MessageRepository.create(db, conversation_id=conversation.id, role="user", content=payload.question)

    def generate():
        assistant_response = ""

        for token in ChatService.stream_answer(
            history=history,
            question=payload.question,
            context=context,
        ):
            assistant_response += token

            yield f"data: {json.dumps({'token': token})}\n\n"

        MessageRepository.create(
            db,
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_response,
        )

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

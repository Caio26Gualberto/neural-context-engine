import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.db.database import SessionLocal
from app.rag.search_service import SearchService
from app.services.chat_service import ChatService

router = APIRouter()


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    db = SessionLocal()
    try:
        results = SearchService.search(db=db, query=payload.question, limit=3)
        context = "\n\n".join(row.content for row in results) if results else ""
    finally:
        db.close()

    return AskResponse(
        answer=ChatService.answer(question=payload.question, context=context)
    )


@router.post("/ask/stream")
def ask_stream(payload: AskRequest):
    db = SessionLocal()
    try:
        results = SearchService.search(db=db, query=payload.question, limit=3)
        context = "\n\n".join(row.content for row in results) if results else ""
    finally:
        db.close()

    def generate():
        for token in ChatService.stream_answer(question=payload.question, context=context):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

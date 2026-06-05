import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.agent_service import AgentService
from app.services.chat_service import ChatService

router = APIRouter()


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    context = AgentService.gather_context(payload.question)
    return AskResponse(
        answer=ChatService.answer(question=payload.question, context=context)
    )


@router.post("/ask/stream")
def ask_stream(payload: AskRequest):
    context = AgentService.gather_context(payload.question)

    def generate():
        for token in ChatService.stream_answer(question=payload.question, context=context):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

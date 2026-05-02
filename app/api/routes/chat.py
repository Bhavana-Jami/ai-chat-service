from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm import stream_response
import json, uuid

router = APIRouter()

# non-streaming (current)
@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # collect full response for now
    full_text = ""
    async for chunk in stream_response(request.messages, request.system_prompt):
        full_text += chunk

    return ChatResponse(
        message={"role": "assistant", "content": full_text},
        session_id=request.session_id or str(uuid.uuid4())
    )

# streaming (next step)
@router.post("/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        async for chunk in stream_response(request.messages, request.system_prompt):
            yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # important for nginx
        }
    )
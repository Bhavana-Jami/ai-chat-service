from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    role: str        # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    session_id: Optional[str] = None
    system_prompt: Optional[str] = None  # for RAG extension later

class ChatResponse(BaseModel):
    message: ChatMessage
    session_id: str
from openai import AsyncOpenAI
from app.schemas.chat import ChatMessage
from app.core.config import settings
from typing import AsyncGenerator

client = AsyncOpenAI(api_key=settings.openai_api_key)

async def stream_response(
    messages: list[ChatMessage],
    system_prompt: str = None
) -> AsyncGenerator[str, None]:
    stream = await client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        stream=True,
        messages=[
            {"role": "system", "content": system_prompt or "You are a helpful assistant."},
            *[m.model_dump() for m in messages]
        ],
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            yield delta
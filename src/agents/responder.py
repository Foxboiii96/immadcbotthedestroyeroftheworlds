# src/agents/responder.py
from src.services.mistral_client import mistral_client
from src.agents.prompts import get_responder_prompt
import httpx

async def agent_responder_generate(current_message, recent_messages, context_summary, strategy, long_term_memories=None, image_url=None):
    """
    Generates the final response, now capable of processing images and long-term memories.
    """
    recent_log = "\n".join(recent_messages)
    text_prompt = get_responder_prompt(
        context_summary,
        strategy,
        recent_log,
        current_message,
        long_term_memories
    )

    messages = []
    if image_url:
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            response.raise_for_status()
            image_bytes = response.content

        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": text_prompt},
                {"type": "image", "image": image_bytes},
            ],
        })
    else:
        messages.append({"role": "user", "content": text_prompt})

    response = await mistral_client.chat.complete_async(
        model="mistral-large-2402",
        messages=messages
    )
    return response.choices[0].message.content

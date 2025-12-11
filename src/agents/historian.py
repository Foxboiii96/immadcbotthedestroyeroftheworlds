# src/agents/historian.py
from src.services.mistral_client import mistral_client
from src.agents.prompts import get_historian_prompt

async def agent_historian_summarize(old_messages):
    """
    Generates a summary of old messages using the Mistral API.
    """
    if not old_messages:
        return "Nincs előzmény."

    text_block = "\n".join(old_messages)
    prompt = get_historian_prompt(text_block)

    response = await mistral_client.chat.complete_async(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

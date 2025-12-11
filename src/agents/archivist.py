# src/agents/archivist.py
from src.services.mistral_client import mistral_client
from src.agents.prompts import get_archivist_prompt

async def agent_archivist_filter_and_summarize(conversation_log: str):
    """
    Analyzes a conversation log and returns a concise memory if it's significant.
    Returns None if the event is not memorable.
    """
    prompt = get_archivist_prompt(conversation_log)

    response = await mistral_client.chat.complete_async(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0, # Low temperature for factual, deterministic filtering
        max_tokens=100
    )

    summary = response.choices[0].message.content.strip()

    if summary == "NONE" or not summary:
        return None

    return summary

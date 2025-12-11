# src/agents/responder.py
from src.services.mistral_client import mistral_client
from src.agents.prompts import get_responder_prompt

async def agent_responder_generate(current_message, recent_messages, context_summary, strategy):
    """
    Generates the final response based on the persona prompt.
    """
    recent_log = "\n".join(recent_messages)
    prompt = get_responder_prompt(context_summary, strategy, recent_log, current_message)

    response = await mistral_client.chat.complete_async(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# src/agents/strategist.py
from src.services.mistral_client import mistral_client
from src.agents.prompts import get_strategist_prompt

async def agent_strategist_analyze(current_message, context_summary):
    """
    Analyzes the user's intent and provides a strategy.
    """
    prompt = get_strategist_prompt(current_message, context_summary)

    response = await mistral_client.chat.complete_async(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

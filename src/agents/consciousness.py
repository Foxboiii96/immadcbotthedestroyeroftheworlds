# src/agents/consciousness.py
from src.services.mistral_client import mistral_client
from src.agents.prompts import get_consciousness_prompt

async def agent_consciousness_generate_thought():
    """
    Generates a brief, in-character thought for the bot's status.
    """
    prompt = get_consciousness_prompt()

    response = await mistral_client.chat.complete_async(
        model="mistral-small-latest",  # Use a smaller model for this simple task
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,  # Higher temperature for more varied thoughts
        max_tokens=20  # Keep the response short
    )

    thought = response.choices[0].message.content.strip().strip('"')
    # A simple filter to ensure the thought is not just an empty string or irrelevant noise
    if not thought or len(thought.split()) > 7:
        return "A kozmoszt kémleli..." # Fallback status

    return thought

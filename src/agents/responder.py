from src.utils.mistral_client import mistral_client

async def agent_responder_generate(current_message, recent_messages, context_summary, strategy):
    """
    Feladata: Megírni a végső választ a Discordra.
    Látja: A rövidtávú pontos üzeneteket + a hosszútávú összefoglalót + a stratégiai utasítást.
    """
    recent_log = "\n".join(recent_messages)
    prompt = (
        f"Te egy segítőkész Discord Bot vagy. \n"
        f"Hosszútávú memória (Agent 1-től): {context_summary}\n"
        f"Stratégiai utasítás (Agent 2-től): {strategy}\n"
        f"Legutóbbi pontos üzenetek:\n{recent_log}\n\n"
        f"Most válaszolj az utolsó üzenetre ('{current_message}') magyarul a fenti információk alapján."
    )

    response = await mistral_client.chat.complete_async(
        model="mistral-large-latest", # Erősebb modell a végső válaszhoz
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

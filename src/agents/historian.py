from src.utils.mistral_client import mistral_client

async def agent_historian_summarize(old_messages):
    """
    Feladata: A chat régebbi szakaszának tömörítése, hogy ne foglaljon sok helyet.
    Nem a teljes szöveget adja vissza, hanem a kontextus lényegét.
    """
    if not old_messages:
        return "Nincs előzmény."

    text_block = "\n".join(old_messages)
    prompt = (
        f"Te egy Archiváló Ágens vagy. A feladatod, hogy a következő chat logból "
        f"készíts egy nagyon rövid, tényszerű összefoglalót magyarul. Csak a lényeget tartsd meg.\n\n"
        f"Chat log:\n{text_block}"
    )

    response = await mistral_client.chat.complete_async(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

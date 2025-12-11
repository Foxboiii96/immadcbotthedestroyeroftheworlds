from src.utils.mistral_client import mistral_client

async def agent_strategist_analyze(current_message, context_summary):
    """
    Feladata: Eldönteni, mi a felhasználó szándéka az összefoglaló és az új üzenet alapján.
    Instrukciókat ad a Válaszadónak.
    """
    prompt = (
        f"Te egy Stratégiai Elemző Ágens vagy. \n"
        f"Kontextus (előzmények): {context_summary}\n"
        f"Aktuális üzenet: {current_message}\n\n"
        f"Határozd meg, mi a felhasználó célja, és adj egy rövid utasítást a válaszadó botnak, "
        f"hogy hogyan reagáljon stílusban és tartalomban. (Pl: 'A felhasználó dühös, nyugtasd meg', 'Kódot kér, adj példát')."
    )

    response = await mistral_client.chat.complete_async(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

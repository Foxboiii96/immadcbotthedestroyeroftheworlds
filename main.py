import os
import discord
import asyncio
from collections import deque
from dotenv import load_dotenv
from mistralai import Mistral

# Környezeti változók betöltése
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

# Mistral kliens inicializálása
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

# Discord Intents beállítása (szükséges az üzenetek olvasásához)
intents = discord.Intents.default()
intents.message_content = True

class MistralAgentBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Helyi memória: az utolsó 50 üzenetet tároljuk csatornánként
        # Ez teszi lehetővé, hogy a bot "lássa" a beszélgetést, de ne egyszerre küldjünk mindent
        self.channel_history = {} 
        self.max_history = 50

    async def on_ready(self):
        print(f'Bejelentkezve mint: {self.user} (ID: {self.user.id})')
        print('A 3-ágens rendszer aktív.')

    async def add_to_history(self, message):
        """Hozzáadja az üzenetet a csatorna specifikus memóriához."""
        channel_id = message.channel.id
        if channel_id not in self.channel_history:
            self.channel_history[channel_id] = deque(maxlen=self.max_history)
        
        # Formátum: "Felhasználó: Üzenet tartalom"
        self.channel_history[channel_id].append(f"{message.author.name}: {message.content}")

    # --- AGENT 1: AZ ARCHIVÁLÓ (Historian) ---
    async def agent_historian_summarize(self, old_messages):
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

    # --- AGENT 2: AZ ELEMZŐ (Strategist) ---
    async def agent_strategist_analyze(self, current_message, context_summary):
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

    # --- AGENT 3: A VÁLASZADÓ (Responder) ---
    async def agent_responder_generate(self, current_message, recent_messages, context_summary, strategy):
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

    async def on_message(self, message):
        # Saját üzeneteket ignoráljuk, de hozzáadjuk a history-hoz, hogy tudjuk mit mondtunk
        if message.author == self.user:
            await self.add_to_history(message)
            return

        # Üzenet hozzáadása a memóriához
        await self.add_to_history(message)

        # Csak akkor válaszol, ha megemlítik, vagy DM-ben van, vagy ha tartalmaz egy kulcsszót (pl: !bot)
        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            async with message.channel.typing():
                try:
                    history = list(self.channel_history.get(message.channel.id, []))
                    
                    # --- A CHAT RÉSZLETEKRE BONTÁSA (PARTITIONING) ---
                    # 1. RÉSZ: Régi üzenetek (pl. az első 35 az 50-ből) -> megy az Archiválónak
                    # 2. RÉSZ: Friss üzenetek (pl. az utolsó 15) -> megy a Válaszadónak szó szerint
                    
                    split_index = max(0, len(history) - 15)
                    old_chunk = history[:split_index]
                    recent_chunk = history[split_index:]

                    # 1. Lépés: Agent 1 összefoglalja a régi részt
                    summary = await self.agent_historian_summarize(old_chunk)
                    
                    # 2. Lépés: Agent 2 elemzi a szituációt
                    current_msg_content = f"{message.author.name}: {message.content}"
                    strategy = await self.agent_strategist_analyze(current_msg_content, summary)

                    # 3. Lépés: Agent 3 generálja a választ
                    final_response = await self.agent_responder_generate(
                        current_msg_content, 
                        recent_chunk, 
                        summary, 
                        strategy
                    )

                    await message.reply(final_response)

                except Exception as e:
                    print(f"Hiba történt: {e}")
                    await message.channel.send("Sajnálom, hiba történt a feldolgozás során.")

if __name__ == "__main__":
    if not DISCORD_TOKEN or not MISTRAL_API_KEY:
        print("Hiba: Hiányzó API kulcsok a .env fájlban!")
    else:
        client = MistralAgentBot(intents=intents)
        client.run(DISCORD_TOKEN)

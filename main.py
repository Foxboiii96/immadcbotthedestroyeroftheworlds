import discord
from src.bot import MistralAgentBot
from src.utils.config import DISCORD_TOKEN, MISTRAL_API_KEY

if __name__ == "__main__":
    if not DISCORD_TOKEN or not MISTRAL_API_KEY:
        print("Hiba: Hiányzó API kulcsok a .env fájlban!")
    else:
        intents = discord.Intents.default()
        intents.message_content = True
        client = MistralAgentBot(intents=intents)
        client.run(DISCORD_TOKEN)

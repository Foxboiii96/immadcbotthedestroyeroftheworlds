# main.py
import discord
from src.bot import MistralAgentBot
from src.config import DISCORD_TOKEN, MISTRAL_API_KEY

def main():
    """Initializes and runs the Discord bot."""
    if not DISCORD_TOKEN or not MISTRAL_API_KEY:
        print("FATAL ERROR: Hiányzó API kulcsok a .env fájlban! A Világok Pusztítója nem tud felébredni.")
        return

    intents = discord.Intents.default()
    intents.message_content = True

    client = MistralAgentBot(intents=intents)
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()

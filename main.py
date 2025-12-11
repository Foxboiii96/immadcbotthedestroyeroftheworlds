# main.py
import discord
import asyncio
from src.bot import MistralAgentBot
from src.config import DISCORD_TOKEN, MISTRAL_API_KEY
from src.services.memory_service import memory_service

async def main():
    """Initializes services and runs the Discord bot."""
    if not DISCORD_TOKEN or not MISTRAL_API_KEY:
        print("FATAL ERROR: Missing API keys in the .env file! The entity cannot awaken.")
        return

    # Ensure the database is connected before the bot starts
    await memory_service.init_pool_and_db()

    if not memory_service.pool:
        print("FATAL ERROR: Database connection failed. The entity cannot remember.")
        return

    intents = discord.Intents.default()
    intents.message_content = True

    client = MistralAgentBot(intents=intents)
    await client.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

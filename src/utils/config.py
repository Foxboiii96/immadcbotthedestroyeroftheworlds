import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Mistral AI API Key
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

# Bot Configuration
MAX_HISTORY = 50
HISTORY_SPLIT_INDEX = 15

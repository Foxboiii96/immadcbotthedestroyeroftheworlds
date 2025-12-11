# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Mistral AI API Key
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

# Supabase DB Connection
DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")


# Bot Configuration
MAX_HISTORY = 50
HISTORY_SPLIT_INDEX = 15

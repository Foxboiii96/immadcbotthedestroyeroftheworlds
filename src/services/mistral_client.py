# src/services/mistral_client.py
from mistralai import Mistral
from src.config import MISTRAL_API_KEY

mistral_client = Mistral(api_key=MISTRAL_API_KEY)

from mistralai import Mistral
from src.utils.config import MISTRAL_API_KEY

mistral_client = Mistral(api_key=MISTRAL_API_KEY)

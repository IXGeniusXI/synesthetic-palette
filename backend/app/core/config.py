import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

class Settings:
    NEBIUS_API_KEY: str = os.getenv("NEBIUS_API_KEY")
    NEBIUS_URL: str = "https://api.tokenfactory.nebius.com/v1/chat/completions"
    ACTIVE_MODEL: str = "nvidia/Nemotron-3_5-Lightning"

settings = Settings()

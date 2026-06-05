# list_models.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

print("📡 Modelli disponibili:")
print("-" * 50)

try:
    models = client.models.list()
    for model in models:
        if "gemini" in str(model).lower():
            print(f"  - {model}")
except Exception as e:
    print(f"❌ Errore nel listare i modelli: {e}")
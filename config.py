# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Modello valido dalla lista
MODEL_NAME = "gemini-2.5-flash"  # ← CAMBIATO

TEMPERATURA = 0.7
MAX_TOKEN = 1024

if not GEMINI_API_KEY:
    print("⚠️ ATTENZIONE: GEMINI_API_KEY non trovata nel file .env")
else:
    print(f"✅ Configurazione OK (API Key: {GEMINI_API_KEY[:10]}...)")
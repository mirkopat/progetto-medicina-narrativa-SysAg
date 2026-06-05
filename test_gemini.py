# test_gemini.py - VERSIONE FUNZIONANTE
import os
from dotenv import load_dotenv
from google import genai

# Carica la API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ API key non trovata nel file .env")
    exit(1)

print("🔧 Configurazione in corso...")
print(f"✅ API Key caricata (prime 10 caratteri: {GEMINI_API_KEY[:10]}...)")

# Inizializza il client
client = genai.Client(api_key=GEMINI_API_KEY)

# Usa un modello valido dalla lista
MODEL = "gemini-2.5-flash"  # ← CAMBIATO con un modello esistente!

print(f"📡 Connessione a {MODEL}...")
print("-" * 50)

try:
    response = client.models.generate_content(
        model=MODEL,
        contents="Ciao! Come stai? Raccontami una brevissima poesia sulla primavera in italiano (massimo 4 righe)."
    )
    
    print("🤖 RISPOSTA DI GEMINI:")
    print("-" * 50)
    print(response.text)
    print("-" * 50)
    print("✅ Test completato con successo!")
    
except Exception as e:
    print(f"❌ Errore: {e}")
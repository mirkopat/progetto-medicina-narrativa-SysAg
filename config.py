# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# SCELTA DEL PROVIDER
# ============================================
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

# ============================================
# CONFIGURAZIONE GEMINI
# ============================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# ============================================
# CONFIGURAZIONE OLLAMA
# ============================================
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma2:2b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434"))

print(f"🔧 Config - Provider: {LLM_PROVIDER}")
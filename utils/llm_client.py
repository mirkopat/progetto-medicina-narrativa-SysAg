"""
Client LLM unificato - supporta sia Gemini che Ollama
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import LLM_PROVIDER, GEMINI_API_KEY, GEMINI_MODEL, OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_PORT


class LLMClient:
    """
    Client unificato per LLM.
    Usa Gemini o Ollama in base alla configurazione.
    """
    
    def __init__(self, provider: str = None):
        self.provider = provider or LLM_PROVIDER
        
        if self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "ollama":
            self._init_ollama()
        else:
            raise ValueError(f"Provider sconosciuto: {self.provider}")
    
    def _init_gemini(self):
        """Inizializza il client Gemini (versione corretta)"""
        from google import genai
        self.model = GEMINI_MODEL
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        print(f"✅ LLM Client: Gemini ({self.model})")
    
    def _init_ollama(self):
        """Inizializza il client Ollama"""
        from utils.ollama_client import OllamaClient
        self.model = OLLAMA_MODEL
        self.client = OllamaClient(model=OLLAMA_MODEL, host=OLLAMA_HOST, port=OLLAMA_PORT)
        print(f"✅ LLM Client: Ollama ({self.model})")
    
    def generate(self, prompt: str) -> str:
        """Genera una risposta usando il provider configurato"""
        if self.provider == "gemini":
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                print(f"❌ Errore Gemini: {e}")
                return ""
        else:  # ollama
            return self.client.generate(prompt)


# Funzione di comodo
def quick_generate(prompt: str) -> str:
    client = LLMClient()
    return client.generate(prompt)


# Test del modulo
if __name__ == "__main__":
    print("🧪 Test del client LLM unificato")
    print("-" * 50)
    print(f"Provider corrente: {LLM_PROVIDER}")
    print()
    
    client = LLMClient()
    
    test_prompt = "Di solo 'Ciao, client funzionante!' in italiano."
    risposta = client.generate(test_prompt)
    
    print(f"🤖 Risposta: {risposta}")
    print("✅ Client LLM pronto all'uso!")
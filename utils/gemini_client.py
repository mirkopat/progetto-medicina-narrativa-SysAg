# utils/gemini_client.py
import os
from dotenv import load_dotenv
from google import genai

# Carica configurazione una volta sola all'avvio
load_dotenv()

class GeminiClient:
    """Client per interfacciarsi con Gemini API"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Inizializza il client Gemini
        
        Args:
            model_name: nome del modello (default gemini-2.5-flash)
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY non trovata nel file .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
    
    def generate(self, prompt: str) -> str:
        """
        Invia un prompt a Gemini e restituisce la risposta
        
        Args:
            prompt: testo da inviare al modello
            
        Returns:
            risposta del modello come stringa
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"❌ Errore nella chiamata a Gemini: {e}")
            return ""
    
    def generate_with_temperature(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Invia un prompt con temperatura personalizzata
        
        Args:
            prompt: testo da inviare
            temperature: creatività (0 = preciso, 1 = creativo)
            
        Returns:
            risposta del modello
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"temperature": temperature}
            )
            return response.text
        except Exception as e:
            print(f"❌ Errore: {e}")
            return ""


# Funzione di comodo per uso veloce
def quick_generate(prompt: str) -> str:
    """Funzione rapida per generare una risposta"""
    client = GeminiClient()
    return client.generate(prompt)


# Test del modulo (se eseguito direttamente)
if __name__ == "__main__":
    print("🧪 Test del client Gemini...")
    client = GeminiClient()
    
    test_prompt = "Di' solo 'Ciao, client funzionante!' in italiano."
    risposta = client.generate(test_prompt)
    
    print(f"🤖 Risposta: {risposta}")
    print("✅ Client Gemini pronto all'uso!")
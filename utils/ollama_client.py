# utils/ollama_client.py
import requests
import json

class OllamaClient:
    """
    Client per Ollama (modelli locali, senza limiti di quota)
    """
    
    def __init__(self, model: str = "gemma2:2b", host: str = "localhost", port: int = 11434):
        self.model = model
        self.base_url = f"http://{host}:{port}"
        self.generate_url = f"{self.base_url}/api/generate"
    
    def generate(self, prompt: str) -> str:
        """
        Invia un prompt a Ollama e restituisce la risposta
        """
        try:
            response = requests.post(
                self.generate_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
            
        except requests.exceptions.ConnectionError:
            print("❌ Errore: Ollama non è in esecuzione. Avvia Ollama dal menu Start.")
            return ""
        except Exception as e:
            print(f"❌ Errore nella chiamata a Ollama: {e}")
            return ""
    
    def test_connection(self) -> bool:
        """
        Verifica che Ollama sia in esecuzione
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            
            # Verifica se il modello è disponibile
            model_available = any(self.model.split(":")[0] in m.get("name", "") for m in models)
            
            if model_available:
                print(f"✅ Ollama connesso, modello {self.model} disponibile")
            else:
                print(f"⚠️ Modello {self.model} non trovato. Esegui: ollama pull {self.model}")
            
            return True
        except Exception as e:
            print(f"❌ Ollama non disponibile. Avvia l'applicazione Ollama.")
            return False


if __name__ == "__main__":
    print("🧪 Test del client Ollama")
    print("-" * 50)
    
    client = OllamaClient()
    
    if client.test_connection():
        test_prompt = "Di solo 'Ciao, client Ollama funzionante!' in italiano."
        risposta = client.generate(test_prompt)
        print(f"🤖 Risposta: {risposta}")
        print("✅ Client Ollama pronto all'uso!")
    else:
        print("❌ Test fallito. Assicurati che Ollama sia in esecuzione.")
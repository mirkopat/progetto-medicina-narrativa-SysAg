# response_gen.py
"""
Modulo per la generazione di risposte empatiche personalizzate
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_client import LLMClient  # ← usa LLMClient, non GeminiClient


class ResponseGenerator:
    """
    Generatore di risposte empatiche
    """
    
    def __init__(self):
        self.llm = LLMClient()  # ← client unificato
    
    def genera_risposta(self, 
                        messaggio_utente: str, 
                        situazione: str = "",
                        emozione: str = "",
                        strategia: str = "") -> str:
        """Genera una risposta empatica personalizzata"""
        
        template = f"""
        Sei un assistente empatico per anziani.
        
        L'utente ha appena scritto questo messaggio:
        "{messaggio_utente}"
        
        {f"Contesto: {situazione}" if situazione else ""}
        {f"Emozione rilevata: {emozione}" if emozione else ""}
        {f"Strategia da suggerire: {strategia}" if strategia else ""}
        
        Istruzioni:
        - Rispondi con empatia
        - Fai una sola domanda alla fine
        - Mantieni la risposta breve (max 3 frasi)
        - Usa l'italiano
        
        Risposta:
        """
        
        try:
            risposta = self.llm.generate(template)
            return risposta.strip()
        except Exception as e:
            print(f"❌ Errore: {e}")
            return "Ti ringrazio per avermelo raccontato. Come ti senti?"
    
    def genera_invito_narrativa(self) -> str:
        """Messaggio di benvenuto per la scrittura riflessiva"""
        prompt = """
        Sei un assistente empatico per anziani.
        Dai il benvenuto all'utente e invitalo a raccontare la sua giornata.
        Usa un tono caldo e accogliente. Sii breve (max 3 frasi).
        Concludi con una domanda aperta come "Cosa ne dici se mi racconti la tua giornata?"
        """
        return self.llm.generate(prompt)
    
    def genera_risposta_con_suggerimento(self, 
                                          messaggio_utente: str, 
                                          emozione: str,
                                          suggerimento: str) -> str:
        """Genera una risposta che include un suggerimento specifico"""
        
        template = f"""
        Sei un assistente empatico per anziani.
        
        Messaggio utente: "{messaggio_utente}"
        Emozione rilevata: {emozione}
        
        Suggerimento da proporre: {suggerimento}
        
        Scrivi una risposta che:
        1. Mostri empatia
        2. Proponga il suggerimento in modo gentile
        3. Finisca con una domanda aperta
        
        Risposta:
        """
        
        try:
            risposta = self.llm.generate(template)
            return risposta.strip()
        except:
            return f"Capisco come ti senti. {suggerimento} Ti andrebbe di provare?"
    
    def risposta_semplice(self, messaggio_utente: str) -> str:
        """Risposta semplice senza parametri aggiuntivi"""
        template = f"""
        L'utente ha scritto: "{messaggio_utente}"
        Rispondi con empatia, brevemente, e fai una domanda.
        """
        try:
            return self.llm.generate(template).strip()
        except:
            return "Grazie per avermelo detto. Vuoi raccontarmi altro?"


if __name__ == "__main__":
    print("🧪 Test ResponseGenerator")
    gen = ResponseGenerator()
    print(f"Invito: {gen.genera_invito_narrativa()}")
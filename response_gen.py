# response_gen.py
"""
Modulo per la generazione di risposte empatiche personalizzate
Ispirato all'esempio dell'assistente con template per LLM
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.gemini_client import GeminiClient


class ResponseGenerator:
    """
    Generatore di risposte empatiche usando Gemini
    """
    
    def __init__(self):
        self.client = GeminiClient()
    
    def genera_risposta(self, 
                        messaggio_utente: str, 
                        situazione: str = "",
                        emozione: str = "",
                        strategia: str = "") -> str:
        """
        Genera una risposta empatica personalizzata
        
        Args:
            messaggio_utente: il messaggio originale dell'utente
            situazione: contesto in cui si trova l'utente (es. "giornata difficile", "dopo terapia")
            emozione: emozione rilevata (es. "tristezza", "ansia", "gioia")
            strategia: strategia da suggerire (es. "respirazione profonda", "contattare un amico")
        
        Returns:
            risposta empatica come stringa
        """
        
        template = f"""
        Sei un assistente empatico per il supporto di pazienti con malattie croniche.
        
        L'utente ha appena scritto questo messaggio:
        "{messaggio_utente}"
        
        {f"Contesto: {situazione}" if situazione else ""}
        {f"Emozione rilevata: {emozione}" if emozione else ""}
        {f"Strategia da suggerire: {strategia}" if strategia else ""}
        
        Istruzioni:
        - Rispondi con empatia, mostrando comprensione per ciò che l'utente sta vivendo
        - Sii caloroso e rassicurante, ma non falso
        - Fai una sola domanda alla fine per incoraggiare il dialogo
        - Mantieni la risposta breve (max 3 frasi)
        - Usa lo stesso linguaggio del messaggio dell'utente (italiano)
        
        Risposta:
        """
        
        try:
            risposta = self.client.generate(template)
            return risposta.strip()
        except Exception as e:
            print(f"❌ Errore nella generazione della risposta: {e}")
            return "Ti ringrazio per avermelo raccontato. Come ti senti in questo momento?"
    
    def genera_risposta_con_suggerimento(self, 
                                          messaggio_utente: str, 
                                          emozione: str,
                                          suggerimento: str) -> str:
        """
        Genera una risposta che include un suggerimento specifico
        
        Args:
            messaggio_utente: il messaggio originale
            emozione: emozione rilevata
            suggerimento: suggerimento pratico da dare (es. "prova a fare una passeggiata breve")
        """
        
        template = f"""
        Sei un assistente empatico per pazienti con malattie croniche.
        
        Messaggio utente: "{messaggio_utente}"
        Emozione rilevata: {emozione}
        
        L'utente potrebbe beneficiare di questo suggerimento: {suggerimento}
        
        Scrivi una risposta che:
        1. Mostri empatia per l'emozione che sta provando
        2. Proponga il suggerimento in modo gentile e non impositivo
        3. Finisca con una domanda aperta
        4. Sia breve e in italiano
        
        Risposta:
        """
        
        try:
            risposta = self.client.generate(template)
            return risposta.strip()
        except Exception as e:
            print(f"❌ Errore: {e}")
            return f"Capisco come ti senti. {suggerimento} Ti andrebbe di provare?"
    
    def risposta_semplice(self, messaggio_utente: str) -> str:
        """
        Risposta semplice senza parametri aggiuntivi
        """
        template = f"""
        L'utente ha scritto: "{messaggio_utente}"
        
        Rispondi con empatia, brevemente, e fai una domanda per continuare il dialogo.
        Usa l'italiano.
        
        Risposta:
        """
        
        try:
            risposta = self.client.generate(template)
            return risposta.strip()
        except:
            return "Grazie per avermelo detto. Vuoi raccontarmi altro?"


# Test del modulo
if __name__ == "__main__":
    print("🧪 Test del generatore di risposte empatiche")
    print("-" * 50)
    
    generator = ResponseGenerator()
    
    # Test 1: risposta semplice
    print("\n📝 Test 1: Risposta semplice")
    print("-" * 30)
    messaggio = "Oggi mi sento giù, non ho voglia di fare niente."
    risposta = generator.risposta_semplice(messaggio)
    print(f"Utente: {messaggio}")
    print(f"Assistente: {risposta}")
    
    # Test 2: risposta con contesto
    print("\n📝 Test 2: Risposta con emozione e strategia")
    print("-" * 30)
    risposta2 = generator.genera_risposta(
        messaggio_utente="Ho paura della chemioterapia di domani",
        situazione="paziente oncologico in trattamento",
        emozione="paura",
        strategia="respirazione profonda e parlare con qualcuno di fidato"
    )
    print(f"Utente: Ho paura della chemioterapia di domani")
    print(f"Assistente: {risposta2}")
    
    # Test 3: risposta con suggerimento
    print("\n📝 Test 3: Risposta con suggerimento")
    print("-" * 30)
    risposta3 = generator.genera_risposta_con_suggerimento(
        messaggio_utente="Non esco di casa da tre giorni",
        emozione="isolamento",
        suggerimento="prova a fare una breve passeggiata di 10 minuti davanti a casa"
    )
    print(f"Utente: Non esco di casa da tre giorni")
    print(f"Assistente: {risposta3}")
    
    print("\n✅ Test completato!")
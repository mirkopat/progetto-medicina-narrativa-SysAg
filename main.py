# main.py
"""
Sistema principale per la medicina narrativa e qualità della vita
Integra tutti i classificatori, il calcolatore QoL e il generatore di risposte
"""

import json
import os
from datetime import datetime

from utils.gemini_client import GeminiClient
from classificatori.dominio_fisico import DominioFisico
from classificatori.dominio_psicologico import DominioPsicologico
from classificatori.dominio_sociale import DominioSociale
from classificatori.dominio_ambientale import DominioAmbientale
from qol_scorer import QoLScorer
from response_gen import ResponseGenerator


class MedicinaNarrativaAgent:
    """
    Agente principale per la medicina narrativa
    """
    
    def __init__(self):
        self.client = GeminiClient()
        self.fisico = DominioFisico()
        self.psicologico = DominioPsicologico()
        self.sociale = DominioSociale()
        self.ambientale = DominioAmbientale()
        self.scorer = QoLScorer()
        self.response_gen = ResponseGenerator()
        
        # Memoria utente (in futuro si può salvare su file)
        self.profilo_utente = {
            "id": "utente_001",
            "storico_punteggi": [],
            "conversazioni": []
        }
    
    def analizza_messaggio(self, messaggio: str) -> dict:
        """
        Analizza un messaggio e restituisce tutti i punteggi
        """
        print("\n" + "="*50)
        print(f"📝 Messaggio: {messaggio}")
        print("="*50)
        
        risultati = {
            "fisico": self.fisico.analizza(messaggio),
            "psicologico": self.psicologico.analizza(messaggio),
            "sociale": self.sociale.analizza(messaggio),
            "ambientale": self.ambientale.analizza(messaggio)
        }
        
        return risultati
    
    def calcola_qol(self, punteggi_domini: dict) -> dict:
        """
        Calcola i punteggi QoL a partire dai punteggi dei domini
        """
        punteggi_trasformati = self.scorer.calcola_tutti_domini(punteggi_domini)
        qol_totale = self.scorer.calcola_qol_totale(punteggi_trasformati)
        
        print("\n" + "="*50)
        print("📊 QUALITÀ DELLA VITA")
        print("="*50)
        for dominio, punteggio in punteggi_trasformati.items():
            print(f"   {dominio.upper()}: {punteggio}")
        print(f"   TOTALE: {qol_totale}")
        
        return {
            "domini": punteggi_trasformati,
            "totale": qol_totale
        }
    
    def genera_risposta(self, messaggio: str, situazione: str = "", emozione: str = "") -> str:
        """
        Genera una risposta empatica
        """
        risposta = self.response_gen.genera_risposta(
            messaggio_utente=messaggio,
            situazione=situazione,
            emozione=emozione
        )
        return risposta
    
    def salva_json(self, messaggio: str, punteggi: dict, qol: dict, risposta: str):
        """
        Salva i risultati in un file JSON
        """
        os.makedirs("dati_json", exist_ok=True)
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "messaggio_utente": messaggio,
            "punteggi_domini": punteggi,
            "qualita_vita": qol,
            "risposta_assistente": risposta
        }
        
        filename = f"dati_json/analisi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dati salvati in {filename}")
        return filename
    
    def elabora_conversazione(self, messaggio: str, situazione: str = "", emozione: str = ""):
        """
        Pipeline completa: analisi → calcolo → risposta → salvataggio
        """
        # 1. Analizza il messaggio
        punteggi = self.analizza_messaggio(messaggio)
        
        # 2. Calcola QoL
        qol = self.calcola_qol(punteggi)
        
        # 3. Genera risposta
        risposta = self.genera_risposta(messaggio, situazione, emozione)
        
        # 4. Salva JSON
        self.salva_json(messaggio, punteggi, qol, risposta)
        
        return risposta


# Modalità interattiva (se eseguito direttamente)
def modalita_interattiva():
    """
    Avvia una conversazione interattiva con l'agente
    """
    print("\n" + "="*50)
    print("🤖 BENVENUTO NELL'ASSISTENTE DI MEDICINA NARRATIVA")
    print("="*50)
    print("Scrivi 'esci' per terminare la conversazione.\n")
    
    agente = MedicinaNarrativaAgent()
    
    while True:
        messaggio = input("Tu: ")
        
        if messaggio.lower() in ['esci', 'quit', 'exit']:
            print("👋 Grazie per aver parlato con me. A presto!")
            break
        
        if messaggio.strip():
            risposta = agente.elabora_conversazione(messaggio)
            print(f"\n🤖 Assistente: {risposta}\n")


# Modalità test (singolo messaggio)
def modalita_test():
    """
    Modalità di test per provare un singolo messaggio
    """
    agente = MedicinaNarrativaAgent()
    
    messaggio_test = "Oggi non mi sento bene. Ho mal di schiena e sono stanco. Non ho voglia di vedere nessuno."
    
    print("\n" + "="*50)
    print("🧪 MODALITÀ TEST")
    print("="*50)
    
    risposta = agente.elabora_conversazione(messaggio_test)
    print(f"\n🤖 Assistente: {risposta}")


if __name__ == "__main__":
    # modalita_interattiva()  # Scommentare per la modalità interattiva
    modalita_test()  # Test con un singolo messaggio
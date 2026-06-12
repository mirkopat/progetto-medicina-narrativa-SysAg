# main.py - VERSIONE CORRETTA COMPLETA
"""
Sistema principale per la medicina narrativa e qualità della vita
"""

import json
import os
from datetime import datetime

from utils.llm_client import LLMClient  # ← client unificato
from classificatori.dominio_fisico import DominioFisico
from classificatori.dominio_psicologico import DominioPsicologico
from classificatori.dominio_sociale import DominioSociale
from classificatori.dominio_ambientale import DominioAmbientale
from qol_scorer import QoLScorer
from response_gen import ResponseGenerator


class MedicinaNarrativaAgent:
    
    def __init__(self, user_id: str = "utente_anonimo"):
        self.user_id = user_id
        self.llm = LLMClient()
        self.fisico = DominioFisico()
        self.psicologico = DominioPsicologico()
        self.sociale = DominioSociale()
        self.ambientale = DominioAmbientale()
        self.scorer = QoLScorer()
        self.response_gen = ResponseGenerator()
    
    def analizza_messaggio(self, messaggio: str) -> dict:
        print("\n" + "="*50)
        print(f"📝 Messaggio: {messaggio}")
        print("="*50)
        
        return {
            "fisico": self.fisico.analizza(messaggio),
            "psicologico": self.psicologico.analizza(messaggio),
            "sociale": self.sociale.analizza(messaggio),
            "ambientale": self.ambientale.analizza(messaggio)
        }
    
    def calcola_qol(self, punteggi_domini: dict) -> dict:
        punteggi_trasformati = self.scorer.calcola_tutti_domini(punteggi_domini)
        qol_totale = self.scorer.calcola_qol_totale(punteggi_trasformati)
        
        print("\n" + "="*50)
        print("📊 QUALITÀ DELLA VITA")
        print("="*50)
        for dominio, punteggio in punteggi_trasformati.items():
            print(f"   {dominio.upper()}: {punteggio}")
        print(f"   TOTALE: {qol_totale}")
        
        return {"domini": punteggi_trasformati, "totale": qol_totale}
    
    def genera_risposta(self, messaggio: str) -> str:
        return self.response_gen.genera_risposta(messaggio_utente=messaggio)
    
    def salva_json(self, punteggi: dict, qol: dict):
        """Salva in un unico file JSON per utente (senza messaggi)"""
        os.makedirs("dati_json", exist_ok=True)
        filename = f"dati_json/{self.user_id}.json"
        
        # Carica dati esistenti se il file esiste ed è valido
        dati = {"user_id": self.user_id, "storico": []}
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    contenuto = f.read().strip()
                    if contenuto:  # Se il file non è vuoto
                        dati = json.loads(contenuto)
            except (json.JSONDecodeError, ValueError):
                print(f"⚠️ File {filename} corrotto, ne creo uno nuovo")
                dati = {"user_id": self.user_id, "storico": []}
        
        nuovo_record = {
            "timestamp": datetime.now().isoformat(),
            "punteggi_domini": qol["domini"],
            "qol_totale": qol["totale"]
        }
        dati["storico"].append(nuovo_record)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dati, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Storico aggiornato in {filename}")
    
    def elabora_conversazione(self, messaggio: str) -> str:
        punteggi = self.analizza_messaggio(messaggio)
        qol = self.calcola_qol(punteggi)
        risposta = self.genera_risposta(messaggio)
        self.salva_json(punteggi, qol)
        return risposta


def modalita_interattiva(user_id: str = "utente"):
    print("\n" + "="*50)
    print("🤖 BENVENUTO NELL'ASSISTENTE DI MEDICINA NARRATIVA")
    print("="*50)
    
    agente = MedicinaNarrativaAgent(user_id=user_id)
    
    # Messaggio di benvenuto per la scrittura riflessiva
    benvenuto = agente.response_gen.genera_invito_narrativa()
    print(f"🤖 Assistente: {benvenuto}\n")
    
    while True:
        messaggio = input("Tu: ")
        if messaggio.lower() in ['esci', 'quit', 'exit']:
            print("👋 Grazie per aver parlato con me. A presto!")
            break
        if messaggio.strip():
            risposta = agente.elabora_conversazione(messaggio)
            print(f"\n🤖 Assistente: {risposta}\n")


def modalita_test():
    print("\n🧪 MODALITÀ TEST")
    agente = MedicinaNarrativaAgent(user_id="test")
    messaggio = "Oggi non mi sento bene. Ho mal di schiena e sono stanco."
    risposta = agente.elabora_conversazione(messaggio)
    print(f"\n🤖 Assistente: {risposta}")


if __name__ == "__main__":
    # Scegli qui la modalità:
    modalita_interattiva(user_id="raimondo")  # ← cambia user_id per ogni persona
    # modalita_test()
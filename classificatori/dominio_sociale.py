# classificatori/dominio_sociale.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import LLMClient

class DominioSociale:
    """Fattori: relazioni, supporto, vita_sessuale"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def _get_punteggio(self, messaggio: str, fattore: str, descrizione: str, scale: dict) -> int:
        prompt = f"""
        Messaggio: "{messaggio}"
        Valuta {descrizione} ({fattore}) su scala 1-5:
        1={scale['1']} 2={scale['2']} 3={scale['3']} 4={scale['4']} 5={scale['5']}
        Rispondi SOLO con il numero.
        """
        try:
            risposta = self.llm.generate(prompt)
            return max(1, min(5, int(risposta.strip())))
        except:
            return 3
    
    def valuta_relazioni(self, messaggio: str) -> int:
        scale = {'1':'Molto insoddisfatto', '2':'Insoddisfatto', '3':'Neutro', '4':'Soddisfatto', '5':'Molto soddisfatto'}
        return self._get_punteggio(messaggio, "relazioni", "soddisfazione delle relazioni personali", scale)
    
    def valuta_supporto(self, messaggio: str) -> int:
        scale = {'1':'Per niente', '2':'Poco', '3':'Abbastanza', '4':'Molto', '5':'Completamente'}
        return self._get_punteggio(messaggio, "supporto", "soddisfazione del sostegno ricevuto da amici e familiari", scale)
    
    def valuta_vita_sessuale(self, messaggio: str) -> int:
        scale = {'1':'Molto insoddisfatto', '2':'Insoddisfatto', '3':'Neutro', '4':'Soddisfatto', '5':'Molto soddisfatto'}
        return self._get_punteggio(messaggio, "vita_sessuale", "soddisfazione della vita sessuale", scale)
    
    def analizza(self, messaggio: str) -> dict:
        print("📊 Analisi dominio SOCIALE...")
        risultati = {
            "relazioni": self.valuta_relazioni(messaggio),
            "supporto": self.valuta_supporto(messaggio),
            "vita_sessuale": self.valuta_vita_sessuale(messaggio)
        }
        print(f"   ✅ Punteggi: {risultati}")
        return risultati

if __name__ == "__main__":
    print("🧪 Test Dominio Sociale")
    dominio = DominioSociale()
    risultati = dominio.analizza("I miei amici mi sono vicini in questo momento difficile")
    print(f"\nRisultati: {risultati}")
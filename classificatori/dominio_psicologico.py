# classificatori/dominio_psicologico.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import LLMClient

class DominioPsicologico:
    """
    Classificatore per il dominio Psicologico della Qualità della Vita
    Fattori: pensieri_positivi, think, stima, percezione_corpo, pensieri_negativi*, spiritualità
    * = reverse item (6 - valore_originale)
    """
    
    def __init__(self):
        self.llm = LLMClient()
    
    def _get_punteggio(self, messaggio: str, fattore: str, descrizione: str, scale: dict) -> int:
        prompt = f"""
        Analizza il seguente messaggio di una persona anziana.
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
    
    def valuta_pensieri_positivi(self, messaggio: str) -> int:
        scale = {'1':'Mai positivo', '2':'Raramente', '3':'Qualche volta', '4':'Spesso', '5':'Sempre positivo'}
        return self._get_punteggio(messaggio, "pensieri_positivi", "quanto spesso hai pensieri positivi", scale)
    
    def valuta_think(self, messaggio: str) -> int:
        scale = {'1':'Impossibile concentrarsi', '2':'Molto difficile', '3':'Difficoltà moderata', '4':'Leggera difficoltà', '5':'Concentrazione ottima'}
        return self._get_punteggio(messaggio, "think", "capacità di concentrazione e funzionamento cognitivo", scale)
    
    def valuta_stima(self, messaggio: str) -> int:
        scale = {'1':'Per niente soddisfatto', '2':'Poco soddisfatto', '3':'Abbastanza', '4':'Soddisfatto', '5':'Molto soddisfatto'}
        return self._get_punteggio(messaggio, "stima", "autostima e soddisfazione di sé", scale)
    
    def valuta_percezione_corpo(self, messaggio: str) -> int:
        scale = {'1':'Molto insoddisfatto', '2':'Insoddisfatto', '3':'Neutro', '4':'Soddisfatto', '5':'Molto soddisfatto'}
        return self._get_punteggio(messaggio, "percezione_corpo", "accettazione del proprio aspetto esteriore", scale)
    
    def valuta_pensieri_negativi(self, messaggio: str) -> int:
        """Reverse item"""
        scale = {'1':'Mai', '2':'Raramente', '3':'Qualche volta', '4':'Spesso', '5':'Sempre'}
        return self._get_punteggio(messaggio, "pensieri_negativi", "presenza di pensieri negativi (malumore, ansia, depressione)", scale)
    
    def valuta_spiritualita(self, messaggio: str) -> int:
        scale = {'1':'Per niente', '2':'Poco', '3':'Abbastanza', '4':'Molto', '5':'Completamente'}
        return self._get_punteggio(messaggio, "spiritualita", "quanto pensi che la tua vita abbia significato", scale)
    
    def analizza(self, messaggio: str) -> dict:
        print("📊 Analisi dominio PSICOLOGICO...")
        risultati = {
            "pensieri_positivi": self.valuta_pensieri_positivi(messaggio),
            "think": self.valuta_think(messaggio),
            "stima": self.valuta_stima(messaggio),
            "percezione_corpo": self.valuta_percezione_corpo(messaggio),
            "pensieri_negativi": self.valuta_pensieri_negativi(messaggio),
            "spiritualita": self.valuta_spiritualita(messaggio)
        }
        print(f"   ✅ Punteggi: {risultati}")
        return risultati

if __name__ == "__main__":
    print("🧪 Test Dominio Psicologico")
    dominio = DominioPsicologico()
    risultati = dominio.analizza("Mi sento giù, non ho voglia di fare niente, mi sembra tutto inutile")
    print(f"\nRisultati: {risultati}")
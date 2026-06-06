# classificatori/dominio_ambientale.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import LLMClient

class DominioAmbientale:
    """Fattori: sicurezza, casa, finanza, servizi, informatività, piaceri, ambiente, trasporti"""
    
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
    
    def valuta_sicurezza(self, messaggio: str) -> int:
        scale = {'1':'Per niente sicuro', '2':'Poco sicuro', '3':'Abbastanza sicuro', '4':'Molto sicuro', '5':'Completamente sicuro'}
        return self._get_punteggio(messaggio, "sicurezza", "quanto ti senti sicuro nella vita quotidiana", scale)
    
    def valuta_casa(self, messaggio: str) -> int:
        scale = {'1':'Pessime', '2':'Cattive', '3':'Sufficienti', '4':'Buone', '5':'Eccellenti'}
        return self._get_punteggio(messaggio, "casa", "condizioni della propria abitazione", scale)
    
    def valuta_finanza(self, messaggio: str) -> int:
        scale = {'1':'Mai', '2':'Raramente', '3':'Qualche volta', '4':'Spesso', '5':'Sempre'}
        return self._get_punteggio(messaggio, "finanza", "le risorse finanziarie bastano per soddisfare i bisogni", scale)
    
    def valuta_servizi(self, messaggio: str) -> int:
        scale = {'1':'Molto insoddisfatto', '2':'Insoddisfatto', '3':'Neutro', '4':'Soddisfatto', '5':'Molto soddisfatto'}
        return self._get_punteggio(messaggio, "servizi", "accessibilità ai servizi sanitari", scale)
    
    def valuta_informativita(self, messaggio: str) -> int:
        scale = {'1':'Mai', '2':'Raramente', '3':'Qualche volta', '4':'Spesso', '5':'Sempre'}
        return self._get_punteggio(messaggio, "informatività", "accessibilità alle informazioni necessarie", scale)
    
    def valuta_piaceri(self, messaggio: str) -> int:
        scale = {'1':'Mai', '2':'Raramente', '3':'Qualche volta', '4':'Spesso', '5':'Sempre'}
        return self._get_punteggio(messaggio, "piaceri", "possibilità di dedicarsi ad attività di svago nel tempo libero", scale)
    
    def valuta_ambiente(self, messaggio: str) -> int:
        scale = {'1':'Pessimo', '2':'Cattivo', '3':'Sufficiente', '4':'Buono', '5':'Eccellente'}
        return self._get_punteggio(messaggio, "ambiente", "qualità dell'ambiente in cui vivi (rumore, inquinamento, clima)", scale)
    
    def valuta_trasporti(self, messaggio: str) -> int:
        scale = {'1':'Molto insoddisfatto', '2':'Insoddisfatto', '3':'Neutro', '4':'Soddisfatto', '5':'Molto soddisfatto'}
        return self._get_punteggio(messaggio, "trasporti", "accessibilità ai mezzi di trasporto", scale)
    
    def analizza(self, messaggio: str) -> dict:
        print("📊 Analisi dominio AMBIENTALE...")
        risultati = {
            "sicurezza": self.valuta_sicurezza(messaggio),
            "casa": self.valuta_casa(messaggio),
            "finanza": self.valuta_finanza(messaggio),
            "servizi": self.valuta_servizi(messaggio),
            "informativita": self.valuta_informativita(messaggio),
            "piaceri": self.valuta_piaceri(messaggio),
            "ambiente": self.valuta_ambiente(messaggio),
            "trasporti": self.valuta_trasporti(messaggio)
        }
        print(f"   ✅ Punteggi: {risultati}")
        return risultati

if __name__ == "__main__":
    print("🧪 Test Dominio Ambientale")
    dominio = DominioAmbientale()
    risultati = dominio.analizza("La mia casa è umida e non mi sento al sicuro nel mio quartiere")
    print(f"\nRisultati: {risultati}")
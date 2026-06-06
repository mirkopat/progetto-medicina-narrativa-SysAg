# classificatori/dominio_fisico.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import LLMClient

class DominioFisico:
    """
    Classificatore per il dominio Fisico della Qualità della Vita
    Fattori: dolore*, energia, sonno, mobilità, attività, medicine*, lavoro
    * = reverse items (6 - valore_originale)
    """
    
    def __init__(self):
        self.llm = LLMClient()
    
    def _get_punteggio(self, messaggio: str, fattore: str, descrizione: str, 
                       scale: dict) -> int:
        """Metodo interno per ottenere un punteggio da Gemini"""
        prompt = f"""
        Analizza il seguente messaggio di un paziente con malattia cronica.
        
        Messaggio: "{messaggio}"
        
        Valuta il livello di {descrizione} ({fattore}).
        
        Scala di valutazione da 1 a 5:
        1 = {scale['1']}
        2 = {scale['2']}
        3 = {scale['3']}
        4 = {scale['4']}
        5 = {scale['5']}
        
        Rispondi SOLO con il numero (da 1 a 5). Non aggiungere altro testo.
        """
        
        try:
            risposta = self.llm.generate(prompt)
            punteggio = int(risposta.strip())
            if 1 <= punteggio <= 5:
                return punteggio
            else:
                return 3
        except:
            return 3
    
    def valuta_dolore(self, messaggio: str) -> int:
        """Reverse item: più alto = peggio"""
        scale = {
            '1': 'Nessun dolore, nessuna limitazione',
            '2': 'Dolore lieve, limitazioni minime',
            '3': 'Dolore moderato, alcune attività limitate',
            '4': 'Dolore forte, molte attività limitate',
            '5': 'Dolore insopportabile, totalmente impedito'
        }
        return self._get_punteggio(messaggio, "dolore", 
                                   "dolore fisico che impedisce le attività quotidiane", scale)
    
    def valuta_energia(self, messaggio: str) -> int:
        scale = {
            '1': 'Nessuna energia, sempre esausto',
            '2': 'Poca energia, mi stanco subito',
            '3': 'Energia moderata',
            '4': 'Buona energia',
            '5': 'Molta energia, pieno di vitalità'
        }
        return self._get_punteggio(messaggio, "energia",
                                   "energia per svolgere attività quotidiane", scale)
    
    def valuta_sonno(self, messaggio: str) -> int:
        scale = {
            '1': 'Molto insoddisfatto, dormo malissimo',
            '2': 'Insoddisfatto, dormo male',
            '3': 'Né soddisfatto né insoddisfatto',
            '4': 'Soddisfatto, dormo bene',
            '5': 'Molto soddisfatto, dormo benissimo'
        }
        return self._get_punteggio(messaggio, "sonno", "qualità del sonno", scale)
    
    def valuta_mobilita(self, messaggio: str) -> int:
        scale = {
            '1': 'Completamente immobilizzato',
            '2': 'Mi muovo con grande difficoltà',
            '3': 'Mi muovo con qualche difficoltà',
            '4': 'Mi muovo abbastanza bene',
            '5': 'Mi muovo liberamente senza problemi'
        }
        return self._get_punteggio(messaggio, "mobilità",
                                   "capacità di muoversi autonomamente", scale)
    
    def valuta_attivita(self, messaggio: str) -> int:
        scale = {
            '1': 'Non riesco a svolgere alcuna attività',
            '2': 'Svolgo poche attività con difficoltà',
            '3': 'Svolgo alcune attività quotidiane',
            '4': 'Svolgo la maggior parte delle attività',
            '5': 'Svolgo tutte le attività senza problemi'
        }
        return self._get_punteggio(messaggio, "attività",
                                   "capacità di svolgere attività quotidiane", scale)
    
    def valuta_medicine(self, messaggio: str) -> int:
        """Reverse item: più alto = più dipendenza"""
        scale = {
            '1': 'Nessuna dipendenza da farmaci',
            '2': 'Dipendenza lieve da farmaci',
            '3': 'Dipendenza moderata',
            '4': 'Dipendenza forte',
            '5': 'Dipendenza totale, non posso farne a meno'
        }
        return self._get_punteggio(messaggio, "medicine",
                                   "dipendenza da farmaci", scale)
    
    def valuta_lavoro(self, messaggio: str) -> int:
        scale = {
            '1': 'Incapacità totale di lavorare',
            '2': 'Grave difficoltà a lavorare',
            '3': 'Difficoltà moderata',
            '4': 'Leggera difficoltà',
            '5': 'Nessuna difficoltà, lavoro normalmente'
        }
        return self._get_punteggio(messaggio, "lavoro",
                                   "capacità di svolgere attività produttive/lavorative", scale)
    
    def analizza(self, messaggio: str) -> dict:
        """Analizza un messaggio e restituisce tutti i punteggi del dominio fisico"""
        print("📊 Analisi dominio FISICO...")
        
        risultati = {
            "dolore": self.valuta_dolore(messaggio),
            "energia": self.valuta_energia(messaggio),
            "sonno": self.valuta_sonno(messaggio),
            "mobilita": self.valuta_mobilita(messaggio),
            "attivita": self.valuta_attivita(messaggio),
            "medicine": self.valuta_medicine(messaggio),
            "lavoro": self.valuta_lavoro(messaggio)
        }
        
        print(f"   ✅ Punteggi: {risultati}")
        return risultati


# Test del modulo
if __name__ == "__main__":
    print("🧪 Test del classificatore Dominio Fisico")
    print("-" * 50)
    
    dominio = DominioFisico()
    
    messaggio_test = "Oggi non mi sento bene, ho mal di schiena e non ho dormito. Sono stanco e non ho voglia di fare nulla."
    
    print(f"Messaggio: {messaggio_test}\n")
    risultati = dominio.analizza(messaggio_test)
    
    print("\n📋 RISULTATI:")
    for fattore, punteggio in risultati.items():
        print(f"   {fattore}: {punteggio}")
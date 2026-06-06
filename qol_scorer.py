# qol_scorer.py
"""
Modulo per il calcolo dei punteggi della Qualità della Vita (QoL)
Basato sul framework WHOQOL-BREF

Formule:
- Per i reverse items: punteggio = 6 - valore_originale
- Punteggio dominio = (media dei fattori) * 4  (scala 4-20)
- Trasformazione 0-100: (punteggio_dominio - 4) * (100 / 16)
"""

class QoLScorer:
    """
    Calcolatore dei punteggi di Qualità della Vita
    """
    
    # Reverse items per ogni dominio
    REVERSE_ITEMS = {
        "fisico": ["dolore", "medicine"],
        "psicologico": ["pensieri_negativi"],
        "sociale": [],  # nessun reverse item
        "ambientale": []  # nessun reverse item
    }
    
    # Fattori per ogni dominio (per verifica)
    FATTORI_DOMINI = {
        "fisico": ["dolore", "energia", "sonno", "mobilita", "attivita", "medicine", "lavoro"],
        "psicologico": ["pensieri_positivi", "think", "stima", "percezione_corpo", "pensieri_negativi", "spiritualita"],
        "sociale": ["relazioni", "supporto", "vita_sessuale"],
        "ambientale": ["sicurezza", "casa", "finanza", "servizi", "informativita", "piaceri", "ambiente", "trasporti"]
    }
    
    def _applica_reverse(self, punteggi: dict, dominio: str) -> dict:
        """
        Applica la trasformazione reverse ai fattori che lo richiedono
        Reverse: 1->5, 2->4, 3->3, 4->2, 5->1
        Formula: punteggio_reverse = 6 - punteggio_originale
        """
        punteggi_adattati = punteggi.copy()
        
        for fattore in self.REVERSE_ITEMS.get(dominio, []):
            if fattore in punteggi_adattati:
                originale = punteggi_adattati[fattore]
                punteggi_adattati[fattore] = 6 - originale
                print(f"   🔄 Reverse item '{fattore}': {originale} -> {punteggi_adattati[fattore]}")
        
        return punteggi_adattati
    
    def calcola_punteggio_dominio(self, punteggi: dict, dominio: str) -> float:
        """
        Calcola il punteggio per un singolo dominio
        
        Args:
            punteggi: dict con i punteggi 1-5 per ogni fattore
            dominio: "fisico", "psicologico", "sociale", "ambientale"
            
        Returns:
            punteggio trasformato in scala 0-100
        """
        # Applica reverse items
        punteggi_reverse = self._applica_reverse(punteggi, dominio)
        
        # Calcola la media dei fattori
        valori = list(punteggi_reverse.values())
        media = sum(valori) / len(valori)
        
        # Calcola punteggio dominio (scala 4-20)
        punteggio_dominio = media * 4
        
        # Trasformazione in scala 0-100
        punteggio_trasformato = (punteggio_dominio - 4) * (100 / 16)
        
        return round(punteggio_trasformato, 2)
    
    def calcola_tutti_domini(self, punteggi: dict) -> dict:
        """
        Calcola i punteggi per tutti i domini
        
        Args:
            punteggi: dict con struttura:
                {
                    "fisico": {"dolore": x, "energia": y, ...},
                    "psicologico": {...},
                    "sociale": {...},
                    "ambientale": {...}
                }
        
        Returns:
            dict con i punteggi trasformati per ogni dominio
        """
        risultati = {}
        
        for dominio in self.FATTORI_DOMINI.keys():
            if dominio in punteggi:
                risultati[dominio] = self.calcola_punteggio_dominio(punteggi[dominio], dominio)
            else:
                print(f"⚠️ Dominio {dominio} non trovato nei punteggi")
                risultati[dominio] = None
        
        return risultati
    
    def calcola_qol_totale(self, punteggi_dominio: dict) -> float:
        """
        Calcola il punteggio totale della Qualità della Vita
        (media dei 4 domini)
        """
        punteggi_validi = [v for v in punteggi_dominio.values() if v is not None]
        
        if not punteggi_validi:
            return 0.0
        
        media_totale = sum(punteggi_validi) / len(punteggi_validi)
        return round(media_totale, 2)


# Test del modulo
if __name__ == "__main__":
    print("🧪 Test del calcolatore QoL")
    print("-" * 50)
    
    scorer = QoLScorer()
    
    # Simula punteggi per il dominio fisico
    punteggi_fisico = {
        "dolore": 4,      # reverse: 6-4=2
        "energia": 2,
        "sonno": 3,
        "mobilita": 3,
        "attivita": 2,
        "medicine": 2,    # reverse: 6-2=4
        "lavoro": 1
    }
    
    print("📊 Punteggi dominio fisico (grezzi):", punteggi_fisico)
    
    punteggio = scorer.calcola_punteggio_dominio(punteggi_fisico, "fisico")
    print(f"📈 Punteggio dominio fisico trasformato (0-100): {punteggio}")
    
    # Test di tutti i domini
    print("\n" + "-" * 50)
    print("📊 Test con tutti i domini:")
    
    tutti_punteggi = {
        "fisico": punteggi_fisico,
        "psicologico": {
            "pensieri_positivi": 3,
            "think": 3,
            "stima": 4,
            "percezione_corpo": 3,
            "pensieri_negativi": 2,  # reverse
            "spiritualita": 3
        },
        "sociale": {
            "relazioni": 4,
            "supporto": 4,
            "vita_sessuale": 3
        },
        "ambientale": {
            "sicurezza": 4,
            "casa": 5,
            "finanza": 3,
            "servizi": 4,
            "informativita": 3,
            "piaceri": 3,
            "ambiente": 4,
            "trasporti": 4
        }
    }
    
    risultati_domini = scorer.calcola_tutti_domini(tutti_punteggi)
    print(f"📈 Punteggi per dominio: {risultati_domini}")
    
    qol_totale = scorer.calcola_qol_totale(risultati_domini)
    print(f"📈 Qualità della Vita totale (0-100): {qol_totale}")
    
    print("\n✅ Test completato!")
# Progetto di Medicina Narrativa - Chatbot per la Valutazione della Qualità della Vita

## Descrizione del progetto

Questo progetto è stato sviluppato per l'esame di **Sistemi ad Agenti** presso il Dipartimento di Informatica dell'Università degli Studi di Bari. L'obiettivo è realizzare un agente conversazionale in grado di interagire con persone anziane, raccogliere narrazioni sulla loro quotidianità e valutare la Qualità della Vita (QoL) secondo il framework WHOQOL-BREF.

Il sistema analizza i messaggi testuali dell'utente e produce punteggi per quattro domini:
- **Fisico** (dolore, energia, sonno, mobilità, attività quotidiane, dipendenza da farmaci, lavoro)
- **Psicologico** (pensieri positivi, concentrazione, autostima, accettazione del corpo, pensieri negativi, spiritualità)
- **Sociale** (relazioni personali, supporto sociale, vita sessuale)
- **Ambientale** (sicurezza, condizioni abitative, risorse finanziarie, accesso ai servizi, informazione, tempo libero, qualità dell'ambiente, trasporti)

I punteggi vengono calcolati su scala 0-100, seguendo le formule di trasformazione del questionario WHOQOL-BREF, inclusa la gestione dei reverse items.

## Ispirazione e riferimenti

Il progetto si ispira a **CArEN (Conversational AgEnt supporting Narrative medicine)**, un assistente virtuale sviluppato nell'ambito della ricerca del dipartimento. CArEN integra un modulo di riconoscimento delle emozioni basato su testo e un generatore di risposte empatiche basato su LLM, con l'obiettivo di supportare pazienti affetti da malattie croniche.

Riferimento bibliografico:
> Miccoli, M., De Carolis, B. N., Palestra, G., & Toma, A. (2025). *Enhancing Digital Narrative Medicine through Emotion Analysis in Conversational Agents*. In Proceedings of UMAP '25, pp. 290-294. ACM.
> [https://dl.acm.org/doi/full/10.1145/3699682.3728334](https://dl.acm.org/doi/full/10.1145/3699682.3728334)

Rispetto a CArEN, il presente progetto estende l'approccio introducendo una valutazione multi-dominio della Qualità della Vita, sostituendo il modulo di emotion recognition con un sistema di classificazione basato sui 24 fattori del WHOQOL-BREF.

## Architettura del sistema

Il sistema è composto dai seguenti moduli:

| Modulo | Descrizione |
|--------|-------------|
| `main.py` | Pipeline principale: acquisizione del messaggio, coordinamento dei classificatori, calcolo dei punteggi, generazione della risposta e salvataggio dei dati |
| `classificatori/` | Quattro moduli (fisico, psicologico, sociale, ambientale) che interrogano l'LLM per ottenere punteggi 1-5 per ciascun fattore |
| `qol_scorer.py` | Calcolatore dei punteggi trasformati (scala 0-100) secondo la formula WHOQOL-BREF, con gestione dei reverse items |
| `response_gen.py` | Generatore di risposte empatiche basato su template, ispirato all'architettura di CArEN |
| `utils/` | Client unificato per LLM (supporta Ollama e Gemini) |
| `config.py` | Configurazioni di sistema (provider LLM, modelli, parametri) |

### LLM supportati

- **Ollama** (modello `gemma2:2b`): esecuzione locale, senza limiti di quota, consigliato per lo sviluppo e il testing
- **Gemini API** (modello `gemini-2.5-flash`): cloud, maggiore qualità, soggetto a limiti di quota giornalieri

Il provider può essere selezionato modificando la variabile `LLM_PROVIDER` nel file `.env`.

## Installazione e avvio

### Prerequisiti

- Python 3.10 o superiore
- Ollama (opzionale, per esecuzione locale)
- Connessione internet (solo per Gemini API)
### Procedura

```bash
# Clonare il repository
git clone https://github.com/tuo-username/progetto-medicina-narrativa-SysAg.git
cd progetto-medicina-narrativa-SysAg

# Installare le dipendenze
pip install -r requirements.txt

# (Opzionale) Scaricare il modello Ollama
ollama pull gemma2:2b

# Avviare il chatbot
python main.py
```

Durante l'esecuzione, il sistema presenta un messaggio di benvenuto che invita l'utente a raccontare la propria giornata (scrittura riflessiva). Per terminare la conversazione, digitare `esci`.

## Interfaccia web (Flask)
Per avviare l'interfaccia web con chat e dashboard dei punteggi:

```bash
python app_flask.py
```
Poi apri il browser su http://127.0.0.1:5000

**Nota sul warning di Flask**: Se compare il messaggio `WARNING: This is a development server...`, nessun problema. È solo un avviso standard di Flask e non influisce sul funzionamento dell'applicazione. Per la demo è perfettamente ok.

## Configurazione del provider LLM
Creare un file .env nella directory principale con il seguente contenuto:

```text
LLM_PROVIDER=ollama
GEMINI_API_KEY=your_api_key_here  # solo se si utilizza Gemini
```

## Sperimentazione e validazione
Il sistema è stato validato mediante un esperimento con 8 personas (profili fittizi di anziani con caratteristiche eterogenee). Per ciascuna persona:

1. Sono stati generati 3 messaggi simulando una conversazione spontanea
2. Il chatbot ha prodotto punteggi QoL per ogni messaggio
3. È stata calcolata la media dei punteggi per dominio
4. Gli stessi profili sono stati sottoposti al questionario WHOQOL-BREF (tramite il tool online neurotoolkit.com/whoqol-bref/)
5. I punteggi del chatbot sono stati confrontati con quelli del questionario

I risultati dell'esperimento sono disponibili nella cartella documentazione/ sotto forma di tabelle Excel e grafici.

**Nota**: Nella cartella "dati_json" sono presenti 9 file, di cui 8 sono personas fittizie. Il file rimanente, "demo_flask.json", riguarda un esempio di utilizzo del sistema con Flask. 

## Struttura del repository
```text
progetto-medicina-narrativa-SysAg/
│
├── classificatori/               # Classificatori per i quattro domini QoL
│   ├── dominio_fisico.py
│   ├── dominio_psicologico.py
│   ├── dominio_sociale.py
│   └── dominio_ambientale.py
│
├── utils/                        # Client per LLM
│   ├── llm_client.py             # Client unificato
│   ├── gemini_client.py          # Client Gemini
│   └── ollama_client.py          # Client Ollama
│
├── templates/                    # Template HTML per Flask
│   └── index.html
│
├── dati_json/                    # File JSON con i punteggi degli utenti (un file per utente)
├── documentazione/               # Materiali di supporto (tabelle Excel, screenshot)
│
├── main.py                       # Pipeline principale (console)
├── app_flask.py                  # Interfaccia web con Flask
├── qol_scorer.py                 # Calcolatore punteggi QoL
├── response_gen.py               # Generatore di risposte empatiche
├── config.py                     # Configurazioni di sistema
├── requirements.txt              # Dipendenze Python
└── README.md                     # Questo file
```

## Dipendenze
Le dipendenze Python sono elencate in requirements.txt:

```text
google-genai
python-dotenv
requests
flask
```

## Limitazioni e sviluppi futuri
**Memoria conversazionale**: Il sistema analizza ogni messaggio in modo indipendente, senza mantenere una cronologia della conversazione. Un possibile miglioramento consiste nell'includere il contesto delle interazioni precedenti.

**Affidabilità dell'LLM**: In alcune circostanze, Ollama può restituire "error 500" (sovraccarico del server). Il sistema implementa meccanismi di fallback che restituiscono punteggi predefiniti (valore 3) in caso di errore.

**Accuratezza per dominio sociale**: Dai risultati sperimentali, il dominio sociale mostra l'errore medio più elevato. Ciò potrebbe essere dovuto alla minore frequenza con cui gli utenti menzionano aspetti relazionali nei messaggi.

**Validazione con utenti reali**: Lo studio è stato condotto su personas simulate. Una validazione con utenti anziani reali consentirebbe una valutazione più affidabile dell'efficacia del sistema.

## Autore
**Mirko Patruno**, con l'aiuto di **Maria Grazia Miccoli**

Corso di Laurea in Informatica

Università degli Studi di Bari "Aldo Moro"

Progetto per l'esame di Sistemi ad Agenti (AA 2025/2026)

## Licenza
Questo progetto è distribuito esclusivamente per scopi accademici e didattici. Non è consentito l'uso commerciale.
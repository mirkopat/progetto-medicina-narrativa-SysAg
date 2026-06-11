# app_flask.py
from flask import Flask, render_template, request, jsonify # type: ignore
import json
import os
from main import MedicinaNarrativaAgent

app = Flask(__name__)
agent = MedicinaNarrativaAgent(user_id="demo_flask")

# Memorizza la cronologia della chat in una lista
chat_history = [{"role": "assistant", "content": "Buongiorno! Raccontami la tua giornata. Come ti senti?"}]

def get_scores():
    """Legge l'ultimo punteggio dal JSON e lo restituisce per il dashboard."""
    json_file = "dati_json/demo_flask.json"
    default_scores = {"fisico": 0, "psicologico": 0, "sociale": 0, "ambientale": 0, "totale": 0}
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if data.get("storico"):
                    last = data["storico"][-1]
                    return {
                        "fisico": last["punteggi_domini"].get("fisico", 0),
                        "psicologico": last["punteggi_domini"].get("psicologico", 0),
                        "sociale": last["punteggi_domini"].get("sociale", 0),
                        "ambientale": last["punteggi_domini"].get("ambientale", 0),
                        "totale": last.get("qol_totale", 0)
                    }
        except: pass
    return default_scores

@app.route("/")
def index():
    """Mostra la pagina principale con chat e dashboard."""
    return render_template("index.html")

@app.route("/get_history", methods=["GET"])
def get_history():
    """Restituisce la cronologia della chat (per il caricamento iniziale)."""
    return jsonify({
        "history": chat_history,
        "scores": get_scores()
    })

@app.route("/send_message", methods=["POST"])
def send_message():
    """Riceve il messaggio, lo elabora e restituisce risposta e punteggi aggiornati."""
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message"}), 400

    global chat_history
    chat_history.append({"role": "user", "content": user_message})

    # Ottiene la risposta dall'agente
    try:
        bot_response = agent.elabora_conversazione(user_message)
    except Exception as e:
        bot_response = f"Errore: {str(e)}"

    chat_history.append({"role": "assistant", "content": bot_response})

    # Recupera i punteggi aggiornati
    latest_scores = get_scores()

    return jsonify({
        "response": bot_response,
        "scores": latest_scores
    })

if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=5000)
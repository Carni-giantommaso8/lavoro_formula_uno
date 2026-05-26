from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
 
app = Flask(__name__)
 
CORS(app, origins=["https://stunning-eureka-gx44w5rr996727pq-4200.app.github.dev"])
 
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="f1user",
        password="securepass",
        database="formula1"
    )
 
@app.route("/")
def home():
    return "Benvenuto nell'API REST della Formula 1"
 
# ─── SCUDERIE ────────────────────────────────────────────────────────────────
 
@app.route("/api/scuderie")
def get_scuderie():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT scuderie.*, sponsor.nome_societa AS nome_sponsor 
            FROM scuderie 
            LEFT JOIN sponsor ON scuderie.id_sponsor = sponsor.id""")
        scuderie = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(scuderie)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/scuderie/<int:id>", methods=['DELETE'])
def delete_scuderia(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scuderie WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Scuderia eliminata con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/scuderie", methods=['POST'])
def add_scuderia():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """INSERT INTO scuderie (nome, team_principal, costruttore_motore, anno_fondazione, id_sponsor) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (data['nome'], data['team_principal'], data['costruttore_motore'],
                               data['anno_fondazione'], data['id_sponsor']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Scuderia inserita con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/scuderie/<int:id>", methods=['PUT'])
def update_scuderia(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """UPDATE scuderie 
                   SET nome=%s, team_principal=%s, costruttore_motore=%s, anno_fondazione=%s, id_sponsor=%s
                   WHERE id=%s"""
        cursor.execute(query, (data['nome'], data['team_principal'], data['costruttore_motore'],
                               data['anno_fondazione'], data['id_sponsor'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Scuderia aggiornata con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# ─── SPONSOR ─────────────────────────────────────────────────────────────────
 
@app.route("/api/sponsor", methods=['GET'])
def get_sponsor():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT id, nome_societa, settore_merceologico,
                          CAST(valore_contratto_annuo AS FLOAT) AS valore_contratto_annuo,
                          CAST(scadenza_contratto AS CHAR) AS scadenza_contratto FROM sponsor""")
        sponsor = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(sponsor), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/sponsor", methods=['POST'])
def add_sponsor():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto)
                          VALUES (%s, %s, %s, %s)""",
                       (data['nome_societa'], data['settore_merceologico'],
                        data['valore_contratto_annuo'], data['scadenza_contratto']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Sponsor inserito con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/sponsor/<int:id>", methods=['PUT'])
def update_sponsor(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE sponsor SET nome_societa=%s, settore_merceologico=%s,
                          valore_contratto_annuo=%s, scadenza_contratto=%s WHERE id=%s""",
                       (data['nome_societa'], data['settore_merceologico'],
                        data['valore_contratto_annuo'], data['scadenza_contratto'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Sponsor aggiornato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/sponsor/<int:id>", methods=['DELETE'])
def delete_sponsor(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sponsor WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Sponsor eliminato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# ─── PILOTI ──────────────────────────────────────────────────────────────────
 
@app.route("/api/piloti", methods=['GET'])
def get_piloti():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT piloti.*, scuderie.nome AS nome_scuderia 
                          FROM piloti LEFT JOIN scuderie ON piloti.id_scuderia = scuderie.id""")
        piloti = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(piloti), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/piloti/<int:id>", methods=['GET'])
def get_pilota(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT piloti.*, scuderie.nome AS nome_scuderia 
                          FROM piloti LEFT JOIN scuderie ON piloti.id_scuderia = scuderie.id
                          WHERE piloti.id=%s""", (id,))
        pilota = cursor.fetchone()
        cursor.close()
        conn.close()
        if not pilota:
            return jsonify({"error": "Pilota non trovato"}), 404
        return jsonify(pilota), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/piloti", methods=['POST'])
def add_pilota():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                       (data['nome'], data['cognome'], data['data_nascita'], data['nazionalita'],
                        data['numero_gara'], data['stipendio_annuo'], data['id_scuderia']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Pilota inserito con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/piloti/<int:id>", methods=['PUT'])
def update_pilota(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE piloti SET nome=%s, cognome=%s, data_nascita=%s, nazionalita=%s,
                          numero_gara=%s, stipendio_annuo=%s, id_scuderia=%s WHERE id=%s""",
                       (data['nome'], data['cognome'], data['data_nascita'], data['nazionalita'],
                        data['numero_gara'], data['stipendio_annuo'], data['id_scuderia'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Pilota aggiornato con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/piloti/<int:id>", methods=['DELETE'])
def delete_pilota(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM piloti WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Pilota eliminato con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# ─── MACCHINE ────────────────────────────────────────────────────────────────
 
@app.route("/api/macchine/scuderia/<int:id_scuderia>", methods=['GET'])
def get_macchina_by_scuderia(id_scuderia):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT macchine.*, scuderie.nome AS nome_scuderia
                          FROM macchine LEFT JOIN scuderie ON macchine.id_scuderia = scuderie.id
                          WHERE macchine.id_scuderia=%s""", (id_scuderia,))
        macchina = cursor.fetchone()
        cursor.close()
        conn.close()
        if not macchina:
            return jsonify({"error": "Macchina non trovata"}), 404
        return jsonify(macchina), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# ─── CIRCUITI ────────────────────────────────────────────────────────────────
 
@app.route("/api/circuiti", methods=['GET'])
def get_circuiti():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM circuiti ORDER BY nome")
        circuiti = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(circuiti), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/circuiti/<int:id>", methods=['GET'])
def get_circuito(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM circuiti WHERE id=%s", (id,))
        circuito = cursor.fetchone()
        cursor.close()
        conn.close()
        if not circuito:
            return jsonify({"error": "Circuito non trovato"}), 404
        return jsonify(circuito), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/circuiti", methods=['POST'])
def add_circuito():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve,
                          record_sul_giro, capacita_spettatori, tipo_circuito)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                       (data['nome'], data['localita'], data['nazione'], data['lunghezza_km'],
                        data['numero_curve'], data['record_sul_giro'],
                        data['capacita_spettatori'], data['tipo_circuito']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Circuito inserito con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/circuiti/<int:id>", methods=['PUT'])
def update_circuito(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE circuiti SET nome=%s, localita=%s, nazione=%s, lunghezza_km=%s,
                          numero_curve=%s, record_sul_giro=%s, capacita_spettatori=%s, tipo_circuito=%s
                          WHERE id=%s""",
                       (data['nome'], data['localita'], data['nazione'], data['lunghezza_km'],
                        data['numero_curve'], data['record_sul_giro'],
                        data['capacita_spettatori'], data['tipo_circuito'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Circuito aggiornato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/circuiti/<int:id>", methods=['DELETE'])
def delete_circuito(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM circuiti WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Circuito eliminato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# ─── GRAN PREMI ──────────────────────────────────────────────────────────────
 
@app.route("/api/gran_premi", methods=['GET'])
def get_gran_premi():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT gran_premi.*, circuiti.nome AS nome_circuito, circuiti.nazione
                          FROM gran_premi
                          LEFT JOIN circuiti ON gran_premi.id_circuito = circuiti.id
                          ORDER BY gran_premi.data_inizio""")
        gran_premi = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(gran_premi), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/gran_premi/<int:id>", methods=['GET'])
def get_gran_premio(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT gran_premi.*, circuiti.nome AS nome_circuito, circuiti.nazione
                          FROM gran_premi LEFT JOIN circuiti ON gran_premi.id_circuito = circuiti.id
                          WHERE gran_premi.id=%s""", (id,))
        gp = cursor.fetchone()
        cursor.close()
        conn.close()
        if not gp:
            return jsonify({"error": "Gran Premio non trovato"}), 404
        return jsonify(gp), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/gran_premi", methods=['POST'])
def add_gran_premio():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito)
                          VALUES (%s, %s, %s, %s, %s)""",
                       (data['nome_evento'], data['edizione_numero'], data['data_inizio'],
                        data['meteo_previsto'], data['id_circuito']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Gran Premio inserito con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/gran_premi/<int:id>", methods=['PUT'])
def update_gran_premio(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE gran_premi SET nome_evento=%s, edizione_numero=%s, data_inizio=%s,
                          meteo_previsto=%s, id_circuito=%s WHERE id=%s""",
                       (data['nome_evento'], data['edizione_numero'], data['data_inizio'],
                        data['meteo_previsto'], data['id_circuito'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Gran Premio aggiornato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/gran_premi/<int:id>", methods=['DELETE'])
def delete_gran_premio(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gran_premi WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Gran Premio eliminato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# ─── SESSIONI ────────────────────────────────────────────────────────────────
 
@app.route("/api/sessioni", methods=['GET'])
def get_sessioni():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        id_gp = request.args.get('id_gran_premio')
        if id_gp:
            cursor.execute("""SELECT sessioni.*, gran_premi.nome_evento
                              FROM sessioni LEFT JOIN gran_premi ON sessioni.id_gran_premio = gran_premi.id
                              WHERE sessioni.id_gran_premio=%s ORDER BY sessioni.orario_inizio""", (id_gp,))
        else:
            cursor.execute("""SELECT sessioni.*, gran_premi.nome_evento
                              FROM sessioni LEFT JOIN gran_premi ON sessioni.id_gran_premio = gran_premi.id
                              ORDER BY sessioni.orario_inizio""")
        sessioni = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(sessioni), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/sessioni/<int:id>", methods=['GET'])
def get_sessione(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT sessioni.*, gran_premi.nome_evento
                          FROM sessioni LEFT JOIN gran_premi ON sessioni.id_gran_premio = gran_premi.id
                          WHERE sessioni.id=%s""", (id,))
        sessione = cursor.fetchone()
        cursor.close()
        conn.close()
        if not sessione:
            return jsonify({"error": "Sessione non trovata"}), 404
        return jsonify(sessione), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/sessioni", methods=['POST'])
def add_sessione():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio)
                          VALUES (%s, %s, %s)""",
                       (data['tipo'], data['orario_inizio'], data['id_gran_premio']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Sessione inserita con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/sessioni/<int:id>", methods=['PUT'])
def update_sessione(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE sessioni SET tipo=%s, orario_inizio=%s, id_gran_premio=%s WHERE id=%s""",
                       (data['tipo'], data['orario_inizio'], data['id_gran_premio'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Sessione aggiornata con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/sessioni/<int:id>", methods=['DELETE'])
def delete_sessione(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessioni WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Sessione eliminata con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# ─── RISULTATI ───────────────────────────────────────────────────────────────
 
@app.route("/api/risultati", methods=['GET'])
def get_risultati():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        id_sessione = request.args.get('id_sessione')
        if id_sessione:
            cursor.execute("""SELECT risultati.*,
                              CONCAT(piloti.nome, ' ', piloti.cognome) AS nome_pilota,
                              sessioni.tipo AS tipo_sessione,
                              gran_premi.nome_evento
                              FROM risultati
                              LEFT JOIN piloti ON risultati.id_pilota = piloti.id
                              LEFT JOIN sessioni ON risultati.id_sessione = sessioni.id
                              LEFT JOIN gran_premi ON sessioni.id_gran_premio = gran_premi.id
                              WHERE risultati.id_sessione=%s
                              ORDER BY risultati.posizione_finale""", (id_sessione,))
        else:
            cursor.execute("""SELECT risultati.*,
                              CONCAT(piloti.nome, ' ', piloti.cognome) AS nome_pilota,
                              sessioni.tipo AS tipo_sessione,
                              gran_premi.nome_evento
                              FROM risultati
                              LEFT JOIN piloti ON risultati.id_pilota = piloti.id
                              LEFT JOIN sessioni ON risultati.id_sessione = sessioni.id
                              LEFT JOIN gran_premi ON sessioni.id_gran_premio = gran_premi.id
                              ORDER BY gran_premi.data_inizio, risultati.posizione_finale""")
        risultati = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(risultati), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/risultati/<int:id>", methods=['GET'])
def get_risultato(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT risultati.*,
                          CONCAT(piloti.nome, ' ', piloti.cognome) AS nome_pilota,
                          sessioni.tipo AS tipo_sessione, gran_premi.nome_evento
                          FROM risultati
                          LEFT JOIN piloti ON risultati.id_pilota = piloti.id
                          LEFT JOIN sessioni ON risultati.id_sessione = sessioni.id
                          LEFT JOIN gran_premi ON sessioni.id_gran_premio = gran_premi.id
                          WHERE risultati.id=%s""", (id,))
        risultato = cursor.fetchone()
        cursor.close()
        conn.close()
        if not risultato:
            return jsonify({"error": "Risultato non trovato"}), 404
        return jsonify(risultato), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/risultati", methods=['POST'])
def add_risultato():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce,
                          numero_pit_stop, id_pilota, id_sessione)
                          VALUES (%s, %s, %s, %s, %s, %s)""",
                       (data['posizione_finale'], data['punti_assegnati'], data['giro_veloce'],
                        data['numero_pit_stop'], data['id_pilota'], data['id_sessione']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Risultato inserito con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/risultati/<int:id>", methods=['PUT'])
def update_risultato(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE risultati SET posizione_finale=%s, punti_assegnati=%s, giro_veloce=%s,
                          numero_pit_stop=%s, id_pilota=%s, id_sessione=%s WHERE id=%s""",
                       (data['posizione_finale'], data['punti_assegnati'], data['giro_veloce'],
                        data['numero_pit_stop'], data['id_pilota'], data['id_sessione'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Risultato aggiornato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/risultati/<int:id>", methods=['DELETE'])
def delete_risultato(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM risultati WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Risultato eliminato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 

 
# ─── CLASSIFICA PILOTI (aggregata) ───────────────────────────────────────────
 
@app.route("/api/classifica/piloti", methods=['GET'])
def get_classifica_piloti():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT piloti.id,
                          CONCAT(piloti.nome, ' ', piloti.cognome) AS pilota,
                          piloti.numero_gara, scuderie.nome AS scuderia,
                          SUM(risultati.punti_assegnati) AS punti_totali,
                          COUNT(CASE WHEN risultati.posizione_finale=1 THEN 1 END) AS vittorie
                          FROM piloti
                          LEFT JOIN risultati ON piloti.id = risultati.id_pilota
                          LEFT JOIN sessioni ON risultati.id_sessione = sessioni.id AND sessioni.tipo='Gara'
                          LEFT JOIN scuderie ON piloti.id_scuderia = scuderie.id
                          GROUP BY piloti.id, piloti.nome, piloti.cognome, piloti.numero_gara, scuderie.nome
                          ORDER BY punti_totali DESC""")
        classifica = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(classifica), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
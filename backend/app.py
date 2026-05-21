from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app= Flask(__name__)

CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="formula1"
    )

@app.route("/")
def home():
    return "Benvenuto nell'API REST della Formula 1"

@app.route("/api/scuderie")
def get_scuderie():
    try:
        conn = get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("""SELECT scuderie.*, sponsor.nome_societa AS nome_sponsor 
            FROM scuderie 
            LEFT JOIN sponsor ON scuderie.id_sponsor = sponsor.id""")
        scuderie=cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(scuderie)
    except Exception as e:
        return jsonify({"error":str(e)}), 500

#
@app.route("/api/sponsor", methods=['GET'])
def get_sponsor():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                id, 
                nome_societa, 
                settore_merceologico, 
                CAST(valore_contratto_annuo AS FLOAT) AS valore_contratto_annuo, 
                CAST(scadenza_contratto AS CHAR) AS scadenza_contratto 
            FROM sponsor
        """
        cursor.execute(query)
        sponsor = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(sponsor), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route("/api/scuderie/<int:id>", methods=['DELETE'])
def delete_scuderia(id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM scuderie WHERE id= %s",(id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message":"Scuderia eliminata con successo"}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/scuderie", methods=['POST'])
def add_scuderia():
    try:
        data=request.json
        conn=get_db_connection()
        cursor=conn.cursor()
        query = """
            INSERT INTO scuderie (nome, team_principal, costruttore_motore, anno_fondazione, id_sponsor) 
            VALUES (%s, %s, %s, %s, %s)
        """
        valori = (data['nome'], data['team_principal'], data['costruttore_motore'], data['anno_fondazione'], data['id_sponsor'])
        
        cursor.execute(query, valori)
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({"message": "Scuderia inserita con successo!"}), 201
    except Exception as e:
        print("ERRORE SERVER DETTAGLIATO:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/api/scuderie/<int:id>", methods=['PUT'])
def update_scuderia(id):
    try:
        data= request.json
        conn = get_db_connection()
        cursor=conn.cursor()
        query="""
            UPDATE scuderie 
            SET nome = %s, team_principal = %s, costruttore_motore = %s, anno_fondazione = %s, id_sponsor = %s
            WHERE id = %s
        """
        valori=(data['nome'], data['team_principal'],data['costruttore_motore'], data['anno_fondazione'], data['id_sponsor'], id)
        cursor.execute(query,valori)
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message":"Scuderia aggiornata con successo"}), 200
    except Exception as e:
        print("ERRORE SERVER:",str(e))
        return jsonify({"error":str(e)}),500

@app.route("/api/sponsor", methods=['POST'])
def add_sponsor():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) 
            VALUES (%s, %s, %s, %s)
        """
        valori = (data['nome_societa'], data['settore_merceologico'], data['valore_contratto_annuo'], data['scadenza_contratto'])
        cursor.execute(query, valori)
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
        query = """
            UPDATE sponsor 
            SET nome_societa = %s, settore_merceologico = %s, valore_contratto_annuo = %s, scadenza_contratto = %s
            WHERE id = %s
        """
        valori = (data['nome_societa'], data['settore_merceologico'], data['valore_contratto_annuo'], data['scadenza_contratto'], id)
        cursor.execute(query, valori)
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
        cursor.execute("DELETE FROM sponsor WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Sponsor eliminato con successo!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/piloti", methods=['GET'])
def get_piloti():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT piloti.*, scuderie.nome AS nome_scuderia 
            FROM piloti 
            LEFT JOIN scuderie ON piloti.id_scuderia = scuderie.id
        """)
        piloti = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(piloti), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/piloti/<int:id>", methods=['DELETE'])
def delete_pilota(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM piloti WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Pilota eliminato con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/piloti", methods=['POST'])
def add_pilota():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valori = (data['nome'], data['cognome'], data['data_nascita'], data['nazionalita'],
                  data['numero_gara'], data['stipendio_annuo'], data['id_scuderia'])
        cursor.execute(query, valori)
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
        query = """
            UPDATE piloti 
            SET nome = %s, cognome = %s, data_nascita = %s, nazionalita = %s,
                numero_gara = %s, stipendio_annuo = %s, id_scuderia = %s
            WHERE id = %s
        """
        valori = (data['nome'], data['cognome'], data['data_nascita'], data['nazionalita'],
                  data['numero_gara'], data['stipendio_annuo'], data['id_scuderia'], id)
        cursor.execute(query, valori)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Pilota aggiornato con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/piloti/<int:id>", methods=['GET'])
def get_pilota(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT piloti.*, scuderie.nome AS nome_scuderia 
            FROM piloti 
            LEFT JOIN scuderie ON piloti.id_scuderia = scuderie.id
            WHERE piloti.id = %s
        """, (id,))
        pilota = cursor.fetchone()
        cursor.close()
        conn.close()
        if not pilota:
            return jsonify({"error": "Pilota non trovato"}), 404
        return jsonify(pilota), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/macchine/scuderia/<int:id_scuderia>", methods=['GET'])
def get_macchina_by_scuderia(id_scuderia):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT macchine.*, scuderie.nome AS nome_scuderia
            FROM macchine
            LEFT JOIN scuderie ON macchine.id_scuderia = scuderie.id
            WHERE macchine.id_scuderia = %s
        """, (id_scuderia,))
        macchina = cursor.fetchone()
        cursor.close()
        conn.close()
        if not macchina:
            return jsonify({"error": "Macchina non trovata"}), 404
        return jsonify(macchina), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
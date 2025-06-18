
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines

DB_PATH = "badge_system.db"

def dict_from_row(row, cursor):
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}

@app.route('/api/personnes', methods=['GET'])
def get_all_personnes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personnes")
    rows = cursor.fetchall()
    result = [dict_from_row(row, cursor) for row in rows]
    conn.close()
    return jsonify(result)

@app.route('/api/personnes', methods=['POST'])
def add_personne():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO personnes (
            unique_id, noms, matriculation, pour_le_compte_de, adresse,
            rccm, id_nat, zone_achat, photo, qr_code, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['unique_id'],
        data['noms'],
        data['matriculation'],
        data['pour_le_compte_de'],
        data['adresse'],
        data['rccm'],
        data['id_nat'],
        data['zone_achat'],
        data.get('photo'),
        data.get('qr_code'),
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Personne ajoutée avec succès"}), 201

if __name__ == "__main__":
    app.run(debug=True)

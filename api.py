from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personnes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Personne(db.Model):
    id = db.Column(db.String, primary_key=True)
    noms = db.Column(db.String, nullable=False)
    matriculation = db.Column(db.String, nullable=False)
    pour_le_compte_de = db.Column(db.String, nullable=False)
    adresse = db.Column(db.String, nullable=False)
    rccm = db.Column(db.String, nullable=False)
    id_nat = db.Column(db.String, nullable=False)
    zone_achat = db.Column(db.String, nullable=False)
    photo = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/api/personnes", methods=["POST"])
def add_person():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données manquantes"}), 400

    person = Personne(
        id=data.get("unique_id"),
        noms=data.get("noms"),
        matriculation=data.get("matriculation"),
        pour_le_compte_de=data.get("pour_le_compte_de"),
        adresse=data.get("adresse"),
        rccm=data.get("rccm"),
        id_nat=data.get("id_nat"),
        zone_achat=data.get("zone_achat"),
        photo=data.get("photo")
    )

    try:
        db.session.add(person)
        db.session.commit()
        return jsonify({"message": "Personne enregistrée"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/personnes", methods=["GET"])
def get_all_personnes():
    personnes = Personne.query.all()
    return jsonify([
        {
            "unique_id": p.id,
            "noms": p.noms,
            "matriculation": p.matriculation,
            "pour_le_compte_de": p.pour_le_compte_de,
            "adresse": p.adresse,
            "rccm": p.rccm,
            "id_nat": p.id_nat,
            "zone_achat": p.zone_achat,
            "photo": p.photo,
            "created_at": p.created_at.isoformat()
        }
        for p in personnes
    ])

@app.route("/api/personnes/<id>", methods=["PUT"])
def update_person(id):
    data = request.get_json()
    person = Personne.query.get(id)
    if not person:
        return jsonify({"error": "Personne non trouvée"}), 404

    person.noms = data.get("noms", person.noms)
    person.matriculation = data.get("matriculation", person.matriculation)
    person.pour_le_compte_de = data.get("pour_le_compte_de", person.pour_le_compte_de)
    person.adresse = data.get("adresse", person.adresse)
    person.rccm = data.get("rccm", person.rccm)
    person.id_nat = data.get("id_nat", person.id_nat)
    person.zone_achat = data.get("zone_achat", person.zone_achat)
    person.photo = data.get("photo", person.photo)

    try:
        db.session.commit()
        return jsonify({"message": "Personne mise à jour"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/personnes/<id>", methods=["DELETE"])
def delete_person(id):
    person = Personne.query.get(id)
    if not person:
        return jsonify({"error": "Personne non trouvée"}), 404

    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Personne supprimée"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

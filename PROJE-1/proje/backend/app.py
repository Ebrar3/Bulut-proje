import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB Bağlantısı - os.getenv() kullanmadan direkt linki veriyoruz
client = MongoClient("mongodb+srv://ebrar3r_db_user:EJPi3SRpinRUqXDt@cluster0.consuu8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.BulutProjeDB
notes_collection = db.notes

@app.route("/")
def home():
    return "Flask çalışıyor! 🚀"

# GET
@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = list(notes_collection.find({}, {'_id': 0}))
    return jsonify(notes)

# POST
@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.json

    if not data or 'title' not in data:
        return jsonify({"error": "Başlık gerekli!"}), 400

    new_note = {
        "title": data['title'],
        "content": data.get('content', '')
    }

    notes_collection.insert_one(new_note)
    return jsonify({"message": "Not başarıyla kaydedildi!"}), 201

if __name__ == "__main__":
    # Tüm ağlardan erişime açmak için host='0.0.0.0' ekledik
    app.run(host='0.0.0.0', debug=True, port=5000)
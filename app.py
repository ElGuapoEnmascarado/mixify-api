from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Conexión con MongoDB Atlas (reemplaza con tu URL real)
client = MongoClient("mongodb+srv://iracheta602:Yahir2003@mixify.4va0z.mongodb.net/mixify?retryWrites=true&w=majority&appName=mixify")
db = client["mixify"]

@app.route("/api/historial_bebidas", methods=["POST"])
def guardar_historial():
    data = request.json
    data["fecha"] = datetime.utcnow()
    db["historial_bebidas"].insert_one(data)
    return jsonify({"msg": "Datos guardados correctamente"})

@app.route("/api/historial_bebidas", methods=["GET"])
def leer_historial():
    bebidas = list(db["historial_bebidas"].find({}, {"_id": 0}))
    return jsonify(bebidas)

@app.route("/api/estado_contenedores", methods=["GET"])
def contenedores():
    conts = list(db["estado_contenedores"].find({}, {"_id": 0}))
    return jsonify(conts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

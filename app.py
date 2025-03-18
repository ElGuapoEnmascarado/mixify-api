from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb+srv://iracheta602:Mixify1234@mixify.4va0z.mongodb.net/?retryWrites=true&w=majority&appName=mixify")
db = client["mixifydb"]  # Aquí indicamos mixifydb

# -------------------
# GET estado_contenedores
@app.route('/api/estado_contenedores', methods=['GET'])
def get_estado():
    data = list(db.estado_contenedores.find())
    for doc in data:
        doc['_id'] = str(doc['_id'])
    return jsonify(data)

# -------------------
# POST historial_bebidas
@app.route('/api/historial_bebidas', methods=['POST'])
def post_historial():
    data = request.json
    db.historial_bebidas.insert_one(data)
    return jsonify({"msg": "Historial guardado correctamente", "data": data}), 201

# -------------------
# (Opcional) GET historial completo
@app.route('/api/historial_bebidas', methods=['GET'])
def get_historial():
    data = list(db.historial_bebidas.find())
    for doc in data:
        doc['_id'] = str(doc['_id'])
    return jsonify(data)

# -------------------
@app.route('/')
def home():
    return "API Mixify funcionando 🚀"

# -------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

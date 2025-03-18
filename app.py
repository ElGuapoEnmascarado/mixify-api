from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb+srv://iracheta602:Mixify1234@mixify.4va0z.mongodb.net/?retryWrites=true&w=majority&appName=mixify")
db = client["mixifydb"]

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
# GET historial completo (opcional)
@app.route('/api/historial_bebidas', methods=['GET'])
def get_historial():
    data = list(db.historial_bebidas.find())
    for doc in data:
        doc['_id'] = str(doc['_id'])
    return jsonify(data)

# -------------------
# POST actualizar Cant_rest
@app.route('/api/actualizar_contenedor', methods=['POST'])
def actualizar_contenedor():
    data = request.json
    nombre = data.get('nombre')
    cantidad_a_restar = data.get('cantidad')

    contenedor = db.estado_contenedores.find_one({"nombre": nombre})
    if not contenedor:
        return jsonify({"error": "Contenedor no encontrado"}), 404

    nueva_cantidad = contenedor["Cant_rest"] - cantidad_a_restar
    if nueva_cantidad < 0:
        nueva_cantidad = 0

    db.estado_contenedores.update_one(
        {"nombre": nombre},
        {"$set": {"Cant_rest": nueva_cantidad}}
    )

    return jsonify({"msg": f"Cantidad actualizada para {nombre}", "nueva_cant": nueva_cantidad}), 200

# -------------------
@app.route('/')
def home():
    return "API Mixify funcionando 🚀"

# -------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

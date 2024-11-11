from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Configura la conexión a MongoDB
client = MongoClient("mongodb://mongodb:27017/")
db = client.weather
collection = db.weather_data

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/data')
def data():
    # Obtiene todos los registros de MongoDB y los convierte en una lista de diccionarios
    records = list(collection.find({}, {"_id": 0, "temperature": 1, "windspeed": 1}))
    return jsonify(records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090)

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from pymongo import MongoClient
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

client = MongoClient("mongodb://mongodb:27017/")
db = client.weather
collection = db.weather_data

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/data')
def data():
    records = list(collection.find({}, {"_id": 0, "temperature": 1, "windspeed": 1}))
    return jsonify(records)

def emit_data():
    while True:
        latest_data = list(collection.find({}, {"_id": 0, "temperature": 1, "windspeed": 1}))
        socketio.emit("update_data", latest_data)
        time.sleep(10)

if __name__ == '__main__':
    thread = threading.Thread(target=emit_data)
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5090,allow_unsafe_werkzeug=True)

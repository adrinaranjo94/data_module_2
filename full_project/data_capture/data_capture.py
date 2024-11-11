import requests
import mysql.connector
from time import sleep

# Configuración de conexión a MySQL
db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="rootpassword",
    database="weather"
)

cursor = db.cursor()

# Función para obtener el clima actual (temperatura y velocidad del viento) y guardarlo en MySQL
def fetch_and_store_current_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.4165&longitude=-3.7026&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Obtiene la temperatura y velocidad del viento actuales de `current_weather`
        temperature = data["current_weather"]["temperature"]
        windspeed = data["current_weather"]["windspeed"]

        # Inserta los datos en MySQL
        cursor.execute("INSERT INTO weather_data (temperature, windspeed) VALUES (%s, %s)", (temperature, windspeed))
        db.commit()
        print(f"Datos insertados: Temperatura={temperature}°C, Velocidad del viento={windspeed} km/h")
    else:
        print("Error al obtener los datos de la API.")

if __name__ == "__main__":
    while True:
        fetch_and_store_current_weather()
        sleep(600)  # Espera una hora antes de la siguiente ejecución

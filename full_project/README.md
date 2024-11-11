# Real-Time Weather Data Heatmap

This project provides a real-time heatmap visualization of weather data (temperature and wind speed) using Flask, Plotly, and Socket.IO. Data is retrieved from the Open-Meteo API, stored in MySQL, and synchronized to MongoDB, which serves as the data source for the visualization. The app utilizes WebSockets to update the heatmap in real time, showing changes in weather data as they occur.

## Project Structure

- `data_capture`: Python script to retrieve weather data from the Open-Meteo API and store it in MySQL.
- `debezium` : Java-based service that synchronizes MySQL data to MongoDB for real-time CDC (Change Data Capture).
- `flask_app` : Flask web server with Socket.IO to provide real-time data to the client for visualization.

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Internet connection to access the Open-Meteo API.

### Installation and Setup

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Environment Configuration:

- Ensure the following settings are configured in the Docker environment files for services that need them:
  - MySQL credentials (MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE).
  - MongoDB connection URI if using a hosted instance.
- Adjust any API credentials or keys needed.

3. Run Docker Compose:
   This will build an run all services defined in the `docker-compose.yml` file.

```bash
docker-compose up --build
```

## Services Overview

1. Data Capture Service (`data_capture`)

- Periodically fetches weather data from the Open-Meteo API.
- Stores retrieved data (temperature and wind speed) in the `weather_data` table in MySQL.
- This script is set to run every 10 minutes, ensuring continuous data collection.

2. Debezium Service (`debezium`)

- A Java service that uses the MySQL CDC (Change Data Capture) mechanism to sync data to MongoDB in near real-time.
- Any changes in the MySQL `weather_data` table are captured and stored in MongoDB, ensuring MongoDB always has the latest data.

3. Flask Web Server (`flask_app`)

- Provides a real-time heatmap visualization of the weather data using Flask, Plotly, and Socket.IO.
- Listens for updates from MongoDB and broadcasts changes to connected clients via WebSockets.
- Displays a scatter plot heatmap of temperature and wind speed on the `/` route.

## Usage

Once the services are running, open a web browser and navigate to http://localhost:5000 to view the real-time heatmap visualization. The heatmap will automatically update whenever new data is received.

## Example Workflow

1. Data Collection: The data_capture service fetches weather data and stores it in MySQL.
2. Data Sync: The Debezium service captures changes in MySQL and syncs them to MongoDB.
3. Real-Time Visualization: The Flask server reads the latest data from MongoDB, pushing updates to the client in real time. The heatmap highlights any recent changes in the data.

## Technical Details

- MySQL: Primary data storage for weather data retrieved from the API.
- MongoDB: Secondary data storage used for real-time CDC (Change Data Capture).
- Debezium: Java-based CDC connector that monitors MySQL for data changes and syncs to MongoDB.
- Flask + Socket.IO: Provides real-time server-to-client communication for updating the Plotly heatmap.
- Plotly: JavaScript library used on the client-side to render the heatmap visualization.

## Requirements

Python 3.8+ for the data_capture and flask_app services.
Java 11 for the Debezium service.

### Example API Request (Open-Meteo)

The data capture service retrieves temperature and wind speed data from the Open-Meteo API:

https://api.open-meteo.com/v1/forecast?latitude=42.36&longitude=-71.05&current_weather=true

## Troubleshooting

- Database Connection Issues: Ensure that MySQL and MongoDB services are up and accessible from other containers.
- Flask Real-Time Updates: If real-time updates are not visible, confirm that Socket.IO is properly connected on both server and client sides.
- Docker Volumes: If data is not persisting as expected, verify Docker volume configurations.

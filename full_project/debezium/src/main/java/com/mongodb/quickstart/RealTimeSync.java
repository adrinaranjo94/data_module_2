package com.mongodb.quickstart;

import com.mongodb.client.*;
import org.bson.Document;

import java.sql.*;
import java.util.Timer;
import java.util.TimerTask;

import static com.mongodb.client.model.Filters.eq;

public class RealTimeSync {

    private static final String MYSQL_URL = "jdbc:mysql://mysql:3306/weather";
    private static final String MYSQL_USER = "root";
    private static final String MYSQL_PASSWORD = "rootpassword";
    private static final String MONGO_URI = "mongodb://mongodb:27017";

    public static void main(String[] args) {
        Timer timer = new Timer();
        timer.schedule(new SyncTask(), 0, 1000); // Ejecuta cada 1 segundo para simular tiempo real
    }

    static class SyncTask extends TimerTask {
        @Override
        public void run() {
            try {
                // Carga el controlador MySQL si es necesario (dependiendo de la versión de Java)
                Class.forName("com.mysql.cj.jdbc.Driver");

                // Conexiones a MySQL y MongoDB
                try (Connection mysqlConnection = DriverManager.getConnection(MYSQL_URL, MYSQL_USER, MYSQL_PASSWORD);
                     MongoClient mongoClient = MongoClients.create(MONGO_URI)) {

                    MongoDatabase mongoDatabase = mongoClient.getDatabase("weather");
                    MongoCollection<Document> mongoCollection = mongoDatabase.getCollection("weather_data");

                    // Consulta y procesa los registros de sync_log
                    String logQuery = "SELECT * FROM sync_log ORDER BY timestamp";
                    try (PreparedStatement logStatement = mysqlConnection.prepareStatement(logQuery);
                         ResultSet logResultSet = logStatement.executeQuery()) {

                        while (logResultSet.next()) {
                            int recordId = logResultSet.getInt("record_id");
                            String action = logResultSet.getString("action");

                            // Consulta el registro en weather_data para obtener los datos completos
                            String dataQuery = "SELECT * FROM weather_data WHERE id = ?";
                            try (PreparedStatement dataStatement = mysqlConnection.prepareStatement(dataQuery)) {
                                dataStatement.setInt(1, recordId);
                                try (ResultSet dataResultSet = dataStatement.executeQuery()) {
                                    if (dataResultSet.next()) {
                                        // Obtiene los datos del registro modificado
                                        int id = dataResultSet.getInt("id");
                                        float temperature = dataResultSet.getFloat("temperature");
                                        float windspeed = dataResultSet.getFloat("windspeed");

                                        Document document = new Document("id", id)
                                                .append("temperature", temperature)
                                                .append("windspeed", windspeed);

                                        // Sincroniza en MongoDB según el tipo de acción
                                        if ("INSERT".equals(action) || "UPDATE".equals(action)) {
                                            mongoCollection.replaceOne(eq("id", id), document, new com.mongodb.client.model.ReplaceOptions().upsert(true));
                                            System.out.println("Sincronizado registro ID " + id + " en MongoDB.");
                                        }
                                    }
                                }
                            }

                            // Limpia el registro de log después de la sincronización
                            String deleteLogQuery = "DELETE FROM sync_log WHERE log_id = ?";
                            try (PreparedStatement deleteLogStatement = mysqlConnection.prepareStatement(deleteLogQuery)) {
                                deleteLogStatement.setInt(1, logResultSet.getInt("log_id"));
                                deleteLogStatement.executeUpdate();
                            }
                        }
                    }
                    System.out.println("Sincronización completa.");
                }
            } catch (ClassNotFoundException e) {
                System.out.println("Error: controlador MySQL no encontrado");
                e.printStackTrace();
            } catch (SQLException e) {
                System.out.println("Error de SQL durante la sincronización");
                e.printStackTrace();
            }
        }
    }
}

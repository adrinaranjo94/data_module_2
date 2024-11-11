CREATE DATABASE IF NOT EXISTS weather;
USE weather;

CREATE TABLE weather_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    temperature FLOAT,
    windspeed FLOAT
);

CREATE TABLE sync_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    record_id INT NOT NULL,
    action VARCHAR(10) NOT NULL, -- 'INSERT' o 'UPDATE'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE TRIGGER after_weather_data_insert
AFTER INSERT ON weather_data
FOR EACH ROW
BEGIN
    INSERT INTO sync_log (record_id, action) VALUES (NEW.id, 'INSERT');
END$$

CREATE TRIGGER after_weather_data_update
AFTER UPDATE ON weather_data
FOR EACH ROW
BEGIN
    INSERT INTO sync_log (record_id, action) VALUES (NEW.id, 'UPDATE');
END$$

DELIMITER ;

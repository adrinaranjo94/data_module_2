# mysql_init.py

import pymysql

# Timezone setting (modifiable)
TIMEZONE = 'Europe/Madrid'

def init_mysql():
    cnx = pymysql.connect(user='root', 
                          password='MyNewPass',
                          host='127.0.0.1')

    cursor = cnx.cursor()

    # Set timezone for MySQL
    cursor.execute(f"SET GLOBAL time_zone = '{TIMEZONE}';")
    cursor.execute(f"SET @@session.time_zone = '{TIMEZONE}';")

    # Drop the existing database if it exists
    query = ("DROP DATABASE IF EXISTS `pluto`;")
    cursor.execute(query)

    # Create a new database
    query = ("CREATE DATABASE IF NOT EXISTS pluto")
    cursor.execute(query)

    # Use the created database
    query = ("USE pluto")
    cursor.execute(query)

    # Create a table for posts with an auto-incrementing id and updated_at field
    query = ('''
    CREATE TABLE posts(
        id INT AUTO_INCREMENT PRIMARY KEY,
        stamp VARCHAR(20),
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute(query)

    # Create a table for audit logs to track changes
    query = ('''
    CREATE TABLE audit_logs(
        id INT AUTO_INCREMENT PRIMARY KEY,
        action VARCHAR(10),
        old_data VARCHAR(255),
        new_data VARCHAR(255),
        event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()

    print(f"MySQL initialized with timezone: {TIMEZONE}")

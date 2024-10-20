import os
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent
from pymysqlreplication.event import QueryEvent
import time


column_names = ["id", "stamp", "updated_at"]

# Function to configure MySQL to enable binlog for row-level replication
def configure_mysql_with_binlog():
    print("Configuring MySQL with binlog enabled...")
    # Modify MySQL configuration inside the Docker container
    cmd = '''
    docker exec some-mysql bash -c "echo '[mysqld]' > /etc/mysql/my.cnf"
    docker exec some-mysql bash -c "echo 'log-bin=mysql-bin' >> /etc/mysql/my.cnf"
    docker exec some-mysql bash -c "echo 'binlog-format=ROW' >> /etc/mysql/my.cnf"
    docker exec some-mysql bash -c "echo 'server-id=1' >> /etc/mysql/my.cnf"
    docker restart some-mysql
    '''
    os.system(cmd)
    print("MySQL binlog configuration completed.")

def process_binlog_event(destination, event):
    """Process each binlog event and insert data into the destination"""
    data = {}
    
    # Print the entire event for debugging purposes
    print("Event data received:", event['values'])

    # Safely map the column names to the values
    for idx, col in enumerate(column_names):
        if f"UNKNOWN_COL{idx}" in event['values']:
            data[col] = event['values'][f"UNKNOWN_COL{idx}"]
        elif col in event['values']:
            data[col] = event['values'][col]
        else:
            print(f"Warning: Column {col} not found in event data.")

    # Insert or update the data in the destination
    destination.insert_data(data)
    print(f"Upserted data from binlog event: {data}")

def start_binlog_monitor(destination):
    """Read binlog events and process them"""
    configure_mysql_with_binlog()
    time.sleep(10)
    destination.connect()  # Connect to the destination database

    # Define connection settings to the MySQL server
    mysql_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "MyNewPass"
    }

    # Create a BinLogStreamReader object to stream binlog events
    stream = BinLogStreamReader(
        connection_settings=mysql_settings,
        server_id=100,  # Must be unique for every slave
        blocking=True,
        only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent]
    )

    # Process the binlog events
    for binlog_event in stream:
        if isinstance(binlog_event, WriteRowsEvent):
            for row in binlog_event.rows:
                print(f"Write event detected: {row}")
                process_binlog_event(destination, {"values": row["values"]})

        elif isinstance(binlog_event, UpdateRowsEvent):
            for row in binlog_event.rows:
                print(f"Update event detected: {row}")
                process_binlog_event(destination, {"values": row["after_values"]})

        elif isinstance(binlog_event, DeleteRowsEvent):
            for row in binlog_event.rows:
                print(f"Delete event detected: {row}")

    stream.close()
    print("Binlog monitoring completed.")

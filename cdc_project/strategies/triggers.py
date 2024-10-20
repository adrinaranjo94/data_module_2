import pymysql
import time

def create_triggers():
    """Create MySQL triggers for capturing insert and update events"""
    cnx = pymysql.connect(user='root', 
                          password='MyNewPass',
                          host='127.0.0.1',
                          database='pluto')

    cursor = cnx.cursor()

    # Trigger for inserts
    query = ('''
    CREATE TRIGGER after_insert_posts
    AFTER INSERT ON posts
    FOR EACH ROW
    BEGIN
        INSERT INTO audit_logs (action, new_data)
        VALUES ('INSERT', CONCAT('ID:', NEW.id, ', Stamp:', NEW.stamp, ', Updated At:', NEW.updated_at));
    END;
    ''')
    cursor.execute(query)

    # Trigger for updates
    query = ('''
    CREATE TRIGGER after_update_posts
    AFTER UPDATE ON posts
    FOR EACH ROW
    BEGIN
        INSERT INTO audit_logs (action, old_data, new_data)
        VALUES ('UPDATE', CONCAT('ID:', OLD.id, ', Stamp:', OLD.stamp, ', Updated At:', OLD.updated_at),
                           CONCAT('ID:', NEW.id, ', Stamp:', NEW.stamp, ', Updated At:', NEW.updated_at));
    END;
    ''')
    cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()

    print("Triggers created successfully.")

def process_trigger_events(destination):
    """Read trigger events from audit_logs and insert into destination (e.g., MongoDB)"""
    cnx = pymysql.connect(user='root',
                          password='MyNewPass',
                          host='127.0.0.1',
                          database='pluto')

    cursor = cnx.cursor()

    # Query to get all events from audit_logs
    query = ('''
    SELECT action, new_data, old_data, event_time
    FROM audit_logs;
    ''')
    cursor.execute(query)

    results = cursor.fetchall()

    # Insert the changes into the destination database
    for row in results:
        data = {
            "action": row[0],
            "new_data": row[1],
            "old_data": row[2],
            "event_time": row[3]
        }
        destination.insert_data(data)
        print(f"Inserted trigger event into destination: {data}")

    cursor.close()
    cnx.close()

def start_trigger_monitor(destination):
    """Monitor the audit_logs for trigger events and process them"""
    create_triggers()
    destination.connect()  # Connect to the destination database
    while True:
        process_trigger_events(destination)
        time.sleep(60)  # Check for new trigger events every minute

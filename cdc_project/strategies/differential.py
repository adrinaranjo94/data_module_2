import pymysql
import time
from destinations.base_destination import BaseDestination

def differential_query(destination):
    print("Starting differential query...")

    # Connect to MySQL database
    cnx = pymysql.connect(user='root',
                          password='MyNewPass',
                          host='127.0.0.1',
                          database='pluto')

    cursor = cnx.cursor()

    # Query to get records updated in the last 1 minute
    query = ('''
    SELECT id, stamp, updated_at 
    FROM posts 
    WHERE updated_at >= NOW() - INTERVAL 1 MINUTE;
    ''')
    cursor.execute(query)

    results = cursor.fetchall()

    # Insert the changes into the destination database
    for row in results:
        data = {
            "id": row[0],
            "stamp": row[1],
            "updated_at": row[2]
        }
        destination.insert_data(data)
        print(f"Inserted data into destination: {data}")

    cursor.close()
    cnx.close()

    print("Differential query completed.")

# Function to continuously monitor the database using the differential query
def start_differential_monitor(destination):
    try:
        destination.connect()  # Connect to the destination database
        while True:
            differential_query(destination)
            time.sleep(60)  # Run the query every 60 seconds
    except KeyboardInterrupt:
        print("Differential query stopped.")

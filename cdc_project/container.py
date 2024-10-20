import sys
import os
from db_init import mysql_init, mongo_init
from strategies.differential import start_differential_monitor
from strategies.binlog import start_binlog_monitor
from strategies.triggers import start_trigger_monitor
from destinations.mongo_destination import MongoDestination
# Import other destinations as needed

# Function to select destination database based on the --to argument
def select_destination(destination_type):
    if destination_type == 'mongo':
        return MongoDestination()
    else:
        print(f"Unknown destination: {destination_type}")
        return None

# Function to handle different strategies with the selected destination
def start_monitoring_with_strategy(strategy, destination_type):
    destination = select_destination(destination_type)
    
    if not destination:
        print(f"Invalid destination: {destination_type}")
        return

    if strategy == 'differential':
        start_differential_monitor(destination)
    elif strategy == 'binlog':
        start_binlog_monitor(destination)
    elif strategy == 'triggers':
        start_trigger_monitor(destination)
    else:
        print(f"Unknown strategy: {strategy}")

# Function to delete specific Docker containers
def delete_containers():
    containers_to_delete = ['some-mysql', 'some-mongo']  # Names of the containers

    for container in containers_to_delete:
        print(f"Stopping and removing container: {container}")
        
        # Stop the container (if running)
        stop_cmd = f"docker stop {container}"
        os.system(stop_cmd)
        
        # Remove the container
        remove_cmd = f"docker rm {container}"
        os.system(remove_cmd)

    print("Specified containers have been deleted.")

# Read input arguments
if len(sys.argv) > 1:
    command = sys.argv[1]

    if command == '-init':
        # Check if strategy and destination are provided
        if len(sys.argv) > 5 and sys.argv[2] == '--strategy' and sys.argv[4] == '--to':
            strategy = sys.argv[3]
            destination_type = sys.argv[5]

            print(f"Initializing MySQL and starting {strategy} strategy to {destination_type}...")

            # Initialize MySQL
            mysql_init.init_mysql()
            # initialize Mongo
            mongo_init.init_mongo()

            # Start monitoring with the selected strategy and destination
            start_monitoring_with_strategy(strategy, destination_type)
        else:
            print("Usage: -init --strategy [differential|binlog|triggers] --to [mongo]")
    elif command == '-delete':
        # Delete the containers for MySQL and MongoDB
        delete_containers()
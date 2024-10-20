from pymongo import MongoClient

# Function to initialize MongoDB (if needed)
def init_mongo():
    """Initialize MongoDB by dropping the existing database if it exists"""
    
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    
    # Specify the database name
    db_name = 'cdc_database'

    # Drop the existing database if it exists
    if db_name in client.list_database_names():
        client.drop_database(db_name)
        print(f"Database '{db_name}' dropped.")
    else:
        print(f"No existing database '{db_name}' found.")

    # Initialize the database
    db = client[db_name]
    print(f"Database '{db_name}' initialized.")

    # Optionally, initialize a collection (like cdc_collection)
    collection_name = 'cdc_collection'
    db.create_collection(collection_name)
    print(f"Collection '{collection_name}' created.")

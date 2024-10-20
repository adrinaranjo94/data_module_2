from pymongo import MongoClient
from destinations.base_destination import BaseDestination

class MongoDestination(BaseDestination):
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """Connect to MongoDB"""
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['cdc_database']
        self.collection = self.db['cdc_collection']
        print("Connected to MongoDB")

    def insert_data(self, data):
        """Insert or update data into MongoDB collection (upsert)"""
        # Assuming 'id' is the unique identifier
        query = {"id": data.get("id")}
        
        # Update the document if it exists, insert if it doesn't
        self.collection.update_one(query, {"$set": data}, upsert=True)
        print(f"Upserted data into MongoDB: {data}")

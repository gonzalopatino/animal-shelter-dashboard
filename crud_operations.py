import os
import uuid
from pymongo import MongoClient


class AnimalShelter:
    """CRUD operations for the Animal collection in MongoDB."""

    def __init__(self):
        """Initialize MongoDB connection using environment variables."""
        # Fetch connection variables from environment
        USER = os.getenv('MONGO_USER')  # Fetch MongoDB user
        PASS = os.getenv('MONGO_PASS')  # Fetch MongoDB password
        HOST = os.getenv('MONGO_HOST')  # Fetch MongoDB host
        PORT = int(os.getenv('MONGO_PORT'))  # Fetch MongoDB port
        DB = 'AAC'  # MongoDB database name
        COL = 'animals'  # MongoDB collection name

        try:
            # Initialize MongoDB connection
            self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
            self.database = self.client[DB]
            self.collection = self.database[COL]
            print(f"Connected to MongoDB database: {DB}, collection: {COL}")
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")

    def generate_uuid(self):
        """Generate a unique UUID for animal_id."""
        return str(uuid.uuid4())  # Generate and return a UUID as a string

    def create(self, data):
        """Insert a new document into the collection."""
        if data:
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        else:
            raise ValueError("No data provided for insertion.")

    def read(self, query):
        """Query documents from the collection."""
        try:
            cursor = self.collection.find(query)
            return [doc for doc in cursor]
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def update(self, query, update_values):
        """Update documents in the collection."""
        try:
            result = self.collection.update_many(query, update_values)
            return result.modified_count
        except Exception as e:
            print(f"An error occurred during update: {e}")
            return 0

    def delete(self, query):
        """Delete documents from the collection."""
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"An error occurred during delete: {e}")
            return 0

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()
        print("MongoDB connection closed.")

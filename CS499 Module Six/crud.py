# crud.py
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Load environment variables from .env to securely access DB credentials
load_dotenv()

class AnimalShelter:
    # Singleton MongoClient to avoid reconnecting repeatedly
    _client = None

    def __init__(self):
        # Load connection details from environment variables
        user = os.getenv('MONGO_USER')
        password = os.getenv('MONGO_PASS')
        host = os.getenv('MONGO_HOST', 'localhost')
        port = int(os.getenv('MONGO_PORT', '27017'))
        db_name = os.getenv('MONGO_DB', 'AAC')
        col_name = os.getenv('MONGO_COL', 'animals')

        # Decide connection URI based on presence of authentication info
        if user and password:
            mongo_uri = f'mongodb://{user}:{password}@{host}:{port}'
            print(f"Connecting with authentication to {host}:{port}")
        else:
            mongo_uri = f'mongodb://{host}:{port}'
            print(f"Connecting without authentication to {host}:{port}")

        try:
            # Initialize the MongoClient if it hasn't been created yet
            if AnimalShelter._client is None:
                AnimalShelter._client = MongoClient(mongo_uri)
            self.client = AnimalShelter._client

            # Access the specified database and collection
            self.database = self.client[db_name]
            self.collection = self.database[col_name]
            print("MongoDB connection successful.")
        except Exception as e:
            print(f"Error initializing MongoDB connection: {e}")
            raise

        # Keep counters to track how many records are updated/ deleted during operations
        self._records_updated = 0
        self._records_matched = 0
        self._records_deleted = 0

    def create_record(self, data):
        # Check input data before trying to insert
        if not data:
            raise ValueError("No document to save. Data is empty.")

        try:
            # Insert a single record and print the new document's unique ID
            result = self.collection.insert_one(data)
            print(f"Inserted document with id: {result.inserted_id}")
            return result.acknowledged
        except Exception as e:
            print(f"Error inserting document: {e}")
            return False

    def get_record_by_id(self, post_id):
        # Retrieve one document by its MongoDB ObjectId
        try:
            doc = self.collection.find_one({'_id': ObjectId(post_id)})
            print(f"Retrieved document by id: {doc}")
            return doc
        except Exception as e:
            print(f"Error retrieving document by id: {e}")
            return None

    def get_records(self, criteria=None):
        # Fetch documents matching criteria or all if none specified
        try:
            if criteria:
                print(f"Finding documents with criteria: {criteria}")
                cursor = self.collection.find(criteria, {'_id': 0})  # exclude MongoDB internal _id by default
            else:
                print("Finding all documents")
                cursor = self.collection.find({}, {'_id': 0})

            docs = list(cursor)
            print(f"Found {len(docs)} documents.")
            return docs
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def update_record(self, query, new_value):
        # Make sure query and new data are provided before updating
        if not query:
            raise ValueError("No search criteria is present.")
        if not new_value:
            raise ValueError("No update value is present.")

        try:
            # Perform bulk update and track matched/modified counts
            result = self.collection.update_many(query, {"$set": new_value})
            self._records_updated = result.modified_count
            self._records_matched = result.matched_count
            print(f"Update: matched {self._records_matched}, modified {self._records_updated}")
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating documents: {e}")
            return False

    def delete_record(self, query):
        # Check query before attempting delete operation
        if not query:
            raise ValueError("No search criteria is present.")

        try:
            # Delete matching documents and track how many were removed
            result = self.collection.delete_many(query)
            self._records_deleted = result.deleted_count
            print(f"Deleted {self._records_deleted} documents.")
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False

    # Properties to safely access operation counters
    @property
    def records_updated(self):
        return self._records_updated

    @property
    def records_matched(self):
        return self._records_matched

    @property
    def records_deleted(self):
        return self._records_deleted


# If I run crud.py by itself, this block runs some basic tests and prints results
if __name__ == "__main__":
    shelter = AnimalShelter()

    print("Testing: create_record")
    shelter.create_record({"name": "Test Dog", "breed": "Labrador", "age_upon_outcome": "2 years"})

    print("Testing: get_records")
    records = shelter.get_records()
    print(f"Records: {records[:2]}")  # Show first two records for quick check

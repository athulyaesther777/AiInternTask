# src/mongodb_handler.py
from pymongo import MongoClient

# Initialize MongoDB connection (adjust the connection string accordingly)
client = MongoClient('mongodb://localhost:27017/')
db = client['pdf_database']
collection = db['pdf_metadata']

def insert_mongodb(metadata):
    # Insert the PDF metadata initially
    result = collection.insert_one(metadata)
    return result.inserted_id

def update_mongodb(document_name, summary_and_keywords):
    # Find the document by name and update the summary and keywords
    result = collection.update_one(
        {"name": document_name},
        {"$set": {
            "summary": summary_and_keywords['summary'],
            "keywords": summary_and_keywords['keywords']
        }}
    )
    return result.modified_count

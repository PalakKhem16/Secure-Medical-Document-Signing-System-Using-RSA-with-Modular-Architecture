"""
db.py — MongoDB connection and collection accessors.
Reads MONGO_URI and DB_NAME from environment variables.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME: str   = os.getenv("DB_NAME", "medisign")

# Single MongoClient instance (reused across all requests)
_client = MongoClient(MONGO_URI)
_db     = _client[DB_NAME]


def get_db():
    """Return the database instance."""
    return _db


def get_collection(name: str):
    """Return a named collection from the database."""
    return _db[name]


#  Named collection helpers 
doctors_col   = _db["doctors"]
documents_col = _db["documents"]
keys_col      = _db["keys"]
audit_col     = _db["audit"]

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

load_dotenv(override=True)


def test_connection():
    mongo_uri = os.getenv("MONGODB_URI")
    assert mongo_uri, "MONGODB_URI not found in .env"

    print("Attempting to connect to MongoDB Atlas...")
    client = MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=10000,
    )
    result = client.admin.command("ping")
    assert result.get("ok") == 1.0 or result.get("ok") == 1
    print("Connection successful! MongoDB is reachable.")
    dbs = client.list_database_names()
    print(f"Accessible databases: {dbs}")
    client.close()


if __name__ == "__main__":
    try:
        test_connection()
    except (ConnectionFailure, PyMongoError, AssertionError) as e:
        print(f"Connection test failed: {e}")

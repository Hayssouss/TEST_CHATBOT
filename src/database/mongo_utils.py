import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def connect_mongo():
    try:
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client[os.getenv("MONGO_DB")]
        print("✅ Connexion MongoDB réussie")
        return db
    except Exception as e:
        print(f"❌ Erreur MongoDB : {e}")
        return None

# Test de connexion
if __name__ == "__main__":
    db = connect_mongo()
    if db is not None:
        print("📦 Collections MongoDB :", db.list_collection_names())

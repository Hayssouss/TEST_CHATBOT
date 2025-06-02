import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect_postgres():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        print("✅ Connexion PostgreSQL réussie")
        return conn
    except Exception as e:
        print(f"❌ Erreur PostgreSQL : {e}")
        return None

# Test de connexion
if __name__ == "__main__":
    conn = connect_postgres()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        print("📋 Tables PostgreSQL :", cur.fetchall())
        cur.close()
        conn.close()

import streamlit as st
import pandas as pd
import psycopg2
import pymongo
import os
from dotenv import load_dotenv
from google.generativeai import configure, GenerativeModel

# ➔ Charger les variables d'environnement
load_dotenv()

# Configuration Gemini
configure(api_key=os.getenv("API_KEY_GOOGLE"))
model = GenerativeModel(os.getenv("LLM_MODEL"))

# ➔ Connexion PostgreSQL
pg_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

# ➔ Connexion MongoDB
mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client[os.getenv("MONGO_DB")]

# ➔ Chemins des prompts
PROMPT_STRUCTURED_PATH = os.getenv("PROMPT_STRUCTURED_PATH")
PROMPT_UNSTRUCTURED_PATH = os.getenv("PROMPT_UNSTRUCTURED_PATH")

def get_postgres_tables():
    with pg_conn.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        return [row[0] for row in cur.fetchall()]

def get_postgres_table_preview(table):
    return pd.read_sql_query(f"SELECT * FROM {table} LIMIT 20", pg_conn)

def get_mongodb_collections():
    return mongo_db.list_collection_names()

def get_mongodb_preview(collection):
    docs = list(mongo_db[collection].find().limit(20))
    for doc in docs:
        doc.pop("_id", None)
    return pd.DataFrame(docs)

def detect_source_from_question(question):
    if "table" in question.lower():
        return "postgres"
    elif "collection" in question.lower():
        return "mongo"
    return None

def extract_target_name(question):
    parts = question.lower().split(" ")
    for i, part in enumerate(parts):
        if part in ["table", "collection"] and i+1 < len(parts):
            return parts[i+1]
    return None

def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def classify(question):
    source = detect_source_from_question(question)
    target = extract_target_name(question)
    if not source or not target:
        return "❌ Impossible de détecter la table ou collection dans la question."

    if source == "postgres":
        try:
            df = get_postgres_table_preview(target)
            cols = df.dtypes.reset_index()
            cols.columns = ["nom", "type"]
            description = "\n".join([f"- {row['nom']} ({row['type']})" for _, row in cols.iterrows()])
            prompt = load_prompt(PROMPT_STRUCTURED_PATH)
        except:
            return "❌ Table PostgreSQL introuvable."
    else:
        try:
            docs = mongo_db[target].find_one()
            if docs:
                description = f"Nom de la collection : {target}\nContenu exemple : {docs}"
            else:
                description = f"Nom de la collection : {target}\nContenu exemple : vide"
            prompt = load_prompt(PROMPT_UNSTRUCTURED_PATH)
        except:
            return "❌ Collection MongoDB introuvable."

    full_prompt = f"{prompt}\n\n{description}"
    response = model.generate_content(full_prompt)
    return response.text

# ➔ UI Streamlit
st.set_page_config(layout="wide")
st.title("🔐 Classification des Données")

source_type = st.radio("Type de source à afficher :", ["Table PostgreSQL", "Collection MongoDB"], horizontal=True)

if source_type == "Table PostgreSQL":
    tables = get_postgres_tables()
    selected_table = st.selectbox("Choisir une table :", tables)
    st.dataframe(get_postgres_table_preview(selected_table), use_container_width=True)
else:
    collections = get_mongodb_collections()
    selected_collection = st.selectbox("Choisir une collection :", collections)
    st.dataframe(get_mongodb_preview(selected_collection), use_container_width=True)

st.markdown("---")
st.header("🔐 Chatbot de Classification")
question = st.text_input("Posez votre question (ex: classifie la table clients)")
if st.button("Envoyer"):
    with st.spinner("⏳ Traitement en cours..."):
        reponse = classify(question)
        st.markdown(reponse)

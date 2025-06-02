import pymongo
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Charger les variables du fichier .env
load_dotenv()

# 🔐 Configurer l'API Gemini
genai.configure(api_key=os.getenv("API_KEY_GOOGLE"))

# 🔌 Connexion à MongoDB
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB")
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db_name]

# 🧾 Nom de la collection à tester (tu peux changer ici)
collection_name = "logs"
collection = db[collection_name]

# 🧠 Charger le prompt pour données non structurées
with open("C:/Users/smart/Desktop/UIR/STAGE/chatbot_classification/prompts/prompt_unstructured.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

# 🔎 Exemple d'un document
sample = collection.find_one()
if not sample:
    raise ValueError(f"Aucun document trouvé dans la collection '{collection_name}'")

# 🧠 Construire la liste des champs avec types
champ_liste = ", ".join([f"{k}: {type(v).__name__}" for k, v in sample.items()])

# 🧾 Construire le prompt final
full_prompt = base_prompt.replace("{{collection_name}}", collection_name).replace("{{champ_liste}}", champ_liste)

# 🤖 Générer la réponse avec Gemini
model = genai.GenerativeModel(os.getenv("LLM_MODEL"))
response = model.generate_content(full_prompt)

# ✅ Affichage
print("===== 📋 Résultat du LLM =====\n")
print(response.text)

import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# === 🔧 Chargement des variables d'environnement ===
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY_GOOGLE"))

# === 📂 Fichier CSV source ===
csv_path = "C:/Users/smart/Desktop/UIR/STAGE/chatbot_classification/data/structured/cleaned/clients.csv"  # Change si besoin
table_name = os.path.splitext(os.path.basename(csv_path))[0].capitalize()  # Extrait "employes" et met "Employes"

# === 📄 Fichier prompt.txt ===
prompt_path = "C:/Users/smart/Desktop/UIR/STAGE/chatbot_classification/prompts/prompt_structured.txt"

# Charger les 5 premières lignes
df = pd.read_csv(csv_path)
df_sample = df.head()

# Déduire les types
typed_columns = []
for col in df_sample.columns:
    sample_dtype = df_sample[col].dtype
    if "int" in str(sample_dtype):
        col_type = "INT"
    elif "float" in str(sample_dtype):
        col_type = "DECIMAL"
    elif "date" in col.lower() or "embauche" in col.lower():
        col_type = "DATE"
    else:
        col_type = "VARCHAR"
    typed_columns.append(f"- {col} ({col_type})")

colonnes_block = "\n".join(typed_columns)

# Lire le prompt
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt_template = f.read()

# Insère dynamiquement le nom de la table et ses colonnes
if "{colonnes}" in prompt_template and "{table}" in prompt_template:
    full_prompt = prompt_template.replace("{colonnes}", colonnes_block).replace("{table}", table_name)
else:
    full_prompt = f"🧾 Table : {table_name}\nColonnes :\n{colonnes_block}\n\n" + prompt_template

# Génération avec Gemini
model = genai.GenerativeModel("models/gemini-1.5-flash-001")
response = model.generate_content(full_prompt)

# Résultat
print("===== 📋 Résultat du LLM =====\n")
print(response.text)

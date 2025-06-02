# Chatbot Classification Project
    I.STRUCTURE DU PROJET 
       
       
        chatbot_classification/
│
├── .env                                #  Clés API et infos sensibles
├── requirements.txt                    #  Dépendances Python
├── README.md                           #  Documentation projet
├── main.py                             #  Entrée principale (test global ou démo)
│
│
├── data/
│   ├── structured/                     #  Données PostgreSQL (CSV / SQL)
│   │   ├── cleaned/
│   │   └── structure_banque.sql
│   └── unstructured/                  #  Données MongoDB (PDF, emails, .txt…)
│       ├── raw/
│       └── cleaned/
│
├── models/                             #  Modèles LLM locaux (.gguf) ou checkpoints
│
├── prompts/
│   └── prompt_structured.txt            #  Prompt de classification (F, C, R, O)
│   └── prompt_unstructured.txt
├── src/
│   ├── chatbot/                        #  Logique du chatbot
│   │   └── chatbot_engine.py
│
│   ├── classification/                #  Code de classification
│   │   ├── test_md.py
│   │   └── test_pg.py
│
│
│   ├── database/                      #  Connexion PostgreSQL & MongoDB
│   │   ├── postgres_utils.py
│   │   └── mongo_utils.py
│
│   ├── dashboard/                     #  Interface utilisateur (Streamlit ou autre)
│   │   ├── app.py                       # Test simple de prompt sans interface

│   └── utils/                         # Fonctions utilitaires
│       └── helpers.py
│

    II.REQUIREMENTS 

    #  LLM + LangChain
langchain>=0.1.17
langchain-community>=0.0.34
langchain-core>=0.1.34
google-generativeai>=0.3.2          # pour Gemini
transformers                        # si tu veux tester HF ou LLM local plus tard
llama-cpp-python                    # si tu utilises llama.cpp

#  Embeddings & vector search
faiss-cpu                          # moteur vectoriel rapide

#  Bases de données
psycopg2-binary                    # PostgreSQL
pymongo                            # MongoDB

#  Interface utilisateur
streamlit                          # dashboard interactif

#  Tests
pytest

#  Utilitaires
python-dotenv                      # pour charger .env
PyYAML                             # pour parser les fichiers YAML

#  Optionnel mais utile
tqdm                               # barre de progression
rich                               # affichage CLI élégant

    III.ETAPES D'EXECUTION DU PROJET
        1.CREATION D'UN ENVIRONNEMENT VIRTUEL
            PS C:\Users\smart\Desktop\UIR\STAGE\chatbot_classification>python -m venv llama_env
                                                                    .\llama_env\Scripts\activate
        
        2.INSTALLATION DES EXIGENCES
            (llama_env) PS C:\Users\smart\Desktop\UIR\STAGE\chatbot_classification>pip install -r requirements.txt

        3.VERIFICATION DU FICHIER .env ET L'ADAPTER SELON VOUS

        4.VERIFICATION DES DONNEES STRUCTURES ET NON STRUCTURES ET ASSURER LEUR IMPORTATION (POSTGRES,MONGODB)

        5.LANCEMENT DU TEST
            (llama_env) PS C:\Users\smart\Desktop\UIR\STAGE\chatbot_classification> streamlit run .\src\dashboard\app.py

IMPORTANT !! : IL FAUT IMPORTER LES DONNES (FICHIER ./data) DANS LES BASES DE DONNEES (POSTGRES:DONNEES STRUCTURES / MONGODB:DONNEES NON STRUCTURES) 

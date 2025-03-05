from flask import Flask, request, jsonify, send_from_directory
# from pydantic import BaseModel
# import mlflow
# import spacy
# import numpy as np
# from gensim.models import Word2Vec
# from sklearn.preprocessing import LabelEncoder
# import joblib  # Pour charger le modèle de classification
# from sklearn.linear_model import LogisticRegression
import os
import sys
from datetime import datetime
from pymongo import MongoClient

print("a")
MONGO_URI = os.getenv("MONGO_DB_URI", "mongodb://mongo:27017/")

# Créer l'application Flask
app = Flask(__name__, static_folder='static')

# Connexion à MongoDB
try:
  # Establish connection
  client = MongoClient("mongodb://mongo:27017/")

  # Test the connection
  db_list = client.list_database_names()
  db = client.get_database("dev")
  collection = db.get_collection("front_app_logs")
  print("Successfully connected to MongoDB")
  print("Databases:", db_list)

except Exception as e:
  print("Error connecting to MongoDB:", e)
  sys.exit(1)  # Exit the program if connection fails

# # Charger les modèles et outils nécessaires
# try:
#     # Charger le modèle à partir de MLflow
#     model = mlflow.sklearn.load_model(f"runs:/5fefbe6797a24f0fafc544605ae42970/oui")  # Remplacez avec l'ID du run et le nom du modèle
    
#     # Charger le modèle Word2Vec
#     vectorizer = Word2Vec.load('word2vec_model.bin')  # Modèle Word2Vec
#     label_encoder = joblib.load('label_encoder.pkl')  # LabelEncoder pré-entraîné
    
#     # Vérifier que le LabelEncoder est bien "fitted"
#     if not hasattr(label_encoder, "classes_"):
#         raise ValueError("LabelEncoder n'est pas correctement entraîné.")
    
#     # Charger le modèle SpaCy
#     nlp = spacy.load("fr_core_news_sm")  # Modèle SpaCy pour le français
    
# except Exception as e:
#     raise RuntimeError(f"Erreur lors du chargement des modèles : {e}")

# # Pré-traitement du texte
# def preprocess_text(text):
#     try:
#         doc = nlp(text)
#         tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
#         return ' '.join(tokens)
#     except Exception as e:
#         raise ValueError(f"Erreur lors du prétraitement du texte : {e}")

# # Transformer un texte en vecteur avec Word2Vec
# def text_to_vector(text):
#     try:
#         tokens = preprocess_text(text).split()
#         vectors = [vectorizer.wv[token] for token in tokens if token in vectorizer.wv]
        
#         if not vectors:
#             raise ValueError("Aucun mot du texte n'est dans le vocabulaire Word2Vec.")
        
#         return np.mean(vectors, axis=0)
#     except Exception as e:
#         raise ValueError(f"Erreur lors de la vectorisation du texte : {e}")

# # Classe pour la requête d'entrée
# class ReadmeRequest(BaseModel):
#     readme: str

# # Point d'entrée pour la prédiction
# @app.route("/predict/", methods=["POST"])
# def predict():
#     try:
#         data = request.get_json()
#         readme_request = ReadmeRequest(**data)
        
#         # Prétraiter et vectoriser le texte
#         text_vector = text_to_vector(readme_request.readme)
        
#         # Reshaper le vecteur pour être compatible avec le modèle
#         text_vector = text_vector.reshape(1, -1)  # Assurez-vous que le format d'entrée correspond à ce que le modèle attend
        
#         # Prédire avec le modèle
#         prediction = model.predict(text_vector)
#         predicted_language = label_encoder.inverse_transform(prediction)
        
#         return jsonify({"predicted_language": predicted_language[0]})
#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 400
#     except Exception as e:
#         return jsonify({"error": f"Erreur interne : {e}"}), 500


# Mock prediction
@app.route("/predict/", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        predicted_language = "javascript"
      
        content = {}
        content["input"] = data["readme"]
        content["prediction"] = predicted_language
        content["time"] = datetime.now().isoformat()
        
        collection.insert_one(content)

        return jsonify({"predicted_language": predicted_language})
    except Exception as e:
        return jsonify({"error": f"Erreur interne : {e}"}), 500


# User interface
@app.route("/")
def read_root():
    return send_from_directory(app.static_folder, 'index.html')


# Start server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

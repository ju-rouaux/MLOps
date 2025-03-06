from flask import Flask, request, jsonify, send_from_directory
import os
import sys
from datetime import datetime
from pymongo import MongoClient
from transformers import DistilBertTokenizer
from transformers import DistilBertModel
import mlflow
import mlflow.pyfunc
import numpy as np
import torch


MONGO_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017/")
MLFLOW_URI = os.getenv("MLFLOW_URI", "http://localhost:8090")


# Créer l'application Flask
app = Flask(__name__, static_folder='static')


# Connexion à MongoDB
try:
  # Establish connection
  client = MongoClient(MONGO_URI)

  # Test the connection
  db_list = client.list_database_names()
  db = client.get_database("dev")
  collection = db.get_collection("front_app_logs")
  print("Successfully connected to MongoDB")
  print("Databases:", db_list)

except Exception as e:
  print("Error connecting to MongoDB:", e)
  sys.exit(1)  # Exit the program if connection fails


# Charger le modèle de MLflow
mlflow.set_tracking_uri(MLFLOW_URI)
model = mlflow.pyfunc.load_model("models:/Aeugh@prod")


# Charger le tokenizer DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
bert_model = DistilBertModel.from_pretrained("distilbert-base-uncased")


# Mock prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        readme_text = data.get("readme", "")

        # Tokenization avec DistilBERT
        inputs = tokenizer(readme_text, padding='max_length', truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():  # Pas besoin de calculer les gradients
          outputs = bert_model(**inputs)

        # Extract the [CLS] token representation and convert it to a list
        sentence_embedding = outputs.last_hidden_state[:, 0, :]

        prediction = model.predict(sentence_embedding)

        # Traitez la prédiction et retournez la réponse
        predicted_language = prediction[0]  # Ajustez selon la sortie de votre modèle
      
        # Temporaire le temps de mapper les langages
        predicted_language = str(predicted_language)

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

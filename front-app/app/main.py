from flask import Flask, request, jsonify, send_from_directory
import os
import sys
from datetime import datetime
from pymongo import MongoClient
from transformers import DistilBertTokenizer
import mlflow
import mlflow.pyfunc
import numpy as np
import torch


MONGO_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017/")


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


# Charger le tokenizer DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

model_uri = "http://mlflow:8080/api/2.0/mlflow/models/get/Model_Pour_Api/versions/1"  # Exemple de modèle version 1
model = mlflow.pyfunc.load_model(model_uri)

# Mock prediction
@app.route("/predict/", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        readme_text = data.get("readme", "")

        # Tokenization avec DistilBERT
        tokens = tokenizer(readme_text, padding=True, truncation=True, return_tensors="pt")

        # Les tokens sont prêts à être passés à votre modèle
        # Assurez-vous que votre modèle peut accepter ces tensors (par exemple sous forme de tableau numpy)
        # Si le modèle prend directement des tenseurs PyTorch
        inputs = tokens['input_ids'].numpy()

        # Prédiction avec le modèle MLflow
        # Si vous avez besoin de passer des tenseurs PyTorch, vous pouvez faire `inputs = torch.tensor(inputs)`
        prediction = model.predict(inputs)

        # Traitez la prédiction et retournez la réponse
        predicted_language = prediction[0]  # Ajustez selon la sortie de votre modèle
       
      
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

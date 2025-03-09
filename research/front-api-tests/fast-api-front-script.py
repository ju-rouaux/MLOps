from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import joblib  # Pour charger le modèle de classification
import spacy
from sklearn.preprocessing import LabelEncoder
import numpy as np
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression

# Crée l'application FastAPI
app = FastAPI()

# Charger les modèles et outils nécessaires
try:
    model = joblib.load('logistic_regression_model.pkl')  # Modèle de classification
    vectorizer = Word2Vec.load('word2vec_model.bin')  # Modèle Word2Vec
    label_encoder = joblib.load('label_encoder.pkl')  # LabelEncoder pré-entraîné
    
    # Vérifier que le LabelEncoder est bien "fitted"
    if not hasattr(label_encoder, "classes_"):
        raise ValueError("LabelEncoder n'est pas correctement entraîné.")
    
    nlp = spacy.load("fr_core_news_sm")  # Modèle SpaCy pour le français
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement des modèles : {e}")

# Pré-traitement du texte
def preprocess_text(text):
    try:
        doc = nlp(text)
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(tokens)
    except Exception as e:
        raise ValueError(f"Erreur lors du prétraitement du texte : {e}")

# Transformer un texte en vecteur avec Word2Vec
def text_to_vector(text):
    try:
        tokens = preprocess_text(text).split()
        vectors = [vectorizer.wv[token] for token in tokens if token in vectorizer.wv]
        
        if not vectors:
            raise ValueError("Aucun mot du texte n'est dans le vocabulaire Word2Vec.")
        
        return np.mean(vectors, axis=0)
    except Exception as e:
        raise ValueError(f"Erreur lors de la vectorisation du texte : {e}")

# Classe pour la requête d'entrée
class ReadmeRequest(BaseModel):
    readme: str

# Point d'entrée pour la prédiction
@app.post("/predict/")
async def predict(request: ReadmeRequest):
    try:
        # Prétraiter et vectoriser le texte
        text_vector = text_to_vector(request.readme)
        
        # Prédire avec le modèle
        prediction = model.predict([text_vector])
        predicted_language = label_encoder.inverse_transform(prediction)
        
        return {"predicted_language": predicted_language[0]}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")

# Route pour tester l'API
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Language Prediction API"}

# Lancer le serveur FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

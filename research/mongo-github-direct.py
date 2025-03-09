import requests
import json
import os
from tqdm import tqdm
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Lire le token GitHub
with open('../keys/GIT_API_TOKEN.txt', 'r') as file:
    git_token = file.read().strip()

# Lire le mot de passe MongoDB
with open('../keys/MONGODB_PASSWORD.txt', 'r') as file:
    password = file.read().strip()

# Configuration MongoDB
uri = f"mongodb+srv://admin:{password}@clusterdev.k5hlx.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDev"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client.get_database("dev")
collection = database.get_collection("repositories")

# Configurer les headers pour l'API GitHub
headers = {'Authorization': 'token ' + git_token}

# Liste des langages courts
languages_short = [
    "Java"
]

# Fonctions de requête API GitHub
def request_repositories(language: str, page: str):
    """Requête pour obtenir les meilleurs dépôts d'un langage donné."""
    url = f'https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page=10&page={page}'
    return requests.get(url, headers=headers).json()

def request_user_and_repo(language: str, page: str):
    """Extraire les utilisateurs et noms des dépôts."""
    response = request_repositories(language=language, page=page)
    return list(map(lambda item: (item["owner"]["login"], item["name"]), response.get("items", [])))

def get_readme(user: str, repo: str):
    """Obtenir le contenu du fichier README.md d'un dépôt."""
    url = f'https://raw.githubusercontent.com/{user}/{repo}/master/README.md'
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

def get_languages(user: str, repo: str):
    """Obtenir les langages utilisés dans un dépôt."""
    url = f'https://api.github.com/repos/{user}/{repo}/languages'
    return requests.get(url, headers=headers).json()

def build_repo_object(user: str, repo: str):
    """Construire un objet représentant un dépôt."""
    content = {
        "user": user,
        "repo": repo,
        "languages": get_languages(user, repo),
    }
    if content["languages"]:
        content["mainLanguage"] = list(content["languages"].keys())[0]
    content["readme"] = get_readme(user, repo)
    return content

# Traitement principal
for language in languages_short:
    results = request_user_and_repo(language, 1)  # Page 1 seulement
    for user, repo in tqdm(results, desc=f"Processing {language} repositories", leave=False):
        try:
            # Construire l'objet de dépôt
            repo_object = build_repo_object(user, repo)
            # Insertion dans MongoDB
            collection.insert_one(repo_object)
            print(f"Inserted {user}/{repo} into MongoDB")
        except Exception as e:
            print(f"Failed to process {user}/{repo}: {e}")

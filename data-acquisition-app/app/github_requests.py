import requests

def request_repositories(language: str, page: str, headers: dict):
  response = requests.get(f'https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page=10&page={page}', headers=headers)
  if response.status_code != 200:
    raise Exception(f"Error requesting repositories: {response.status_code} - {response.text}")
  return response.json()

def request_user_and_repo(language: str, page: str, headers: dict):
  response = request_repositories(language=language, page=page, headers=headers)
  return list(map(lambda item: (item["owner"]["login"], item["name"]), response["items"]))
  
def get_readme(user: str, repo: str, headers: dict):
  # Try md
  response = requests.get(f'https://raw.githubusercontent.com/{user}/{repo}/master/README.md', headers=headers)
  if response.status_code != 200:
    # Try rst
    response = requests.get(f'https://raw.githubusercontent.com/{user}/{repo}/master/README.rst', headers=headers)
    if response.status_code != 200:
      raise Exception("README file not found")
  return response.text

def get_languages(user: str, repo:str, headers: dict):
  response = requests.get(f'https://api.github.com/repos/{user}/{repo}/languages', headers=headers)
  if response.status_code != 200:
    raise Exception(f"Error requesting repositories: {response.status_code} - {response.text}")
  return response.json()
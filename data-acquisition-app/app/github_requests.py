import requests
import time

def make_request(url: str, headers: dict):
  response = requests.get(url, headers=headers)
  if response.status_code == 403: # Retry after one minute
    print("Forbidden: You have reached the API rate limit. Waiting for 10 seconds.")
    time.sleep(10)
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
      raise Exception("Forbidden: You have reached the API rate limit.")
  elif response.status_code != 200:
    raise Exception(f"Error requesting URL: {response.status_code} - {response.text}")
  return response

def request_repositories(language: str, page: str, headers: dict):
  url = f'https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page=100&page={page}'
  response = make_request(url, headers)
  return response.json()

def request_user_and_repo(language: str, page: str, headers: dict):
  response = request_repositories(language=language, page=page, headers=headers)
  return list(map(lambda item: (item["owner"]["login"], item["name"]), response["items"]))
  
def get_readme(user: str, repo: str, headers: dict):
  for branch in ['master', 'main']:
    for ext in ['.md', '.rst', '.txt', '']:
      url = f'https://raw.githubusercontent.com/{user}/{repo}/{branch}/README{ext}'
      try:
        response = make_request(url, headers)
        return response.text
      except Exception as e:
        if "Forbidden" in str(e):
          raise e
  raise Exception("README file not found")

def get_languages(user: str, repo:str, headers: dict):
  url = f'https://api.github.com/repos/{user}/{repo}/languages'
  response = make_request(url, headers)
  return response.json()
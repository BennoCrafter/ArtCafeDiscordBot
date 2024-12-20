import requests

base_url: str = "https://nekos.best/api/v2/%s?amount=%d"
prompt: str = "hug"

resp = requests.get(base_url % (prompt, 100))
data = resp.json()
print(data["results"])
print(data["results"][0]["url"])

import json
import requests

api_token = 'your_api_token'
api_url_base = 'https://fiar3d.herokuapp.com/api/game/'

api_url = api_url_base+ input("game? ")
headers = {'Content-Type': 'application/json'}



response = requests.get(api_url, headers=headers)


if response.status_code == 200:
    print(json.loads(response.content.decode('utf-8')))
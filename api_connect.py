from Game import *
import json
import requests

api_url_base = 'https://fiar3d.herokuapp.com/api/'

def get_game(id):
    api_url = api_url_base + "game/" + str(id)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(api_url, headers=headers)
    res = json.loads(response.content.decode('utf-8'))
    player_x_id = res["ai_a"]
    player_y_id = res["ai_b"]
    game = Game()
    game.player = 1 if res["to_move"] == player_x_id else -1
    game.moves = [x["position"] for x in res["moves"]]
    game.board = res["board"]
    game.board = [[[[player_y_id,None,player_x_id].index(z)-1 for z in y] for y in x] for x in game.board]
    return game

def get_ai(id):
    api_url = api_url_base + "ai/" + str(id)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(api_url, headers=headers)
    res = json.loads(response.content.decode('utf-8'))
    if "error_message" in res:
        print(res["error_message"])
        return None
    return res

def new_ai(name):
    api_url = api_url_base + "ai"
    data = {"name" : name}
    response = requests.post(api_url, json=data)
    res = json.loads(response.content.decode('utf-8'))
    if "error_message" in res:
        print(res["error_message"])
        return None
    return res

def new_game(ai_id,secret_key):
    api_url = api_url_base + "game"
    data = {ai_id:ai_id,secret_key:secret_key}
    response = requests.post(api_url, json=data)
    res = json.loads(response.content.decode('utf-8'))
    if "error_message" in res:
        print(res["error_message"])
        return None
    return res

if __name__ == '__main__':
    ai = new_ai("p3injdhfaz33tjdj")
    print(new_game(ai["id"],ai["key"]))
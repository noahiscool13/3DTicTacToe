from Game import *
import json
import requests
from time import sleep

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
        raise UserWarning(res["error_message"])
    return res

def new_ai(name):
    api_url = api_url_base + "ai"
    data = {"name" : name}
    response = requests.post(api_url, json=data)
    res = json.loads(response.content.decode('utf-8'))
    if "error_message" in res:
        raise UserWarning(res["error_message"])
    return res

def new_game(ai_id, ai_key):
    api_url = api_url_base + "game"
    data = {"ai_id":ai_id, "ai_key":ai_key}
    response = requests.post(api_url, json=data)
    res = json.loads(response.content.decode('utf-8'))
    if "error_message" in res:
        raise UserWarning(res["error_message"])
    return res

def send_move(game,ai_id,ai_key,position):
    api_url = api_url_base + "game/" + str(game) + "/moves"
    data = {"ai_id":ai_id, "ai_key":ai_key,"position":position}
    response = requests.post(api_url, json=data)
    res = json.loads(response.content.decode('utf-8'))
    if "error_message" in res:
        raise UserWarning(res["error_message"])
    return res

if __name__ == '__main__':
    from trained_ai3 import AI as AI1
    from trained_ai3 import AI as AI2
    ai1 = new_ai("niceyyyyyyyyy1")
    ai2 = new_ai("niceyyyyyyyyy2")
    game_base = new_game(ai1["id"],ai1["key"])
    while not (game_base["ai_b"] is None):
        game_base = new_game(ai1["id"], ai1["key"])
    game_base = new_game(ai2["id"],ai2["key"])
    game = get_game(game_base["id"])
    game.print_board()
    while not game.check_board():
        if game.player == 1:
            send_move(game_base["id"], ai1["id"], ai1["key"], AI1(game)-1)
        else:
            send_move(game_base["id"], ai2["id"], ai2["key"], AI2(game)-1)
        sleep(0.3)
        game = get_game(game_base["id"])

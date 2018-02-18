from time import time
from copy import deepcopy
from random_AI import AI as random_ai
from random import choice

def safe_div(x,y):
    if y == 0:
        return 10**99
    return x / y

def AI(game):
    """Montecarlo tree search v1"""
    t = time()
    nxt_games = []
    ratings = []
    count_g = 0
    count_b = 0
    for x in game.allowed_moves():
        game_child = deepcopy(game)
        game_child.move(x)
        nxt_games.append(game_child)
        ratings.append([0,0])
    while time()-t < game.time_limit:
        for x in range(len(nxt_games)):
            count_g+=1
            dummy_game = deepcopy(nxt_games[x])
            while not dummy_game.check_board():
                count_b+=1
                dummy_game.move(random_ai(dummy_game))
            if dummy_game.check_board() == game.player:
                ratings[x][0] += 1
            elif dummy_game.check_board() == -game.player:
                ratings[x][1] += 1
    print(count_g, "games simulated and", count_b, "bord positions seen.")
    ratings = [safe_div(a[0],a[1]) for a in ratings]
    good_moves = [game.allowed_moves()[x] for x in range(len(game.allowed_moves())) if ratings[x] == max(ratings)]
    return choice(good_moves)
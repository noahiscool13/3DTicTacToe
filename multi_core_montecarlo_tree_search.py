from time import time
from copy import deepcopy
from random_AI import AI as random_ai
from random import choice
from multiprocessing import Pool

def safe_div(x,y):
    if y == 0:
        return 10**99
    return x / y

def play_random(game):
    out = [0,0]
    for x in range(100):
        g = deepcopy(game)
        while not g.check_board():
            g.move(random_ai(g))
        if g.check_board() == game.player:
            out[1]+=1
        elif g.check_board() == -game.player:
            out[0]+=1
    return out

def AI(game):
    """Montecarlo tree search Multi core v1"""
    t = time()
    nxt_games = []
    ratings = []
    count_g = 0
    for x in game.allowed_moves():
        game_child = deepcopy(game)
        game_child.move(x)
        nxt_games.append(game_child)
        ratings.append([0,0])
    while time()-t < game.time_limit:
        count_g +=len(nxt_games)*100
        pool = Pool()
        batch = pool.map(play_random,nxt_games)
        pool.close()
        pool.join()
        for n,x in enumerate(batch):
            ratings[n] = [ratings[n][0]+x[0],ratings[n][0]+x[1]]
    print(count_g, "games simulated",ratings)
    ratings = [safe_div(a[0],a[1]) for a in ratings]
    good_moves = [game.allowed_moves()[x] for x in range(len(game.allowed_moves())) if ratings[x] == max(ratings)]
    return choice(good_moves)
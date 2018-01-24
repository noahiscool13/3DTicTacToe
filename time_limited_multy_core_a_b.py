from copy import deepcopy
from random import choice, sample
from multiprocessing import Pool
from time import time

def tread(g):
    return alphabeta(g[0], g[2], -99999, 99999, g[1].player,g[3])

def score(game,player):
    if game.check_board() == player:
        return 1
    if game.check_board():
        return -1
    return 0

def  alphabeta(game, depth, a, b, player,t_stop):
    if depth == 0 or game.check_board() or time() > t_stop:
        return score(game,player)
    if game.player == player:
        best = -99999
        for x in sample(game.allowed_moves(),len(game.allowed_moves())):
            game_child = deepcopy(game)
            game_child.move(x)
            best = max(best, alphabeta(game_child, depth - 1,a,b, player,t_stop))
            a = max(a,best)
            if b <= a:
                break
        return best
    best = 99999
    for x in sample(game.allowed_moves(),len(game.allowed_moves())):
        game_child = deepcopy(game)
        game_child.move(x)
        best = min(best, alphabeta(game_child, depth - 1,a,b, player,t_stop))
        b = min(b,best)
        if b <= a:
            break
    return best

def AI(game,t_max):
    """Time limited multi core alpha beta AI"""
    t_end = time() + t_max
    depth = 1
    nxt_scores = []
    pool = Pool(6)
    while time() < t_end:
        nxt_games = []
        for x in game.allowed_moves():
            game_child = deepcopy(game)
            game_child.move(x)
            nxt_games.append((game_child,game,depth,t_end))
        nxt_scores.append(pool.map(tread, nxt_games))
        depth+=1
    good_moves = []
    print("depth was "+ str(depth))
    for x in range(len(game.allowed_moves())):
        if nxt_scores[-2][x] == max(nxt_scores[-2]):
            good_moves.append(game.allowed_moves()[x])
    pool.close()
    return choice(good_moves)
from copy import deepcopy
from random import choice

def score(game,player):
    if game.check_board() == player:
        return 1
    if game.check_board():
        return -1
    return 0

def  alphabeta(game, depth, a, b, player):
    if depth == 0 or game.check_board():
        return score(game,player)
    if game.player == player:
        best = -99999
        for x in game.allowed_moves():
            game_child = deepcopy(game)
            game_child.move(x)
            best = max(best, alphabeta(game_child, depth - 1,a,b, player) - depth / 100)
            a = max(a,best)
            if b <= a:
                break
        return best
    best = 99999
    for x in game.allowed_moves():
        game_child = deepcopy(game)
        game_child.move(x)
        best = min(best, alphabeta(game_child, depth - 1,a,b, player))
        b = min(b,best)
        if b <= a:
            break
    return best

def AI(game):
    """Basic alpha beta AI"""
    nxt_games = []
    for x in game.allowed_moves():
        game_child = deepcopy(game)
        game_child.move(x)
        nxt_games.append(game_child)
    nxt_scores = [alphabeta(g, 5,-99999,99999, game.player) for g in nxt_games]
    good_moves = [game.allowed_moves()[x] for x in range(len(game.allowed_moves())) if
                  nxt_scores[x] == max(nxt_scores)]
    return choice(good_moves)
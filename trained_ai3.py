from copy import deepcopy
from random import choice, sample
import numpy as np
import tensorflow as tf
import os

flatten = lambda l: [item for sublist in l for item in sublist]

tf.reset_default_graph()

hidden_l1 = {"w": tf.Variable(tf.random_normal([65, 100])), "b": tf.Variable(tf.random_normal([100]))}
hidden_l2 = {"w": tf.Variable(tf.random_normal([100, 100])), "b": tf.Variable(tf.random_normal([100]))}
output_l = {"w": tf.Variable(tf.random_normal([100, 1])), "b": tf.Variable(tf.random_normal([1]))}

def net(data):

    data = tf.cast(data,tf.float32)
    l1 = tf.nn.sigmoid(tf.matmul(data, hidden_l1["w"]) + hidden_l1["b"])
    l2 = tf.nn.sigmoid(tf.matmul(l1, hidden_l2["w"]) + hidden_l2["b"])
    out = tf.nn.sigmoid(tf.matmul(l2, output_l["w"]) + output_l["b"])

    return out

saver = tf.train.Saver()


def score(game,player):
    if game.check_board() == player:
        return 1
    if game.check_board():
        return -1
    q = flatten(flatten(game.board))+[game.player]
    # q = [[-1 if x == "x" else x for x in n] for n in q]
    # q = [[1 if x == "y" else x for x in n] for n in q]
    # q = [[0 if x == "0" else x for x in n] for n in q]
    p = net(np.array([q],dtype=float)).eval()
    if player == "1":
        return 1-p[0][0]
    else:
        return p[0][0]

def  alphabeta(game, depth, a, b, player):
    if game.check_board():
        return score(game, player)
    if depth == 0:
        return score(game, player)

    if game.player == player:
        best = -99999
        for x in sample(game.allowed_moves(),len(game.allowed_moves())):
            game_child = deepcopy(game)
            game_child.move(x)
            ab = alphabeta(game_child, depth - 1, a, b, player)
            best = max(best, ab)
            if ab == 1:
                done = 0
            a = max(a,best)
            if b <= a:
                break
        return best
    best = 99999
    for x in sample(game.allowed_moves(),len(game.allowed_moves())):
        game_child = deepcopy(game)
        game_child.move(x)
        ab = alphabeta(game_child, depth - 1,a,b, player)
        best = min(best, ab)
        if ab == 1:
            done = 0
        b = min(b,best)
        if b <= a:
            break
    return best

def AI(game):
    """Neural net trained AI"""
    with tf.Session() as sess:
        saver.restore(sess, os.path.join(os.getcwd(),"trained_models/NN3.ckpt"))
        nxt_games = []
        for x in game.allowed_moves():
            game_child = deepcopy(game)
            game_child.move(x)
            nxt_games.append(game_child)
        nxt_scores = [alphabeta(g, 1,-99999, 99999, game.player) for g in nxt_games]
        print(nxt_scores)
        good_moves = [game.allowed_moves()[x] for x in range(len(game.allowed_moves())) if
                      nxt_scores[x] == max(nxt_scores)]
        return choice(good_moves)
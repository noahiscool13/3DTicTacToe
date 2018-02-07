from copy import deepcopy
from random import choice, sample
from time import time
import tensorflow as tf
import os

flatten = lambda l: [item for sublist in l for item in sublist]

tf.reset_default_graph()

hidden_l1 = {"w": tf.Variable(tf.random_normal([64, 500])), "b": tf.Variable(tf.random_normal([500]))}
hidden_l2 = {"w": tf.Variable(tf.random_normal([500, 500])), "b": tf.Variable(tf.random_normal([500]))}
hidden_l3 = {"w": tf.Variable(tf.random_normal([500, 500])), "b": tf.Variable(tf.random_normal([500]))}
hidden_l4 = {"w": tf.Variable(tf.random_normal([500, 100])), "b": tf.Variable(tf.random_normal([100]))}
output_l = {"w": tf.Variable(tf.random_normal([100, 1])), "b": tf.Variable(tf.random_normal([1]))}

def net(data):

    data = tf.cast(data,tf.float32)
    l1 = tf.nn.sigmoid(tf.matmul(data, hidden_l1["w"]) + hidden_l1["b"])
    l2 = tf.nn.sigmoid(tf.matmul(l1, hidden_l2["w"]) + hidden_l2["b"])
    l3 = tf.nn.sigmoid(tf.matmul(l2, hidden_l3["w"]) + hidden_l3["b"])
    l4 = tf.nn.sigmoid(tf.matmul(l3, hidden_l4["w"]) + hidden_l4["b"])
    out = tf.nn.sigmoid(tf.matmul(l4, output_l["w"]) + output_l["b"])

    return out

saver = tf.train.Saver()


def score(game,player):
    if game.check_board() == player:
        return 1
    if game.check_board():
        return -1
    q = flatten(flatten(game.board))
    q = [[-1 if x == "x" else x for x in n] for n in q]
    q = [[1 if x == "y" else x for x in n] for n in q]
    q = [[0 if x == "0" else x for x in n] for n in q]
    p = net([flatten(q)]).eval()
    if player == "x":
        return 1-p[0][0]
    else:
        return p[0][0]

def  alphabeta(game, depth, a, b, player,t_stop):
    if time() > t_stop:
        return (score(game,player),0)
    if game.check_board():
        return (score(game, player), 1)
    if depth == 0:
        return (score(game, player), 0)

    done = 1

    if game.player == player:
        best = -99999
        for x in sample(game.allowed_moves(),len(game.allowed_moves())):
            game_child = deepcopy(game)
            game_child.move(x)
            ab = alphabeta(game_child, depth - 1, a, b, player, t_stop)
            best = max(best, ab[0])
            if ab[1] == 1:
                done = 0
            a = max(a,best)
            if b <= a:
                break
        return best,done
    best = 99999
    for x in sample(game.allowed_moves(),len(game.allowed_moves())):
        game_child = deepcopy(game)
        game_child.move(x)
        ab = alphabeta(game_child, depth - 1,a,b, player,t_stop)
        best = min(best, ab[0])
        if ab[1] == 1:
            done = 0
        b = min(b,best)
        if b <= a:
            break
    return best,done

def AI(game):
    """Neural net trained AI"""
    with tf.Session() as sess:
        completed = 0
        saver.restore(sess, os.path.join(os.getcwd(),"trained_models/NN1.ckpt"))
        t_end = time() + game.time_limit
        depth = 0
        nxt_scores = []
        while time() < t_end:
            nxt_games = []
            for x in game.allowed_moves():
                game_child = deepcopy(game)
                game_child.move(x)
                nxt_games.append(game_child)
            nxt_scores.append([alphabeta(g, depth,-99999,99999, game.player,t_end) for g in nxt_games])
            if 0 not in [a[1] for a in nxt_scores[0]]:
                print("completed search.")
                completed = 1
                break
            depth+=1
        good_moves = []
        print("depth was " + str(depth))
        nxt_scores = [[y[0] for y in x] for x in nxt_scores]
        print(nxt_scores)
        if len(nxt_scores) > 0:
            if completed:
                print("moral:",max(nxt_scores[-1]))
                for x in range(len(game.allowed_moves())):
                    if nxt_scores[-1][x] == max(nxt_scores[-1]):
                        good_moves.append(game.allowed_moves()[x])
            else:
                if len(nxt_scores) > 1:
                    print("moral:", max(nxt_scores[-2]))
                    for x in range(len(game.allowed_moves())):
                        if nxt_scores[-2][x] == max(nxt_scores[-2]):
                            good_moves.append(game.allowed_moves()[x])
                else:
                    print("moral:", max(nxt_scores[-1]))
                    for x in range(len(game.allowed_moves())):
                        if nxt_scores[-1][x] == max(nxt_scores[-1]):
                            good_moves.append(game.allowed_moves()[x])
            return choice(good_moves)
        return choice(game.allowed_moves())

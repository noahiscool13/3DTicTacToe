from Game import *
from copy import deepcopy
from time import *
from multiprocessing import Pool
from random import randint
import pickle
from random_AI import AI as random_move
from basic_alpha_beta import AI as AI1
from basic_alpha_beta import AI as AI2

time_max = 1

x_wins = set()
y_wins = set()


def runs(x):
    states = []
    game = Game()
    game.time_limit = 1

    bad_start = randint(0, 64)
    while (not game.check_board()) and bad_start:
        game.move(random_move(game))

    if game.check_board():
        if len(game.moves)>10:
            for _ in range(5):
                game.undo_move()

    while not game.check_board():
        if game.player == "x":
            game.move(AI1(deepcopy(game)))
        else:
            game.move(AI2(deepcopy(game)))
        states.append(tuple([tuple([tuple(z) for z in l]) for l in game.board]))
    if game.check_board() == "x":
        return ("x", states)
    if game.check_board() == "y":
        return ("y", states)
    return ("tie",[])

t = time()
if __name__ == '__main__':

    try:
        x_wins = pickle.load(open("x_wins_clean.p", "rb"))
        y_wins = pickle.load(open("y_wins_clean.p", "rb"))
    except:
        print("No file found")

    n = 0

    while True:
        pool = Pool()

        games = pool.map(runs, list(range(500)))

        pool.close()
        pool.join()

        print(len(games))

        for x in games:
            try:
                if x[0] == "x":
                    for y in x[1]:
                        x_wins.add(y)
                elif x[0] == "y":
                    for y in x[1]:
                        y_wins.add(y)
            except:
                print("broke",x)

        print("game: ", n, "done")
        print(len(x_wins), len(y_wins))
        pickle.dump(x_wins, open("x_wins_clean.p", "wb"))
        pickle.dump(y_wins, open("y_wins_clean.p", "wb"))

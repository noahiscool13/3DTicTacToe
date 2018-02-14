from Game import *
from copy import deepcopy
from time import *
from multiprocessing import Pool
from random import randint
import pickle
from random_AI import AI as random_move
from basic_alpha_beta import AI as AI1
from basic_alpha_beta import AI as AI2
from tqdm import tqdm

flatten = lambda l: [item for sublist in l for item in sublist]

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
        if len(game.moves)>5:
            for _ in range(5):
                game.undo_move()

    while not game.check_board():
        if game.player == 1:
            game.move(AI1(deepcopy(game)))
        else:
            game.move(AI2(deepcopy(game)))
            states.append(tuple(flatten([tuple(flatten([tuple(z) for z in l])) for l in game.board]) + [game.player]))
    states.append(tuple(flatten([tuple(flatten([tuple(z) for z in l])) for l in game.board])+[game.player]))
    if game.check_board() == 1:
        return (1, states)
    if game.check_board() == -1:
        return (-1, states)
    return ("tie",[])

t = time()
if __name__ == '__main__':

    try:
        x_wins = pickle.load(open("x_wins_clean.p", "rb"))
        y_wins = pickle.load(open("y_wins_clean.p", "rb"))
    except:
        x_wins = set()
        y_wins = set()
        print("No file found")

    n = 0

    while True:
        pool = Pool(4)
        batch = 500
        games = list(tqdm(pool.imap(runs, list(range(batch))),total=batch,ncols=100))

        pool.close()
        pool.join()

        print(len(games))
        for x in games:
            try:
                if x[0] == 1:
                    for y in x[1]:
                        x_wins.add(y)
                elif x[0] == -1:
                    for y in x[1]:
                        y_wins.add(y)
            except:
                print("broke",x)

        print("game: ", n, "done")
        print(len(x_wins), len(y_wins))
        pickle.dump(x_wins, open("x_wins_clean.p", "wb"))
        pickle.dump(y_wins, open("y_wins_clean.p", "wb"))

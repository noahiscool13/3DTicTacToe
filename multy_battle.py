from Capturing import Capturing
from Game import *
from random import randint,choice
from copy import deepcopy


ais = ["time_limited_minimax","time_limited_alpha_beta","time_limited_multy_core_a_b"]

time_max = 0.5

k = 24

for x in range(len(ais)):
    exec("from " + ais[x] + " import AI as AI" + str(x))

elo = {x: 0 for x in range(len(ais))}

if __name__ == '__main__':
    for x in range(10):
        ai_1 = randint(0,len(ais)-1)
        opponents = list(range(len(ais)))
        opponents.remove(ai_1)
        ai_2 = choice(opponents)
        print("game",x)
        print(ais[ai_1],"vs",ais[ai_2])
        game = Game()
        game.time_limit = time_max
        while not game.check_board():
            if game.player == "x":
                with Capturing() as output:
                    exec("game.move(AI" + str(ai_1) + "(deepcopy(game)))")
            else:
                with Capturing() as output:
                    exec("game.move(AI" + str(ai_2) + "(deepcopy(game)))")

        R1 = 10**(elo[ai_1]/400)
        R2 = 10**(elo[ai_2]/400)

        e1 = R1 / (R1 + R2)
        e2 = R2 / (R2 + R1)

        if game.check_board() == "x":
            print(ais[ai_1],"won")
            s1 = 1
            s2 = 0
        if game.check_board() == "y":
            print(ais[ai_2],"won")
            s1 = 0
            s2 = 1

        elo[ai_1] = elo[ai_1] + k * (s1 - e1)
        elo[ai_2] = elo[ai_2] + k * (s2 - e2)

    print(elo)
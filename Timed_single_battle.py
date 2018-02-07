from Game import *
from copy import deepcopy
from time import *
import inspect
import os
from Capturing import *
from random_AI import AI as AI1
from random_AI import AI as AI2

display = 1
capture = 0
time_max = 300

p1_time = []
p2_time = []

p1_comment = {}
p2_comment = {}

move = 1



t = time()
if __name__ == '__main__':
    game = Game()
    game.time_limit = time_max
    while not game.check_board():
        if game.player == "x":
            t = time()
            if capture:
                with Capturing() as output:
                    game.move(AI1(deepcopy(game)))
            else:
                game.move(AI1(deepcopy(game)))
            p1_time.append(round(time() - t, 3))
            if capture:
                if len(output)>0:
                    p1_comment[move] = output
        else:
            t = time()
            if capture:
                with Capturing() as output:
                    game.move(AI2(deepcopy(game)))
            else:
                game.move(AI2(deepcopy(game)))
            p2_time.append(round(time() - t, 3))
            if capture:
                if len(output)>0:
                    p2_comment[move] = output
        move += 1
        if display:
            game.print_board()
            print("Last move was:", game.moves[-1])
    game.print_board()
    print(game.check_board())
    print(game.moves)
    print(len(game.moves))

    post_mortem = open(os.path.join("post_morta",str(round(time()))),"w")
    post_mortem.write("Player x: " + str(inspect.getdoc(AI1)) + "\n")
    post_mortem.write("Player y: " + str(inspect.getdoc(AI2)) + "\n")
    post_mortem.write("Moves: " + str(game.moves)+"\n")
    post_mortem.write("Winner: " + str(game.check_board())+"\n")
    post_mortem.write("Times AI1: " + str(sum(p1_time)) + " " + str(p1_time)+"\n")
    post_mortem.write("Times AI2: " + str(sum(p2_time)) + " " + str(p2_time)+"\n")
    post_mortem.write("End position " + str(game.board)+"\n")
    post_mortem.write("Player x comments: " + str(p1_comment) + "\n")
    post_mortem.write("Player y comments: " + str(p2_comment) + "\n")
    post_mortem.close()
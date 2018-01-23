from Game import *
from copy import deepcopy
from human_inteligence import AI as AI1
from basic_alpha_beta import AI as AI2

game = Game()

while not game.check_board():
    if game.player == "x":
        game.move(AI1(deepcopy(game)))
    else:
        game.move(AI2(deepcopy(game)))
game.print_board()
print(game.check_board())

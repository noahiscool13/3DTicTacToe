from Game import *
from copy import deepcopy
from multy_core_a_b import AI as AI1
from human_inteligence import AI as AI2

display = 1

if __name__ == '__main__':
    game = Game()
    while not game.check_board():
        if game.player == "x":
            game.move(AI1(deepcopy(game)))
        else:
            game.move(AI2(deepcopy(game)))
        if display:
            game.print_board()
            print("Last move was:", game.moves[-1])
    game.print_board()
    print(game.check_board())
    print(game.moves)
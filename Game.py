import numpy as np
from math import *

class Game:
    def __init__(self):
        self.board = []
        self.player = "x"

        for x in range(4):
            t = []
            for y in range(4):
                t.append(['0', '0', '0', '0'])
            self.board.append(t)


    def print_board(self):
        for x in self.board:
            print(np.array(x))
            print()


    def allowed_moves(self):
        n = 1
        allowed = []
        for x in self.board[3]:
            for y in x:
                if y == '0':
                    allowed.append(n)
                n+=1
        return allowed

    def move(self,place):
        if place in self.allowed_moves():
            x = 0
            while 1:
                if self.board[x][(place-1)%4][floor((place-1)/4)] == '0':
                    self.board[x][(place-1) % 4][floor((place-1) / 4)] = self.player
                    if self.player == "x":
                        self.player = "y"
                    else:
                        self.player = "x"
                    break
                else:
                    x+=1

    def check_board(self):
        for layer in self.board:
            for row in layer:
                if len([1 for x in row if x == "x"]) == 4:
                    return "x"
                if len([1 for x in row if x == "y"]) == 4:
                    return "y"
            for coll in range(4):
                if len([1 for x in range(4) if layer[x][coll] == "x"]) == 4:
                    return "x"
                if len([1 for x in range(4) if layer[x][coll] == "y"]) == 4:
                    return "y"
            if len([1 for x in range(4) if layer[x][x] == "x"]) == 4:
                return "x"
            if len([1 for x in range(4) if layer[x][x] == "y"]) == 4:
                return "y"
            if len([1 for x in range(4) if layer[x][3-x] == "x"]) == 4:
                return "x"
            if len([1 for x in range(4) if layer[x][3-x] == "y"]) == 4:
                return "y"

        for row in range(4):
            for coll in range(4):
                if len([1 for layer in range(4) if self.board[layer][row][coll] == "x"]) == 4:
                    return "x"
                if len([1 for layer in range(4) if self.board[layer][row][coll] == "y"]) == 4:
                    return "y"
            if len([1 for x in range(4) if self.board[x][row][x] == "x"]) == 4:
                return "x"
            if len([1 for x in range(4) if self.board[x][row][x] == "y"]) == 4:
                return "y"
            if len([1 for x in range(4) if self.board[x][row][3-x] == "x"]) == 4:
                return "x"
            if len([1 for x in range(4) if self.board[x][row][3-x] == "y"]) == 4:
                return "y"

            if len([1 for x in range(4) if self.board[x][x][row] == "x"]) == 4:
                return "x"
            if len([1 for x in range(4) if self.board[x][x][row] == "y"]) == 4:
                return "y"
            if len([1 for x in range(4) if self.board[x][3-x][row] == "x"]) == 4:
                return "x"
            if len([1 for x in range(4) if self.board[x][3-x][row] == "y"]) == 4:
                return "y"


game = Game()

while not game.check_board():
    game.print_board()
    print(game.check_board())
    print(game.allowed_moves())
    game.move(int(input("mov? ")))


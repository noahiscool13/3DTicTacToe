import numpy as np
from math import *

class Game:
    def __init__(self):
        self.board = []
        self.player = "x"
        self.moves = []

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
        for x in range(4):
            for y in range(4):
                if self.board[3][y][x] == '0':
                    allowed.append(x*4+y+1)
                n+=1
        return allowed

    def move(self,place):
        if place in self.allowed_moves():
            self.moves.append(place)
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

    def undo_move(self):
        x = 3
        while 1:
            if self.board[x][(self.moves[-1]-1)%4][floor((self.moves[-1]-1)/4)] == '0':
                self.board[x][(self.moves[-1]-1) % 4][floor((self.moves[-1]-1) / 4)] = self.player
                if self.player == "x":
                    self.player = "y"
                else:
                    self.player = "x"
                break
            else:
                x-=1
        self.moves.pop()

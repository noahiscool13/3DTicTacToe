from Game import *
from copy import deepcopy
from time import *
import datetime
from io import StringIO
import sys
import pickle
from time_limited_multy_core_a_b import AI as AI1
from time_limited_multy_core_a_b import AI as AI2

time_max = 1

x_wins = []
y_wins = []

class Capturing(list):

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

t = time()
if __name__ == '__main__':

    n = 0

    while datetime.datetime.now().hour != 14:
        n+=1

        p1_time = []
        p2_time = []

        p1_comment = {}
        p2_comment = {}

        move = 1

        states = []

        game = Game()
        while not game.check_board():
            if game.player == "x":
                t = time()
                with Capturing() as output:
                    game.move(AI1(deepcopy(game),time_max))
                p1_time.append(round(time() - t, 3))
                if len(output)>0:
                    p1_comment[move] = output
            else:
                t = time()
                with Capturing() as output:
                    game.move(AI2(deepcopy(game),time_max))
                p2_time.append(round(time() - t, 3))
                if len(output)>0:
                    p2_comment[move] = output
            states.append(game.board)
            move += 1
        if game.check_board() == "x":
            x_wins.append(states)
        if game.check_board() == "y":
            y_wins.append(states)
        print("game: ",n,"done")

        pickle.dump(x_wins,open("x_wins.p", "wb"))
        pickle.dump(y_wins,open("y_wins.p", "wb"))

from random import choice
def AI(game):
    """Random AI"""
    return choice(game.allowed_moves())
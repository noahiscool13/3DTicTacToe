def AI(game):
    game.print_board()
    print("you are: ", game.player)
    try:
        print("last move by opponent was: ", game.moves[-1])
    except:
        print("no moves yet")
    return int(input("move (" + str(game.allowed_moves()) + "): "))
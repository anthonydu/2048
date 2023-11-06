from GameOf2048 import GameOf2048
import numpy as np


if __name__ == "__main__":
    game = GameOf2048()

    print("Welcome to 2048!")
    game.place_new_number()
    while True:
        print(game.board)
        key = input()
        if key == "q":
            break
        before = game.board.copy()
        game.move(key)
        if not np.all(before == game.board):
            game.place_new_number()
            if 0 not in game.board:
                print(game.board)
                print("Game over!")
                break

from GameOf2048 import Directions, GameOf2048
import numpy as np


if __name__ == "__main__":
    game = GameOf2048()

    print("Welcome to 2048!")
    while True:
        print(game.board)
        key = input()
        if key == "q":
            break
        before = game.board.copy()
        if key in iter(Directions):
            game.move(key)
        if not np.all(before == game.board):
            game.place_new_number()
            if game.game_over():
                print(game.board)
                print("Game over!")
                break

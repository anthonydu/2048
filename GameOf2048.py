import numpy as np
from random import random, randrange


class GameOf2048:
    DIM = 4

    def __init__(self):
        self.board = np.array([[0 for _ in range(self.DIM)]] * self.DIM)

    def move_arr(self, arr):
        result = []
        prev = None
        for el in arr:
            if el != 0:
                if result and el == prev:
                    result[-1] *= 2
                    prev = None
                else:
                    result.append(el)
                    prev = el
        for _ in range(len(arr) - len(result)):
            result.append(0)
        return result

    def move(self, key):
        for i in range(self.DIM):
            match key:
                case "a":
                    self.board[i, :] = self.move_arr(self.board[i, :])
                case "d":
                    self.board[i, :] = self.move_arr(self.board[i, :][::-1])[::-1]
                case "w":
                    self.board[:, i] = self.move_arr(self.board[:, i])
                case "s":
                    self.board[:, i] = self.move_arr(self.board[:, i][::-1])[::-1]

    def place_new_number(self):
        empties = []
        for i in range(self.DIM):
            for j in range(self.DIM):
                if self.board[i, j] == 0:
                    empties.append((i, j))

        space = empties[randrange(len(empties))]
        value = 2 if random() < 0.9 else 4
        self.board[space] = value

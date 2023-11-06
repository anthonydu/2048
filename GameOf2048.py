import numpy as np
from random import random, randrange
from copy import deepcopy
from enum import Enum


class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class GameOf2048:
    DIM = 4

    def __init__(self):
        self.score = 0
        self.board = np.array([[0 for _ in range(self.DIM)]] * self.DIM)
        self.place_new_number()

    def move_arr(self, arr):
        result = []
        prev = None
        for el in arr:
            if el != 0:
                if result and el == prev:
                    result[-1] *= 2
                    self.score += result[-1]
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
                case Directions.LEFT:
                    self.board[i, :] = self.move_arr(self.board[i, :])
                case Directions.RIGHT:
                    self.board[i, :] = self.move_arr(self.board[i, :][::-1])[::-1]
                case Directions.UP:
                    self.board[:, i] = self.move_arr(self.board[:, i])
                case Directions.DOWN:
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

    def game_over(self):
        sum = 0
        game = deepcopy(self)
        game.move("w")
        if 0 not in game.board:
            sum += 1
        game = deepcopy(self)
        game.move("a")
        if 0 not in game.board:
            sum += 1
        game = deepcopy(self)
        game.move("s")
        if 0 not in game.board:
            sum += 1
        game = deepcopy(self)
        game.move("d")
        if 0 not in game.board:
            sum += 1
        return sum == 4

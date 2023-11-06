from copy import deepcopy
import math
from GameOf2048 import Directions, GameOf2048
import pygame
import numpy as np


# reset
# reward
# play(action)
# game_iteration
# game_over
class GameOf2048AI:
    WIDTH, HEIGHT = 500, 550
    FPS = 4096
    COLORS = {
        0: (204, 192, 179),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
    }

    def reset_game(self):
        self.game = GameOf2048()

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("2048 by Anthony Du")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 80)
        self.reset_game()

    def play_step(self, action):
        self.clock.tick(self.FPS)
        self.window.fill("#faf8ef")
        self.draw()
        prev_score = self.game.score
        prev_ajacent = self.adjacent()
        self.step(action)
        pygame.display.flip()
        if self.game.game_over():
            return 0, True, self.game.score
        else:
            diff = self.game.score - prev_score
            if diff != 0:
                return math.log2(diff) * 16 + self.adjacent(), False, self.game.score
            elif prev_ajacent >= self.adjacent():
                return -100, False, self.game.score
            else:
                return 0, False, self.game.score

    def draw(self):
        text = self.font.render(str(self.game.score), True, "#776e65")
        rect = text.get_rect(center=(self.WIDTH / 2, 50))
        self.window.blit(text, rect)
        pygame.draw.rect(self.window, "#bbada0", (45, 95, 410, 410), 0, 10)
        for row in range(GameOf2048.DIM):
            for col in range(GameOf2048.DIM):
                pygame.draw.rect(
                    self.window,
                    self.COLORS.get(self.game.board[row, col]),
                    (55 + col * 100, 105 + row * 100, 90, 90),
                    0,
                    10,
                )
                if self.game.board[row, col] != 0:
                    font_size = 80 if self.game.board[row, col] < 100 else 50
                    text = pygame.font.SysFont(None, font_size).render(
                        str(self.game.board[row, col]), True, "#776e65"
                    )
                    rect = text.get_rect(center=(100 + col * 100, 150 + row * 100))
                    self.window.blit(text, rect)

    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        before = self.game.board.copy()
        match action:
            case [1, 0, 0, 0]:
                self.game.move(Directions.UP)
            case [0, 1, 0, 0]:
                self.game.move(Directions.DOWN)
            case [0, 0, 1, 0]:
                self.game.move(Directions.LEFT)
            case [0, 0, 0, 1]:
                self.game.move(Directions.RIGHT)
        valid = not np.all(before == self.game.board)
        if valid:
            self.game.place_new_number()
        return valid

    def empty_spaces(self):
        sum = 0
        for i in range(self.game.DIM):
            for j in range(self.game.DIM):
                this = self.game.board[i][j]
                if this == 0:
                    sum += 1
        return sum

    def adjacent(self):
        sum = 0
        for i in range(self.game.DIM):
            for j in range(self.game.DIM):
                this = self.game.board[i][j]
                if this != 0:
                    if i + 1 < self.game.DIM and self.game.board[i + 1][j] == this:
                        sum += math.log2(this)
                    if j + 1 < self.game.DIM and self.game.board[i][j + 1] == this:
                        sum += math.log2(this)
                    if i - 1 >= 0 and self.game.board[i - 1][j] == this:
                        sum += math.log2(this)
                    if j - 1 >= 0 and self.game.board[i][j - 1] / this > 2:
                        sum += math.log2(this)
                    if i + 1 < self.game.DIM and self.game.board[i + 1][j] > this:
                        sum -= math.log2(self.game.board[i + 1][j] / this) * 2
                    if j + 1 < self.game.DIM and self.game.board[i][j + 1] > this:
                        sum -= math.log2(self.game.board[i][j + 1] / this) * 2
                    if i - 1 >= 0 and self.game.board[i - 1][j] > this:
                        sum -= math.log2(self.game.board[i - 1][j] / this) * 2
                    if j - 1 >= 0 and self.game.board[i][j - 1] > this:
                        sum += math.log2(self.game.board[i][j - 1] / this) * 2
        return sum

    def exposed(self):
        sum = 0
        for i in range(self.game.DIM):
            for j in range(self.game.DIM):
                surrounded = True
                this = self.game.board[i][j]
                if this != 0:
                    if i + 1 < self.game.DIM and self.game.board[i + 1][j] == 0:
                        sum += 16 - math.log2(this)
                        surrounded = False
                    if j + 1 < self.game.DIM and self.game.board[i][j + 1] == 0:
                        sum += 16 - math.log2(this)
                        surrounded = False
                    if i - 1 >= 0 and self.game.board[i - 1][j] == 0:
                        sum += 16 - math.log2(this)
                        surrounded = False
                    if j - 1 >= 0 and self.game.board[i][j - 1] == 0:
                        sum += 16 - math.log2(this)
                        surrounded = False
                    if surrounded:
                        sum -= 16 - math.log2(this)
        return sum / 16

from GameOf2048 import GameOf2048
import pygame
import numpy as np


class GameOf2048GUI:
    WIDTH, HEIGHT = 500, 550
    FPS = 30
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

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("2048 by Anthony Du")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 80)
        self.game = GameOf2048()
        while self.running:
            self.clock.tick(self.FPS)
            self.window.fill("#faf8ef")
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.on_key_down(event)
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
        pygame.quit()

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
        if self.game.game_over():
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.fill("#faf8ef")
            overlay.set_alpha(160)
            self.window.blit(overlay, (0, 0))
            text = self.font.render("Game Over", True, "#776e65")
            rect = text.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2 - 25))
            self.window.blit(text, rect)
            text = pygame.font.SysFont(None, 50).render(
                "Press R to restart", True, "#776e65"
            )
            rect = text.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2 + 25))
            self.window.blit(text, rect)

    def on_key_down(self, event):
        before = self.game.board.copy()
        match event.key:
            case pygame.K_UP:
                self.game.move("w")
            case pygame.K_DOWN:
                self.game.move("s")
            case pygame.K_LEFT:
                self.game.move("a")
            case pygame.K_RIGHT:
                self.game.move("d")
            case pygame.K_r:
                self.game = GameOf2048()
                return
        if not np.all(before == self.game.board):
            self.game.place_new_number()


if __name__ == "__main__":
    GameOf2048GUI()

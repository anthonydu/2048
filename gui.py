from GameOf2048 import GameOf2048
import pygame
import numpy as np


WIDTH, HEIGHT = 500, 500
FPS = 30
FONT_SIZE = 24
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


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 by Anthony Du")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont(None, 80)
    game = GameOf2048()
    game.place_new_number()

    def draw_board():
        pygame.draw.rect(window, "#bbada0", (45, 45, 410, 410), 0, 10)
        for row in range(GameOf2048.DIM):
            for col in range(GameOf2048.DIM):
                pygame.draw.rect(
                    window,
                    COLORS.get(game.board[row, col]),
                    (55 + col * 100, 55 + row * 100, 90, 90),
                    0,
                    10,
                )
                if game.board[row, col] != 0:
                    text = font.render(str(game.board[row, col]), True, (0, 0, 0))
                    rect = text.get_rect(center=(100 + col * 100, 100 + row * 100))
                    window.blit(text, rect)

    def on_key_down(event):
        before = game.board.copy()
        match event.key:
            case pygame.K_UP:
                game.move("w")
            case pygame.K_DOWN:
                game.move("s")
            case pygame.K_LEFT:
                game.move("a")
            case pygame.K_RIGHT:
                game.move("d")
        if not np.all(before == game.board):
            game.place_new_number()

    while running:
        clock.tick(FPS)
        window.fill("#faf8ef")

        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                on_key_down(event)
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

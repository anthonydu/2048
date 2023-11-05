import random


class MineSweeper:
    # mines:  0 - no mine
    #         1 - yes mine

    # states: 0 - hidden
    #         1 - visible
    #         2 - flagged

    def __init__(self, width: int, height: int) -> None:
        self.mines = [[0] * height] * width
        self.states = [[0] * height] * width
        self.width = width
        self.height = height

    # start game when the first square is clicked
    def start(self, x0: int, y0: int, numMines: int) -> None:
        self.states[x0][y0] = 1
        while numMines > 0:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if (x, y) != (x0, y0) and self.mines[x][y] != 1:
                self.grid[x][y] = 1
                numMines -= 1

    def flag(self, x: int, y: int) -> bool:
        if self.states[x][y] == 0:
            self.states[x][y] = 2
            return True
        else:
            return False

    def reveal(self, x: int, y: int) -> bool:
        if self.states[x][y] == 0:
            if self.mines[x][y] == 1:
                return True
            else:
                self.states[x][y] = 1

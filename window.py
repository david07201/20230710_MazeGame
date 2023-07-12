import sys

import pygame as pg
import pygame.locals as pgl


class Wall():
    def __init__(self, window, type, r, c):
        self.window = window
        self.type = type
        self.r = r
        self.c = c
        self.existed = True

    def create(self):
        self.existed = True

    def delete(self):
        self.existed = False

    def draw(self):
        if self.existed:
            if self.type == 'horizontal':
                y = UNIT * self.r + WALL_DEPTH // 2
                pg.draw.line(
                    surface=self.window, 
                    color=WHITE, 
                    start_pos=(UNIT * self.c, y), 
                    end_pos=(UNIT * (self.c + 1) + WALL_DEPTH // 2 + 1, y), 
                    width=WALL_DEPTH
                )
            elif self.type == 'vertical':
                x = UNIT * self.c + WALL_DEPTH // 2
                pg.draw.line(
                    surface=self.window, 
                    color=WHITE, 
                    start_pos=(x, UNIT * self.r), 
                    end_pos=(x, UNIT * (self.r + 1) + WALL_DEPTH // 2 + 1), 
                    width=WALL_DEPTH
                )

class Cell():
    def __init__(self, window, r, c):
        self.window = window
        self.r = r
        self.c = c
        self.visited = False

    def connect_walls(self, top: Wall, right: Wall, botton: Wall, left: Wall):
        self.top = top
        self.right = right
        self.botton = botton
        self.left = left

    def highlight(self):
        pg.draw.rect(
            self.window, 
            YELLOW, 
            (UNIT * self.c + WALL_DEPTH, 
             UNIT * self.r + WALL_DEPTH, 
             UNIT - WALL_DEPTH,
             UNIT - WALL_DEPTH)
        )


if __name__ == '__main__':
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 0, 0)
    UNIT = 40
    WALL_DEPTH = 5    # Odd number is prefered
    WINDOW_WIDTH = 800 + WALL_DEPTH
    WINDOW_HEIGHT = 800 + WALL_DEPTH
    ROWS = (WINDOW_HEIGHT - WALL_DEPTH) // UNIT
    COLUMNS = (WINDOW_WIDTH - WALL_DEPTH) // UNIT
    FPS = 30

    pg.init()
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()

    h_walls: list[Wall] = []
    for r in range(ROWS + 1):
        for c in range(COLUMNS):
            oWall = Wall(window, 'horizontal', r, c)
            h_walls.append(oWall)

    v_walls: list[Wall] = []
    for r in range(ROWS):
        for c in range(COLUMNS + 1):
            oWall = Wall(window, 'vertical', r, c)
            v_walls.append(oWall)
    
    cells: list[Cell] = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            oCell = Cell(window, r, c)
            oCell.connect_walls(
                top=h_walls[r * COLUMNS + c], 
                right=v_walls[r * (COLUMNS + 1) + c + 1],
                botton=h_walls[(r + 1) * COLUMNS + c],
                left=v_walls[r * (COLUMNS + 1) + c]
            )
            cells.append(oCell)
    
    test_r1 = 5
    test_c1 = 5
    test_cell = cells[test_r1 * COLUMNS + test_c1]
    test_cell.top.delete()
    test_cell.right.delete()
    test_cell.botton.delete()
    test_cell.left.delete()

    test_r2 = 5
    test_c2 = 5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        window.fill(BLACK)

        for oWall in h_walls + v_walls:
            oWall.draw()
        cells[test_r2 * COLUMNS + test_c2].highlight()
        
        pg.display.update()

        clock.tick(FPS)
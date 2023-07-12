import sys

import pygame as pg
import pygame.locals as pgl


class Cell():
    def __init__(self, window, r, c):
        self.window = window
        self.r = r
        self.c = c
        self.visited = False

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
                    end_pos=(UNIT * (self.c + 1) + WALL_DEPTH, y), 
                    width=WALL_DEPTH
                )
            elif self.type == 'vertical':
                x = UNIT * self.c + WALL_DEPTH // 2
                pg.draw.line(
                    surface=self.window, 
                    color=WHITE, 
                    start_pos=(x, UNIT * self.r), 
                    end_pos=(x, UNIT * (self.r + 1) + WALL_DEPTH), 
                    width=WALL_DEPTH
                )


if __name__ == '__main__':
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    UNIT = 40
    WALL_DEPTH = 1    # Odd number is prefered
    WINDOW_WIDTH = 800 + WALL_DEPTH
    WINDOW_HEIGHT = 800 + WALL_DEPTH
    ROWS = (WINDOW_HEIGHT - WALL_DEPTH) // UNIT
    COLUMNS = (WINDOW_WIDTH - WALL_DEPTH) // UNIT
    FPS = 30

    pg.init()
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()

    h_walls = []
    for r in range(ROWS + 1):
        for c in range(COLUMNS):
            oWall = Wall(window, 'horizontal', r, c)
            h_walls.append(oWall)

    v_walls = []
    for r in range(ROWS):
        for c in range(COLUMNS + 1):
            oWall = Wall(window, 'vertical', r, c)
            v_walls.append(oWall)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        window.fill(BLACK)

        for oWall in h_walls + v_walls:
            oWall.draw()

        pg.display.update()

        clock.tick(FPS)
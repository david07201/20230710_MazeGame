import sys

import pygame as pg


class Wall():
    def __init__(self, root: pg.Surface, type: str, r: int, c: int):
        self.root = root
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
                    surface=self.root, 
                    color=WHITE, 
                    start_pos=(UNIT * self.c, y), 
                    end_pos=(UNIT * (self.c + 1) + WALL_DEPTH // 2 + 1, y), 
                    width=WALL_DEPTH
                )
            elif self.type == 'vertical':
                x = UNIT * self.c + WALL_DEPTH // 2
                pg.draw.line(
                    surface=self.root, 
                    color=WHITE, 
                    start_pos=(x, UNIT * self.r), 
                    end_pos=(x, UNIT * (self.r + 1) + WALL_DEPTH // 2 + 1), 
                    width=WALL_DEPTH
                )

class Cell():
    def __init__(self, root: pg.Surface, r: int, c: int):
        self.root = root
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
            self.root, 
            YELLOW, 
            (UNIT * self.c + WALL_DEPTH, 
             UNIT * self.r + WALL_DEPTH, 
             UNIT - WALL_DEPTH,
             UNIT - WALL_DEPTH)
        )

class Text():
    def __init__(self, root: pg.Surface, loc: tuple[int, int], 
                 text: str, color: tuple[int, int, int]):
        pg.font.init()
        self.root = root
        self.loc = loc
        self.text = None
        self.color = color
        self.font = pg.font.SysFont('Comic Sans MS', 20)
        self.set_text(text)

    def set_text(self, text: str):
        if self.text == text:
            return
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)

    def draw(self):
        self.root.blit(self.text_surface, self.loc)
        
        


if __name__ == '__main__':
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 0, 0)
    UNIT = 40
    WALL_DEPTH = 3    # Odd number is prefered
    LABEL_HEIGHT = 30
    MAZE_WIDTH = 1280
    MAZE_HEIGHT = 600
    WINDOW_WIDTH = MAZE_WIDTH + WALL_DEPTH
    WINDOW_HEIGHT = MAZE_HEIGHT + WALL_DEPTH + LABEL_HEIGHT
    ROWS = (MAZE_HEIGHT) // UNIT
    COLUMNS = (MAZE_WIDTH) // UNIT
    FPS = 30

    pg.init()
    root = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()

    h_walls: list[Wall] = []
    for r in range(ROWS + 1):
        for c in range(COLUMNS):
            oWall = Wall(root, 'horizontal', r, c)
            h_walls.append(oWall)

    v_walls: list[Wall] = []
    for r in range(ROWS):
        for c in range(COLUMNS + 1):
            oWall = Wall(root, 'vertical', r, c)
            v_walls.append(oWall)
    
    cells: list[Cell] = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            oCell = Cell(root, r, c)
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

    oLabel = Text(
        root, 
        (10, WINDOW_HEIGHT - LABEL_HEIGHT), 
        ("PRESS: 'R' to RESTART; 'Q' to QUIT; "
        "'TOP', 'RIGHT', 'BOTTON', 'LEFT' to MOVE."),
        WHITE
    )

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

        root.fill(BLACK)

        for oWall in h_walls + v_walls:
            oWall.draw()
        cells[test_r2 * COLUMNS + test_c2].highlight()

        oLabel.draw()
        
        pg.display.update()

        clock.tick(FPS)
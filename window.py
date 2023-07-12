import sys

import pygame as pg


class Wall():
    def __init__(self, root: pg.Surface, type: str, r: int, c: int, unit: int,
                 wall_depth: int, color: tuple[int, int, int]):
        self.root = root
        self.type = type
        self.r = r
        self.c = c
        self.unit = unit
        self.wall_depth = wall_depth
        self.color = color
        self.existed = True

    def create(self):
        self.existed = True

    def delete(self):
        self.existed = False

    def draw(self):
        if self.existed:
            if self.type == 'horizontal':
                y = self.unit * self.r + self.wall_depth // 2
                start = (self.unit * self.c, y)
                end = (self.unit * (self.c + 1) + self.wall_depth // 2 + 1, y)
                pg.draw.line(
                    surface=self.root, 
                    color=self.color, 
                    start_pos=start, 
                    end_pos=end, 
                    width=self.wall_depth
                )
            elif self.type == 'vertical':
                x = self.unit * self.c + self.wall_depth // 2
                start = (x, self.unit * self.r)
                end = (x, self.unit * (self.r + 1) + self.wall_depth // 2 + 1)
                pg.draw.line(
                    surface=self.root, 
                    color=self.color, 
                    start_pos=start, 
                    end_pos=end, 
                    width=self.wall_depth
                )

class Cell():
    def __init__(self, root: pg.Surface, r: int, c: int, unit: int, 
                 wall_depth: int):
        self.root = root
        self.r = r
        self.c = c
        self.unit = unit
        self.wall_depth = wall_depth
        self.visited = False

    def connect_walls(self, top: Wall, right: Wall, botton: Wall, left: Wall):
        self.top = top
        self.right = right
        self.botton = botton
        self.left = left

    def connect_cells(self, cells: list, rows:int, columns: int):
        self.neighbors: list[Cell] = []
        # Top
        if self.r > 0:
            self.neighbors.append(cells[(self.r - 1) * columns + self.c])
        # Right
        if self.c < columns - 1:
            self.neighbors.append(cells[self.r * columns + self.c + 1])
        # Botton
        if self.r < rows - 1:
            self.neighbors.append(cells[(self.r + 1) * columns + self.c])
        # Left
        if self.c > 0:
            self.neighbors.append(cells[self.r * columns + self.c - 1])

    def highlight(self, color):
        pg.draw.rect(
            self.root, 
            color, 
            (self.unit * self.c + self.wall_depth, 
             self.unit * self.r + self.wall_depth, 
             self.unit - self.wall_depth,
             self.unit - self.wall_depth)
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
    YELLOW = (255, 255, 0)
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
            oWall = Wall(root, 'horizontal', r, c, UNIT, WALL_DEPTH, WHITE)
            h_walls.append(oWall)

    v_walls: list[Wall] = []
    for r in range(ROWS):
        for c in range(COLUMNS + 1):
            oWall = Wall(root, 'vertical', r, c, UNIT, WALL_DEPTH, WHITE)
            v_walls.append(oWall)
    
    cells: list[Cell] = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            oCell = Cell(root, r, c, UNIT, WALL_DEPTH)
            oCell.connect_walls(
                top=h_walls[r * COLUMNS + c], 
                right=v_walls[r * (COLUMNS + 1) + c + 1],
                botton=h_walls[(r + 1) * COLUMNS + c],
                left=v_walls[r * (COLUMNS + 1) + c]
            )
            cells.append(oCell)
    for oCell in cells:
        oCell.connect_cells(cells, ROWS, COLUMNS)
    
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
                if event.key == pg.K_r:
                    print(cells[test_r2 * COLUMNS + test_c2].neighbors[0].r)
                    print(cells[test_r2 * COLUMNS + test_c2].neighbors[0].c)

        root.fill(BLACK)

        for oWall in h_walls + v_walls:
            oWall.draw()
        cells[test_r2 * COLUMNS + test_c2].highlight(YELLOW)

        oLabel.draw()
        
        pg.display.update()

        clock.tick(FPS)
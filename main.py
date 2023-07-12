import sys
import random

import pygame as pg

import window


class Maze():
    def __init__(self, 
                 cells: list[window.Cell], h_walls: list[window.Wall], 
                 v_walls: list[window.Wall]):
        self.cells = cells
        self.h_walls = h_walls
        self.v_walls = v_walls
        self.is_generating = False
        self.stack = []
        self.cur = None
        self.pre1 = None
        self.pre2 = None
        self.pre3 = None
        self.pre4 = None
        self.pre5 = None


    def update(self):
        def choose_neighbor(cell: window.Cell):
            candidate = []
            for i, neighbor in enumerate(cell.neighbors):
                if neighbor is not None:
                    if not neighbor.generated:
                        candidate.append((neighbor, i))
            if candidate == []:
                return None
            else:
                return random.choice(candidate)

        if self.cur is None:
            self.reset()
            self.cur = random.choice(self.cells)
        next = choose_neighbor(self.cur)
        if not next and not self.stack:
            self.is_generating = False
            self.cur = None
            self.pre1 = None
            self.pre2 = None
            self.pre3 = None
            self.pre4 = None
            self.pre5 = None
            self.stack.clear()
            self.set_goal_pos()
            self.set_goal_pos()
            return
        if next:
            self.stack.append(self.cur)
            self.cur.walls[next[1]].delete()
            self.cur.generated = True
            self.cur = next[0]
        elif self.stack:
            self.cur.generated = True
            self.cur = self.stack.pop()
        self.pre5 = self.pre4
        self.pre4 = self.pre3
        self.pre3 = self.pre2
        self.pre2 = self.pre1
        self.pre1 = self.cur


    def reset(self):
        for oWall in self.h_walls + self.v_walls:
            oWall.existed = True
        for oCell in self.cells:
            oCell.generated = False


    def set_start_pos(self):
        pass

    def set_goal_pos(self):
        pass
        
        


if __name__ == '__main__':
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    YELLOW1 = (YELLOW[0] // 6 * 5, YELLOW[1] // 6 * 5, 0)
    YELLOW2 = (YELLOW[0] // 6 * 4, YELLOW[1] // 6 * 4, 0)
    YELLOW3 = (YELLOW[0] // 6 * 3, YELLOW[1] // 6 * 3, 0)
    YELLOW4 = (YELLOW[0] // 6 * 2, YELLOW[1] // 6 * 2, 0)
    YELLOW5 = (YELLOW[0] // 6 * 1, YELLOW[1] // 6 * 1, 0)
    UNIT = 40
    WALL_DEPTH = 3    # Odd number is prefered
    LABEL_HEIGHT = 30
    MAZE_WIDTH = 1280
    MAZE_HEIGHT = 600
    WINDOW_WIDTH = MAZE_WIDTH + WALL_DEPTH
    WINDOW_HEIGHT = MAZE_HEIGHT + WALL_DEPTH + LABEL_HEIGHT
    ROWS = (MAZE_HEIGHT) // UNIT
    COLUMNS = (MAZE_WIDTH) // UNIT
    FPS = 60

    pg.init()
    root = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()

    h_walls: list[window.Wall] = []
    for r in range(ROWS + 1):
        for c in range(COLUMNS):
            oWall = window.Wall(
                root, 'horizontal', r, c, UNIT, WALL_DEPTH, WHITE)
            h_walls.append(oWall)

    v_walls: list[window.Wall] = []
    for r in range(ROWS):
        for c in range(COLUMNS + 1):
            oWall = window.Wall(
                root, 'vertical', r, c, UNIT, WALL_DEPTH, WHITE)
            v_walls.append(oWall)
    
    cells: list[window.Cell] = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            oCell = window.Cell(root, r, c, UNIT, WALL_DEPTH)
            oCell.connect_walls(h_walls, v_walls, COLUMNS)
            cells.append(oCell)
    for oCell in cells:
        oCell.connect_cells(cells, ROWS, COLUMNS)
    
    oMaze = Maze(cells, h_walls, v_walls)

    oLabel = window.Text(
        root, 
        (10, WINDOW_HEIGHT - LABEL_HEIGHT), 
        ("PRESS: 'R' to RESTART; 'Q' to QUIT; "
        "'TOP', 'RIGHT', 'BOTTON', 'LEFT' to MOVE."),
        WHITE
    )

    key_press = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

        if oMaze.is_generating:
            oMaze.update()
        else:
            if key_press is False and event.type == pg.KEYDOWN:
                key_press = True
                match event.key:
                    case pg.K_r:
                        oMaze.is_generating = True
                    case pg.K_UP:
                        print('UP')
                    case pg.K_RIGHT:
                        oMaze.is_generating = True
                    case pg.K_DOWN:
                        pass
                    case pg.K_LEFT:
                        pass
                    case _:
                        pass
            elif key_press is True and event.type == pg.KEYUP:
                key_press = False



        root.fill(BLACK)

        if oMaze.pre5:
            oMaze.pre5.highlight(YELLOW5)
        if oMaze.pre4:
            oMaze.pre4.highlight(YELLOW4)
        if oMaze.pre3:
            oMaze.pre3.highlight(YELLOW3)
        if oMaze.pre2:
            oMaze.pre2.highlight(YELLOW2)
        if oMaze.pre1:
            oMaze.pre1.highlight(YELLOW1)        
        if oMaze.cur:
            oMaze.cur.highlight(YELLOW)
        
        for oWall in h_walls + v_walls:
            oWall.draw()

        oLabel.draw()
        
        pg.display.update()

        clock.tick(FPS)
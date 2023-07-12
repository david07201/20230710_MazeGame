import sys

import pygame as pg

import window



        
        


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
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()

    h_walls: list[window.Wall] = []
    for r in range(ROWS + 1):
        for c in range(COLUMNS):
            oWall = window.Wall(window, 'horizontal', r, c)
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

    oLabel = Text(
        window, 
        (10, WINDOW_HEIGHT - LABEL_HEIGHT), 
        ("PRESS: 'R' to RESTART; 'Q' to QUIT; "
        "'TOP', 'RIGHT', 'BOTTON', 'LEFT' to MOVE.")
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

        window.fill(BLACK)

        for oWall in h_walls + v_walls:
            oWall.draw()
        cells[test_r2 * COLUMNS + test_c2].highlight()

        oLabel.draw()
        
        pg.display.update()

        clock.tick(FPS)
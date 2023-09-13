import math
import numpy as np
import pygame as pg
import sys

# board dimensions
ROW = 6
COL = 7

# pygame dimensions
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
SQUARESIZE = 100
WIDTH = COL * SQUARESIZE
HEIGHT = (ROW+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)

# players
EMPTY = 0
PLAYER = 1
AI = 2

# colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_GREY = (200, 200, 200)

# pygame inits
pg.init()
myfont = pg.font.SysFont("monospace", 75)

class Gameboard:

    def __init__(self):
        self.state = np.zeros((ROW, COL), dtype=int)
        self.screen = self.setup()

    def setup(self):
        screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Connect 4')

        # Fill the screen with the background color
        screen.fill(BLACK)

        # Draw the board background
        pg.draw.rect(screen, BLUE, (0, SQUARESIZE, WIDTH, HEIGHT - SQUARESIZE))

        # Return the surface
        return screen

    def draw_board(self):
        # draw board
        for c in range(COL):
            for r in range(ROW):
                pg.draw.rect(self.screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
        
        # draw checker pieces
        for c in range(COL):
            for r in range(ROW):
                if self.state[r][c] == PLAYER:
                    pg.draw.circle(self.screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2 + 100)), RADIUS)
                elif self.state[r][c] == AI:
                    pg.draw.circle(self.screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2 + 100)), RADIUS)
                else:
                    pg.draw.circle(self.screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        
        pg.display.update()

    def print_state(self):
        for row in self.state:
            print(" ".join(str(int(cell)) for cell in row))

    # only changes state and doesnt get new child
    def drop_piece(self, row, col, player):
        for i in range(row+1):
            if i != 0:
                self.state[i-1][col] = EMPTY
            self.state[i][col] = PLAYER if player == PLAYER else AI
            self.draw_board()
            pg.time.wait(100)

    # returns next open row in a certain column
    def get_next_open_row(self, col):
        for i in range(ROW-1, -1, -1):
            if self.state[i][col] == EMPTY:
                return i

    # returns number tof empty spaces     
    def empty_spaces(self):
        return np.count_nonzero(self.state == 0)
    
    # possible winning moves
    def winning_move(self, player):
        # Check horizontal locations for win
        for c in range(COL-3):
            for r in range(ROW):
                if self.state[r][c] == player and self.state[r][c+1] == player and self.state[r][c+2] == player and self.state[r][c+3] == player:
                    return True
        # Check vertical locations for win
        for c in range(COL):
            for r in range(ROW-3):
                if self.state[r][c] == player and self.state[r+1][c] == player and self.state[r+2][c] == player and self.state[r+3][c] == player:
                    return True
        # Check negatively sloped diaganols
        for c in range(COL-3):
            for r in range(ROW-3):
                if self.state[r][c] == player and self.state[r+1][c+1] == player and self.state[r+2][c+2] == player and self.state[r+3][c+3] == player:
                    return True
        # Check positively sloped diaganols
        for c in range(COL-3):
            for r in range(3, ROW):
                if self.state[r][c] == player and self.state[r-1][c+1] == player and self.state[r-2][c+2] == player and self.state[r-3][c+3] == player:
                    return True
                
    # returns indeces of valid columns
    def get_available_actions(self):
        return [c for c in range(COL) if any(self.state[:, c] == 0)]
    
    def player_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEMOTION:
                pg.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                pg.draw.circle(self.screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                pg.display.update()

            if event.type == pg.MOUSEBUTTONDOWN:
                pg.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))  
                posx = event.pos[0]
                action = (int(math.floor(posx/SQUARESIZE)))
                if action in self.get_available_actions():
                    row = self.get_next_open_row(action)
                    self.drop_piece(row, action, PLAYER)
                    return True, action
        return False, None
    
    def display(self, label, x, y, color):
        label = myfont.render(label, 1, color)
        self.screen.blit(label, (x,y))
        pg.display.update()
    
    def is_game_over(self):
        return not self.empty_spaces() or self.winning_move(AI) or self.winning_move(PLAYER) 
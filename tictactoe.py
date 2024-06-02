import sys
import pygame # type: ignore
import numpy as np

from constants import *

#PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE AI")
screen.fill(BG_COLOUR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.num_marked_sqrs = 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.num_marked_sqrs += 1

    def is_empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def is_full(self):
        return self.num_marked_sqrs == 9
    
    def is_empty(self):
        return self.num_marked_sqrs == 0
    
    def get_empty_sqrs(self):
        return [[row, col] for row in range(ROWS) for col in range(COLS) if self.is_empty_sqr(row, col)]
    
    def currunt_state(self):
        # return 0 if there is no win yet
        # return 1 if player 1 has won
        # return 2 if player 2 has won

        # verticle wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
            
        # horzontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
            
        # desc diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            self.squares[1][1]

        # asc diagonal win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            self.squares[1][1]

        #* if no win yet
        return 0


class Game:
    def __init__(self):
        self.board = Board()
        # Todo: self.ai = AI()
        self.player = 1         # 1-X   # 2-O
        self.gamemode = "pvp"  #! pvp or ai
        self.running = True
        self.show_lines()

    def show_lines(self):

        # verticle
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(screen, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT-SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw X
            # desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOUR, start_desc, end_desc, CROSS_WIDTH)

            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOUR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # draw O
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOUR, center, RADIUS, CIRC_WIDTH)


    # Changes from one player to another
    def next_turn(self):
        self.player = self.player % 2 + 1


def main():

    # Object
    game = Game()
    board = game.board

    # Game loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = int(pos[0] // SQSIZE)
                row = int(pos[1] // SQSIZE)

                if board.is_empty_sqr(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()
                    print(board.squares)
            
        
        pygame.display.update()

main()


import copy
import random
import sys
import pygame # type: ignore
import numpy as np # type: ignore

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
        # return [[row, col] for row in range(ROWS) for col in range(COLS) if self.is_empty_sqr(row, col)]
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs
    
    def current_state(self, show = False):
        # return 0 if there is no win yet
        # return 1 if player 1 has won
        # return 2 if player 2 has won

        # verticle wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    colour = CIRC_COLOUR if self.squares[0][col] == 2 else CROSS_COLOUR
                    iPos = (col * SQSIZE + SQSIZE // 2, FINAL_OFFSET)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - FINAL_OFFSET)
                    pygame.draw.line(screen, colour, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        # horzontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    colour = CIRC_COLOUR if self.squares[row][0] == 2 else CROSS_COLOUR
                    iPos = (FINAL_OFFSET, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - FINAL_OFFSET, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, colour, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
            
        # desc diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    colour = CIRC_COLOUR if self.squares[1][1] == 2 else CROSS_COLOUR
                    iPos = (FINAL_OFFSET, FINAL_OFFSET)
                    fPos = (WIDTH - FINAL_OFFSET, HEIGHT - FINAL_OFFSET)
                    pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    colour = CIRC_COLOUR if self.squares[1][1] == 2 else CROSS_COLOUR
                    iPos = (FINAL_OFFSET, HEIGHT - FINAL_OFFSET)
                    fPos = (WIDTH - FINAL_OFFSET, FINAL_OFFSET)
                    pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        #* if no win yet
        return 0

class AI:

    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player

    def random_choice(self, board):
        empty_sqrs = board.get_empty_sqrs()
        return random.choice(empty_sqrs)    # row, col
    
    def minimax(self, board, maximizing):
        
        # terminal case
        state = board.current_state()

        #* player 1 wins
        if state == 1:
            return 1, None      #! eval, move
        
        #* player 2 wins
        elif state == 2:
            return -1, None
        
        #* draw
        elif board.is_full():
            return 0, None
        
        elif maximizing:
            max_eval = -101
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                current_eval = self.minimax(temp_board, False)[0]
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 101
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                current_eval = self.minimax(temp_board, True)[0]
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = (row, col)

            return min_eval, best_move

    

    def eval(self, main_board):
        if self.level == 0:
            #* random choice
            current_eval = "random"
            move = self.random_choice(main_board)
        else:
            #* minimax algorithm choice
            current_eval, move = self.minimax(main_board, False)

        print(f"AI has chosen to mark the square in pos {move} with an eval of {current_eval}.")

        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1         # 1-X   # 2-O
        self.gamemode = "ai"  #! pvp or ai
        self.running = True
        self.show_lines()

    def show_lines(self):

        # USED to reset the screen
        screen.fill(BG_COLOUR)

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
 

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.current_state(show=True) != 0 or self.board.is_full()

    def reset(self):
        self.__init__()


def main():

    # Object
    game = Game()
    ai = game.ai
    board = game.board

    # Game loop
    while True:
        #TODO: implement ktinker GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = int(pos[0] // SQSIZE)
                row = int(pos[1] // SQSIZE)
                
                if board.is_empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

            if event.type == pygame.KEYDOWN:

                #! g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                #! 0-randon AI
                if event.key == pygame.K_0:
                    ai.level = 0

                #! 1-randon AI
                if event.key == pygame.K_1:
                    ai.level = 1

                #! r-randon AI
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                    
            
        if game.gamemode == "ai" and game.player == ai.player and game.running:
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                    game.running = False
        
        pygame.display.update()

main()


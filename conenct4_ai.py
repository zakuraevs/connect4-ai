import numpy as np
import pygame
import sys
import math
from threading import Timer
import random

# initial variables
# -------------------------------
# capitalized because they are global and static
ROWS = 6
COLS = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# various functions used by the game
# -------------------------------
# using numpy, create an empty matrix of 6 rows and 7 columns
def create_board():
    board = np.zeros((ROWS, COLS))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece

# checking that the top row of the selected column is still not fileld
# ie that there is still space in the current column
# note that indexing starts at 0


def is_valid_location(board, col):
    return board[0][col] == 0

# checking where the piece will fall in the current column
# ie finding the first zero row in given column
def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

# not the best way to do it but simple

def winning_move(board, piece):
    # checking horizontal locations for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking horizontal locations for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # checking positively sloped diagonals for win
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    # checking negatively sloped diagonals for win
    for c in range(3,COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else :
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()


def evaluate_window(window, piece):
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 80    

    return score    

def score_position(board, piece):

    score = 0

    # score center column
    center_array = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)


    # score positively sloped diagonals
    for r in range(3,ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # score negatively sloped diagonals
    for r in range(3,ROWS):
        for c in range(3,COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)


    return score


def get_valid_locations(board):
    valid_locations = []
    
    for column in range(COLS):
        if is_valid_location(board, column):
            valid_locations.append(column)

    return valid_locations


def pick_best_move(board, piece):
    best_score = -1000
    valid_locations = get_valid_locations(board)
    best_column = random.choice(valid_locations)

    for column in valid_locations:
        row = get_next_open_row(board, column)
        temp_board = board.copy()
        drop_piece(temp_board, row, column, piece)

        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_column = column

    return best_column




# various state tracker variables
# -------------------------------
# initializing the board
board = create_board()

# initially nobody has won yet
game_over = False

not_over = True

def end_game():
    global game_over
    game_over = True
    print(game_over)

# initialy it is player 1's turn
turn = 1#random.randint(PLAYER, AI)

pygame.init()
SQUARESIZE = 100

width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)



# game loop
# -------------------------------

# loop that runs while the game_over variable is false,
# ie someone hasn't placed 4 in a row yet
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            xpos = pygame.mouse.get_pos()[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius )
            

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # ask for player 1 inupt
            if turn == PLAYER:
                # we assume players will use correct input
                xpos = event.pos[0] 
                col = int(math.floor(xpos/SQUARESIZE)) #int(input("Player 1 make your selection by typing (0-6):"))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        print("PLAYER 1 WINS!")
                        label = my_font.render("PLAYER 1 WINS!", 1, RED)
                        screen.blit(label, (40, 10))
                        not_over = False
                        t = Timer(3.0, end_game)
                        t.start()
                
                # increment turn by 1
                turn += 1
                # this will alternate between 0 and 1 withe very turn
                turn = turn % 2 

                     
    # ask for player 2 input
    if turn == AI and not game_over:

        #col = random.randint(0, COLS - 1)
        col = pick_best_move(board, AI_PIECE)

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                print("PLAYER 2 WINS!")
                label = my_font.render("PLAYER 2 WINS!", 1, YELLOW)
                screen.blit(label, (40, 10))
                not_over = False
                t = Timer(3.0, end_game)
                t.start()
        draw_board(board)    

        # increment turn by 1
        turn += 1
        # this will alternate between 0 and 1 withe very turn
        turn = turn % 2

        #draw_board(board)

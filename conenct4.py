import numpy as np

# initial variables
# -------------------------------
# capitalized because they are global and static
ROWS = 6
COLS = 7




# various functions used by the game
# -------------------------------
# using numpy, create an empty matrix of 6 rows and 7 columns
def create_board():
    board = np.zeros((ROWS,COLS))
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
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3]:
                return True

    # checking horizontal locations for win
    for c in range(COLS):
            for r in range(ROWS-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c]:
                    return True

    # checking positively sloped diagonals for win
    for c in range(COLS-3):
                for r in range(ROWS-3):
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3]:
                        return True




    # checking negatively sloped diagonals for win






# various state tracker variables
# -------------------------------
# initializing the board
board = create_board()
#print(board)

# initially nobody has won yet
game_over = False

# initialy it is player 1's turn
turn = 0




# game loop
# -------------------------------

# loop that runs while the game_over variable is false,
# ie someone hasn't placed 4 in a row yet
while not game_over:
    # ask for player 1 inupt
    if turn == 0:
        # we assume players will use correct input 
        col = int(input("Player 1 make your selection by typing (0-6):"))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("PLAYER 1 WINS!")
                game_over = True

    # ask for player 2 input
    else:
        col = int(input("Player 2 make your selection by typing (0-6):"))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                print("PLAYER 2 WINS!")
                game_over = True

    print(board)

    # increment turn by 1
    turn += 1
    # this will alternate between 0 and 1 withe very turn
    turn = turn % 2
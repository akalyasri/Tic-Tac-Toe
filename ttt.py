import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

def initial_state(board_size):
    """
    Returns starting state of the board based on board_size.
    """
    return [[EMPTY for _ in range(board_size)] for _ in range(board_size)]


def player(board):
    """
    Returns the player who has the next turn on the board.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    return O if count_x > count_o else X


def actions(board):
    """
    Returns the set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board resulting from making move (i, j).
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid Move")
    
    new_board = deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def check_winner(board, k):
    """
    Returns the winner (X or O) if there is one, otherwise None.
    Works for NxN boards with a dynamic winning condition (k-in-a-row).
    """
    n = len(board)

    # Check rows and columns
    for i in range(n):
        for j in range(n - k + 1):  # Ensure at least k elements in the row/column
            # Check row
            if board[i][j] is not None and all(board[i][j] == board[i][j + d] for d in range(k)):
                return board[i][j]
            # Check column
            if board[j][i] is not None and all(board[j][i] == board[j + d][i] for d in range(k)):
                return board[j][i]

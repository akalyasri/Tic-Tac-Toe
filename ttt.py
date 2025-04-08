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

    # Check diagonals
    for i in range(n - k + 1):

        for j in range(n - k + 1):

            # Check main diagonal
            if board[i][j] is not None and all(board[i + d][j + d] == board[i][j] for d in range(k)):
                return board[i][j]
            
            # Check anti-diagonal
            if board[i][j + k - 1] is not None and all(board[i + d][j + k - 1 - d] == board[i][j + k - 1] for d in range(k)):
                return board[i][j + k - 1]

    return None


def terminal(board, k):
    """
    Returns True if the game is over (win or draw), False otherwise.
    """
    return check_winner(board, k) is not None or not any(EMPTY in row for row in board)


def utility(board, k):
    """
    Returns 1 if X wins, -1 if O wins, 0 for a draw.
    """
    winner = check_winner(board, k)
    if winner == X:
        return 1
    elif winner == O:
        return -1
    else:
        return 0


def minimax(board, k, depth_limit=5):
    """
    Returns the best move using Minimax with Alpha-Beta Pruning and a depth limit.
    """
    if terminal(board, k):
        return None

    current_player = player(board)
    alpha, beta = -float('inf'), float('inf')

    if current_player == X:
        return max_alpha_beta(board, alpha, beta, k, 0, depth_limit)[1]
    else:
        return min_alpha_beta(board, alpha, beta, k, 0, depth_limit)[1]
    
def max_alpha_beta(board, alpha, beta, k, depth, depth_limit):
    """
    Maximizing function for Alpha-Beta Pruning.
    """
    if terminal(board, k) or depth >= depth_limit:
        return utility(board, k), None

    best_score = -float('inf')
    best_action = None

    for action in actions(board):
        score, _ = min_alpha_beta(result(board, action), alpha, beta, k, depth + 1, depth_limit)
        if score > best_score:
            best_score, best_action = score, action
        alpha = max(alpha, best_score)
        if beta <= alpha:
            break  # Prune

    return best_score, best_action


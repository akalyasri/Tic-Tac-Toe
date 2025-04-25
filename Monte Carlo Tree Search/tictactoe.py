from copy import deepcopy
from mcts import *

# Tic Tac Toe board class
class Board():
    # create constructor (init board class instance)
    def __init__(self, board=None):
        # define players
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '.'
        self.position = {}
    
        self.init_board()
        
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
    
  
    def init_board(self):
        
        for row in range(3):
            for col in range(3):
                self.position[row, col] = self.empty_square
    
    def make_move(self, row, col):
        board = Board(self)
        board.position[row, col] = self.player_1
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        return board
    
    # get whether the game is drawn
    def is_draw(self):
        for row, col in self.position:
            # empty square is available
            if self.position[row, col] == self.empty_square:
                return False
        return True
    
    # get whether the game is won
    def is_win(self):
        for col in range(3):
            winning_sequence = []

            for row in range(3):
                # if found same next element in the row
                if self.position[row, col] == self.player_2:
                    winning_sequence.append((row, col))
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    return True
                
        for row in range(3):
            winning_sequence = []            

            for col in range(3):
                # if found same next element in the row
                if self.position[row, col] == self.player_2:
                    winning_sequence.append((row, col))
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    return True
        winning_sequence = []
        
        for row in range(3):
            col = row
        
            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                winning_sequence.append((row, col))
                
            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                return True
        winning_sequence = []
        
        for row in range(3):
            # init column
            col = 3 - row - 1
        
            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                winning_sequence.append((row, col))
                
            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                return True
        return False
    
    # generate legal moves to play in the current position
    def generate_states(self):
        actions = []
        
        for row in range(3):
            for col in range(3):
                if self.position[row, col] == self.empty_square:
                    actions.append(self.make_move(row, col))
        
        return actions
    
    # main game loop
    def game_loop(self):
        print('\n  Tic Tac Toe by Code Monkey King\n')
        print('  Type "exit" to quit the game')
        print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')
        
        # print board
        print(self)
        
        # create MCTS instance
        mcts = MCTS()
                
        # game loop
        while True:
            user_input = input('> ')
            if user_input == 'exit': break
            if user_input == '': continue
            
            try:
                # parse user input (move format [col, row]: 1,2) 
                row = int(user_input.split(',')[1]) - 1
                col = int(user_input.split(',')[0]) - 1

                # check move legality
                if self.position[row, col] != self.empty_square:
                    print(' Illegal move!')
                    continue

                self = self.make_move(row, col)
                print(self)

                # check if the game is won
                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break
                
                # check if the game is drawn
                elif self.is_draw():
                    print('Game is drawn!\n')
                    break
            
                best_move = mcts.search(self)

                # make AI move
                self = best_move.board
                print(self)

                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break
                
                elif self.is_draw():
                    print('Game is drawn!\n')
                    break
                
            except Exception as e:
                print('  Error:', e)
                print('  Illegal command!')
                print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')
        
    # print board state
    def __str__(self):
        board_string = ''
        
        for row in range(3):
            for col in range(3):
                board_string += ' %s' % self.position[row, col]

            board_string += '\n'

        if self.player_1 == 'x':
            board_string = '\n--------------\n "x" to move:\n--------------\n\n' + board_string
        
        elif self.player_1 == 'o':
            board_string = '\n--------------\n "o" to move:\n--------------\n\n' + board_string
        return board_string

# main driver
if __name__ == '__main__':
    board = Board()    
    board.game_loop()

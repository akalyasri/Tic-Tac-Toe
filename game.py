import pygame
import sys
import time
import gameMaster as ttt

pygame.init()

# window size - might change later
size = width, height = 900, 700  

# colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = None  # in the begining, none
ai_turn = False

# asking user for size of board they want to play
def get_board_size():
    while True:
        try:
            size_input = int(input("Enter the size of the Tic-Tac-Toe board (nxn): "))
            if size_input < 3:
                print("The board size should be at least 3x3.")
            else:
                return size_input
        except ValueError:
            print("Please enter a valid integer.")

# creating board based on user input
board_size = get_board_size()  # board size from the user
board = ttt.initial_state(board_size)  # pass the size to your gameMaster's initial state
